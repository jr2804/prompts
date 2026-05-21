#!/usr/bin/env python3
# /// script
# dependencies = [
#   "defusedxml",
#   "lxml",
# ]
# /
"""Validate PPTX files against XSD schemas.

Usage:
    python validate.py <unpacked_dir> --original <original_file>
"""

import argparse
import sys
from pathlib import Path

from validators import PPTXSchemaValidator


def main():
    parser = argparse.ArgumentParser(description="Validate PPTX XML files")
    parser.add_argument("unpacked_dir", help="Path to unpacked PPTX directory")
    parser.add_argument("--original", required=True, help="Path to original .pptx file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    unpacked_dir = Path(args.unpacked_dir)
    original_file = Path(args.original)

    assert unpacked_dir.is_dir(), f"Error: {unpacked_dir} is not a directory"
    assert original_file.is_file(), f"Error: {original_file} is not a file"
    assert original_file.suffix.lower() == ".pptx", f"Error: {original_file} must be a .pptx file"

    validator = PPTXSchemaValidator(unpacked_dir, original_file, verbose=args.verbose)
    total_repairs = validator.repair()
    if total_repairs:
        print(f"Auto-repaired {total_repairs} issue(s)")

    success = validator.validate()
    if success:
        print("All validations PASSED!")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
