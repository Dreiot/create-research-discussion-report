#!/usr/bin/env python3
"""Validate structural and reader-facing contracts for a discussion DOCX."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from zipfile import BadZipFile, ZipFile

from lxml import etree


W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
M = "http://schemas.openxmlformats.org/officeDocument/2006/math"
NS = {"w": W, "m": M}
EXPECTED = {
    "ascii": "Times New Roman",
    "hAnsi": "Times New Roman",
    "cs": "Times New Roman",
    "eastAsia": "宋体",
}

INTERNAL_CONTEXT_PATTERNS = {
    "证据来源 heading": r"证据来源",
    "Git identity": r"Git\s*身份|\bGit\s+(?:branch|commit|SHA)\b",
    "repository analysis path": r"analysis_reports[/\\]",
    "repository evidence path": r"experiments[/\\]evidence[/\\]",
    "hash identity": r"\bSHA-?256\b|\b[0-9a-f]{40}\b",
}

ENGLISH_JARGON = ("baseline", "checkpoint", "runner", "quota", "claim")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("docx", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--allow-plain-greek", action="store_true")
    parser.add_argument("--allow-internal-context", action="store_true")
    return parser.parse_args()


def load_parts(path: Path) -> dict[str, bytes]:
    try:
        with ZipFile(path) as archive:
            return {name: archive.read(name) for name in archive.namelist()}
    except (BadZipFile, FileNotFoundError) as exc:
        raise SystemExit(f"cannot read DOCX: {exc}") from exc


def validate(path: Path, allow_plain_greek: bool, allow_internal_context: bool) -> dict:
    parts = load_parts(path)
    document = etree.fromstring(parts["word/document.xml"])
    settings = etree.fromstring(parts["word/settings.xml"])
    errors: list[str] = []
    warnings: list[str] = []

    display_math = len(document.xpath(".//m:oMathPara", namespaces=NS))
    all_math = len(document.xpath(".//m:oMath", namespaces=NS))
    inline_math = all_math - display_math
    math_styles = Counter(
        node.get(f"{{{M}}}val")
        for node in document.xpath(".//m:rPr/m:sty", namespaces=NS)
    )
    math_font = settings.xpath("string(.//m:mathFont/@m:val)", namespaces=NS)
    if all_math and math_font != "Times New Roman":
        errors.append(f"math font is {math_font!r}, expected Times New Roman")

    font_issues = 0
    theme_font_issues = 0
    for part_name, payload in parts.items():
        if not part_name.startswith("word/") or not part_name.endswith(".xml"):
            continue
        try:
            root = etree.fromstring(payload)
        except etree.XMLSyntaxError:
            continue
        for fonts in root.xpath(".//w:rFonts", namespaces=NS):
            actual = {key: fonts.get(f"{{{W}}}{key}") for key in EXPECTED}
            if actual != EXPECTED:
                font_issues += 1
            if any(
                fonts.get(f"{{{W}}}{key}")
                for key in ("asciiTheme", "hAnsiTheme", "eastAsiaTheme", "cstheme")
            ):
                theme_font_issues += 1
    if font_issues:
        errors.append(f"{font_issues} font declarations do not match the requested type system")
    if theme_font_issues:
        errors.append(f"{theme_font_issues} theme-font declarations remain")

    rows = document.xpath(".//w:tr", namespaces=NS)
    protected_rows = document.xpath(".//w:tr[w:trPr/w:cantSplit]", namespaces=NS)
    if len(protected_rows) != len(rows):
        errors.append(f"only {len(protected_rows)}/{len(rows)} table rows have w:cantSplit")

    plain_text = "".join(
        document.xpath(".//w:t[not(ancestor::m:oMath)]/text()", namespaces=NS)
    )
    greek = sorted(set(re.findall(r"[Α-Ωα-ωϕ]", plain_text)))
    if greek and not allow_plain_greek:
        errors.append(f"plain Greek variables outside OMML: {''.join(greek)}")

    percent_tokens = re.findall(r"(?<![\w.])\d+(?:\.\d+)?%", plain_text)
    inconsistent_percent_tokens = [
        token for token in percent_tokens if not re.fullmatch(r"\d+\.\d{2}%", token)
    ]
    if inconsistent_percent_tokens:
        errors.append(
            "percentage values without two decimals: "
            + ", ".join(sorted(set(inconsistent_percent_tokens)))
        )

    if not allow_internal_context:
        for label, pattern in INTERNAL_CONTEXT_PATTERNS.items():
            if re.search(pattern, plain_text, flags=re.IGNORECASE | re.MULTILINE):
                errors.append(f"reader-facing report contains internal context: {label}")

    lowered = plain_text.lower()
    for term in ENGLISH_JARGON:
        count = len(re.findall(rf"\b{re.escape(term)}\b", lowered))
        if count > 1:
            warnings.append(
                f"English jargon {term!r} appears {count} times; prefer Chinese after first use"
            )

    return {
        "path": str(path.resolve()),
        "display_math": display_math,
        "inline_math": inline_math,
        "math_styles": dict(math_styles),
        "math_font": math_font,
        "tables": len(document.xpath(".//w:tbl", namespaces=NS)),
        "table_rows": len(rows),
        "protected_table_rows": len(protected_rows),
        "font_issues": font_issues,
        "theme_font_issues": theme_font_issues,
        "errors": errors,
        "warnings": warnings,
        "ok": not errors,
    }


def main() -> int:
    args = parse_args()
    result = validate(
        args.docx,
        allow_plain_greek=args.allow_plain_greek,
        allow_internal_context=args.allow_internal_context,
    )
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"DOCX: {result['path']}")
        print(f"OMML: {result['display_math']} display, {result['inline_math']} inline")
        print(f"Tables: {result['protected_table_rows']}/{result['table_rows']} protected rows")
        print(f"Math styles: {result['math_styles']}")
        for warning in result["warnings"]:
            print(f"WARNING: {warning}")
        for error in result["errors"]:
            print(f"ERROR: {error}")
        if result["ok"]:
            print("OK: report validation passed")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
