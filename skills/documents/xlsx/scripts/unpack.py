#!/usr/bin/env python3
# /// script
# dependencies = [
#   "defusedxml",
# ]
# /
"""Unpack Office files (XLSX) for editing.

Usage:
    python unpack.py <xlsx_file> <output_dir>
"""

import argparse
import sys
import zipfile
from pathlib import Path

import defusedxml.minidom


def unpack(input_file: str, output_directory: str) -> tuple[None, str]:
    input_path = Path(input_file)
    output_path = Path(output_directory)

    if not input_path.exists():
        return None, f"Error: {input_file} does not exist"
    if input_path.suffix.lower() not in {".xlsx", ".xlsm"}:
        return None, f"Error: {input_file} must be a .xlsx or .xlsm file"

    try:
        output_path.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(input_path, "r") as zf:
            zf.extractall(output_path)

        xml_files = list(output_path.rglob("*.xml")) + list(output_path.rglob("*.rels"))
        for xml_file in xml_files:
            try:
                content = xml_file.read_text(encoding="utf-8")
                dom = defusedxml.minidom.parseString(content)
                xml_file.write_bytes(dom.toprettyxml(indent="  ", encoding="utf-8"))
            except Exception:
                pass

        return None, f"Unpacked {input_file} ({len(xml_files)} XML files)"

    except zipfile.BadZipFile:
        return None, f"Error: {input_file} is not a valid file"
    except Exception as e:
        return None, f"Error unpacking: {e}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unpack an XLSX file for editing")
    parser.add_argument("input_file", help="XLSX file to unpack")
    parser.add_argument("output_directory", help="Output directory")
    args = parser.parse_args()

    _, message = unpack(args.input_file, args.output_directory)
    print(message)
    if "Error" in message:
        sys.exit(1)
