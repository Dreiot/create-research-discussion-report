#!/usr/bin/env python3
"""Audit a generated academic discussion DOCX for the skill's hard contracts."""

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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("docx", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--allow-pp", action="store_true")
    parser.add_argument("--allow-plain-greek", action="store_true")
    return parser.parse_args()


def load_parts(path: Path) -> dict[str, bytes]:
    try:
        with ZipFile(path) as archive:
            return {name: archive.read(name) for name in archive.namelist()}
    except (BadZipFile, FileNotFoundError) as exc:
        raise SystemExit(f"cannot read DOCX: {exc}") from exc


def audit(path: Path, allow_pp: bool, allow_plain_greek: bool) -> dict:
    parts = load_parts(path)
    document = etree.fromstring(parts["word/document.xml"])
    settings = etree.fromstring(parts["word/settings.xml"])
    issues: list[str] = []

    display_math = len(document.xpath(".//m:oMathPara", namespaces=NS))
    all_math = len(document.xpath(".//m:oMath", namespaces=NS))
    inline_math = all_math - display_math
    math_styles = Counter(
        node.get(f"{{{M}}}val")
        for node in document.xpath(".//m:rPr/m:sty", namespaces=NS)
    )
    math_font = settings.xpath("string(.//m:mathFont/@m:val)", namespaces=NS)
    if all_math and math_font != "Times New Roman":
        issues.append(f"math font is {math_font!r}, expected Times New Roman")

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
            if any(fonts.get(f"{{{W}}}{key}") for key in ("asciiTheme", "hAnsiTheme", "eastAsiaTheme", "cstheme")):
                theme_font_issues += 1
    if font_issues:
        issues.append(f"{font_issues} font declarations do not match the requested type system")
    if theme_font_issues:
        issues.append(f"{theme_font_issues} theme-font declarations remain")

    rows = document.xpath(".//w:tr", namespaces=NS)
    protected_rows = document.xpath(".//w:tr[w:trPr/w:cantSplit]", namespaces=NS)
    if len(protected_rows) != len(rows):
        issues.append(f"only {len(protected_rows)}/{len(rows)} table rows have w:cantSplit")

    plain_text = "".join(document.xpath(".//w:t[not(ancestor::m:oMath)]/text()", namespaces=NS))
    if not allow_pp and re.search(r"(?i)(?:\bpp\b|百分点)", plain_text):
        issues.append("found pp/百分点; use 高/低 XX.XX% for this report style")
    greek = sorted(set(re.findall(r"[Α-Ωα-ωϕ]", plain_text)))
    if greek and not allow_plain_greek:
        issues.append(f"plain Greek variables outside OMML: {''.join(greek)}")

    percent_tokens = re.findall(r"(?<![\w.])\d+(?:\.\d+)?%", plain_text)
    bad_percent_tokens = [token for token in percent_tokens if not re.fullmatch(r"\d+\.\d{2}%", token)]
    if bad_percent_tokens:
        issues.append("percentage values without two decimals: " + ", ".join(sorted(set(bad_percent_tokens))))

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
        "issues": issues,
        "ok": not issues,
    }


def main() -> int:
    args = parse_args()
    result = audit(args.docx, args.allow_pp, args.allow_plain_greek)
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"DOCX: {result['path']}")
        print(f"OMML: {result['display_math']} display, {result['inline_math']} inline")
        print(f"Tables: {result['protected_table_rows']}/{result['table_rows']} protected rows")
        print(f"Math styles: {result['math_styles']}")
        if result["issues"]:
            for issue in result["issues"]:
                print(f"ERROR: {issue}")
        else:
            print("OK: report contract passed")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
