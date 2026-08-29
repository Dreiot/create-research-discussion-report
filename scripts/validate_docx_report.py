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
    styles = etree.fromstring(parts["word/styles.xml"])
    errors: list[str] = []
    warnings: list[str] = []

    normal_styles = styles.xpath(".//w:style[@w:styleId='Normal']", namespaces=NS)
    normal_first_line_chars = ""
    if normal_styles:
        normal_first_line_chars = normal_styles[0].xpath(
            "string(w:pPr/w:ind/@w:firstLineChars)", namespaces=NS
        )
    if normal_first_line_chars != "200":
        errors.append(
            "Normal style first-line indent is "
            f"{normal_first_line_chars!r}, expected w:firstLineChars='200'"
        )

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

    tables = document.xpath(".//w:tbl", namespaces=NS)
    centered_tables = [
        table
        for table in tables
        if table.xpath("string(w:tblPr/w:jc/@w:val)", namespaces=NS) == "center"
    ]
    if len(centered_tables) != len(tables):
        errors.append(f"only {len(centered_tables)}/{len(tables)} tables are centered")

    table_paragraphs = document.xpath(".//w:tc//w:p", namespaces=NS)
    zero_indent_table_paragraphs = []
    zero_spacing_table_paragraphs = []
    single_spacing_table_paragraphs = []
    centered_table_paragraphs = []
    for paragraph in table_paragraphs:
        first_line_chars = paragraph.xpath(
            "string(w:pPr/w:ind/@w:firstLineChars)", namespaces=NS
        )
        first_line_twips = paragraph.xpath(
            "string(w:pPr/w:ind/@w:firstLine)", namespaces=NS
        )
        if first_line_chars == "0" and first_line_twips == "0":
            zero_indent_table_paragraphs.append(paragraph)

        spacing = paragraph.xpath("w:pPr/w:spacing", namespaces=NS)
        if spacing:
            before = spacing[0].get(f"{{{W}}}before")
            after = spacing[0].get(f"{{{W}}}after")
            before_lines = spacing[0].get(f"{{{W}}}beforeLines")
            after_lines = spacing[0].get(f"{{{W}}}afterLines")
            before_auto = spacing[0].get(f"{{{W}}}beforeAutospacing")
            after_auto = spacing[0].get(f"{{{W}}}afterAutospacing")
            if (
                before == "0"
                and after == "0"
                and before_lines in (None, "0")
                and after_lines in (None, "0")
                and before_auto in (None, "0")
                and after_auto in (None, "0")
            ):
                zero_spacing_table_paragraphs.append(paragraph)

            line = spacing[0].get(f"{{{W}}}line")
            line_rule = spacing[0].get(f"{{{W}}}lineRule")
            if line == "240" and line_rule == "auto":
                single_spacing_table_paragraphs.append(paragraph)

        alignment = paragraph.xpath("string(w:pPr/w:jc/@w:val)", namespaces=NS)
        if alignment == "center":
            centered_table_paragraphs.append(paragraph)
    if len(zero_indent_table_paragraphs) != len(table_paragraphs):
        errors.append(
            "only "
            f"{len(zero_indent_table_paragraphs)}/{len(table_paragraphs)} "
            "table paragraphs explicitly reset both character and point first-line indent to zero"
        )
    if len(zero_spacing_table_paragraphs) != len(table_paragraphs):
        errors.append(
            "only "
            f"{len(zero_spacing_table_paragraphs)}/{len(table_paragraphs)} "
            "table paragraphs explicitly set spacing before and after to zero"
        )
    if len(centered_table_paragraphs) != len(table_paragraphs):
        errors.append(
            "only "
            f"{len(centered_table_paragraphs)}/{len(table_paragraphs)} "
            "table paragraphs are centered"
        )
    if len(single_spacing_table_paragraphs) != len(table_paragraphs):
        errors.append(
            "only "
            f"{len(single_spacing_table_paragraphs)}/{len(table_paragraphs)} "
            "table paragraphs use single line spacing"
        )

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
        "normal_first_line_chars": normal_first_line_chars,
        "tables": len(tables),
        "centered_tables": len(centered_tables),
        "table_rows": len(rows),
        "protected_table_rows": len(protected_rows),
        "table_paragraphs": len(table_paragraphs),
        "zero_indent_table_paragraphs": len(zero_indent_table_paragraphs),
        "zero_spacing_table_paragraphs": len(zero_spacing_table_paragraphs),
        "single_spacing_table_paragraphs": len(single_spacing_table_paragraphs),
        "centered_table_paragraphs": len(centered_table_paragraphs),
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
        print(f"Body first-line indent: {result['normal_first_line_chars']!r} character units")
        print(
            "Tables: "
            f"{result['centered_tables']}/{result['tables']} centered, "
            f"{result['protected_table_rows']}/{result['table_rows']} protected rows, "
            f"{result['zero_indent_table_paragraphs']}/{result['table_paragraphs']} "
            "cell paragraphs with zero first-line indent, "
            f"{result['zero_spacing_table_paragraphs']}/{result['table_paragraphs']} "
            "with zero spacing, "
            f"{result['single_spacing_table_paragraphs']}/{result['table_paragraphs']} "
            "with single line spacing, "
            f"{result['centered_table_paragraphs']}/{result['table_paragraphs']} centered"
        )
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
