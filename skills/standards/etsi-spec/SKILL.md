---
name: etsi-spec
description: Retrieving metadata and documentation for ETSI specifications. Use when you need to find latest version, full title, publication date, download URLs, or version history for any ETSI specification (EN, ES, EG, TS, TR, SR, GS, GR, PAS). Supports parts (e.g., -1, -2, -3).
---

# ETSI Specification Retrieval

## Overview

Retrieve comprehensive metadata for ETSI (European Telecommunications Standards Institute) specifications including latest version, full title, publication date, download URLs, and version history.

## Quick Start

To get metadata for an ETSI specification:

```bash
uv run python scripts/get_etsi_spec.py <spec-number>
```

**Accepted formats:**
- `103224` (six digits, defaults to TS type)
- `103 224` (three digits, space, three digits)
- `ETSI TS 103 224` (with prefix)
- `EG 202 396-3` (document type + spec + part)
- `TR 103 907` (document type + six digits)
- `ES 200 381-1` (document type + six digits + part)

**Examples:**
```bash
# TS (Technical Specification)
uv run python scripts/get_etsi_spec.py 103224
uv run python scripts/get_etsi_spec.py ETSI TS 103 224

# EG (ETSI Guide)
uv run python scripts/get_etsi_spec.py EG 202 396-3

# TR (Technical Report)
uv run python scripts/get_etsi_spec.py TR 103 907

# ES (ETSI Standard)
uv run python scripts/get_etsi_spec.py ES 200 381-1
```

## ETSI Document Types

ETSI publishes multiple document types, each with different purposes:

| Type | Name | Purpose |
|------|------|----------|
| EN | European Standard | Harmonized standard |
| ES | ETSI Standard | Technical specification for market implementation |
| EG | ETSI Guide | Guidance document |
| TS | Technical Specification | Technical specification |
| TR | Technical Report | Informational report |
| SR | Special Report | Temporary or specific-use document |
| GS | Group Specification | Specification from a specific group |
| GR | Group Report | Report from a specific group |
| PAS | Publicly Available Specification | Document for public use |

## Specification Numbering

ETSI specifications follow this pattern:
- **Document type**: EN, ES, EG, TS, TR, SR, GS, GR, or PAS
- **Prefix**: Series identifier (3 digits) - indicates technical area
- **Number**: Unique identifier within series (3 digits)
- **Part**: Optional component (-1, -2, -3, etc.) for multi-part standards
- **Full format**: `<doc_type> XXX YYY[-Z]`

**Common series prefixes:**
- `200`: General telephony requirements
- `103`: Speech and multimedia Transmission Quality (STQ)
- `123`: System architecture
- `128`: Security
- `133`: Protocol stack
- `202`: Network protocols

**Examples:**
- `ETSI TS 103 224`: TS type, series 103, specification 224
- `EG 202 396-3`: EG type, series 202, specification 396, part 3
- `ES 200 381-1`: ES type, series 200, specification 381, part 1

## Script Output

The script returns:
- Latest version number (e.g., V1.7.1)
- Release code (e.g., 60 for 60th revision)
- Full specification title
- Publication date
- Direct download URL for PDF
- Version history (all available versions)

**Example output for ETSI TS 103 224:**
```
======================================================================
SPECIFICATION: ETSI TS 103224
======================================================================
Latest Version:  V1.7.1
Release Code:    60
Directory:       01.07.01_60
Title:           Speech and multimedia Transmission Quality (STQ); A sound field reproduction method...
Publication Date: nov 2025
Download URL:    https://www.etsi.org/deliver/etsi_ts/103200_103299/103224/01.07.01_60/ts_103224v010701p.pdf
======================================================================

Full versions available: 7
Version history:
  - V1.7.1 (release 60) ~ 2025
  - V1.7.0 (release 59) ~ 2025
  ...
```

## How It Works

The script retrieves ETSI specification metadata through these steps:

1. **Parse specification number** from various input formats, including document type (EN/ES/EG/TS/TR/SR/GS/GR/PAS) and optional part (-1, -2, etc.)

2. **Construct delivery directory URL** using ETSI's predictable structure:
   - Pattern: `https://www.etsi.org/deliver/etsi_<type>/<prefix>00_<prefix>99/<full_spec>/`
   - Example for TS 103 224: `https://www.etsi.org/deliver/etsi_ts/103200_103299/103224/`

3. **Scrape version directories** from delivery page
   - Format: `XX.YY.ZZ_AA` (major.minor.patch_release)
   - Example: `01.07.01_60` = version 1.7.1, release 60
   - Some specs may use different formats (e.g., no release code)

4. **Identify latest version** by sorting directories
5. **Construct PDF download URL** by trying common filename patterns:
   - `<type>_<spec>v<version_no_dots>p.pdf`
   - `<type>_<spec>v<version_no_dots>.pdf`
   - `<spec>v<version_no_dots>.pdf`
   - EG specs may use `.m.pdf` extension instead of `.p.pdf`

6. **Extract metadata from PDF**:
   - Parse PDF metadata for title and creation date
   - If title missing, extract from first page content

## Limitations

1. **Spec numbering**: Not all specification numbers exist or follow expected patterns. Some specs may be:
   - Withdrawn
   - Superseded by newer versions
   - Located in different directory structures
   - Have unique numbering schemes

2. **URL variations**: ETSI delivery URLs may vary by document type and series. The script tries common patterns but may not handle all cases.

3. **Parts detection**: Multi-part standards (e.g., ES 200 381-1, -2, -3) are detected from spec number but all parts must be queried separately for complete version history.

4. **EG specifications**: EG specs sometimes use different PDF file extensions (e.g., `.m.pdf` instead of `.p.pdf`).

5. **Multi-part spec directories**: Multi-part specifications like "EG 202 396-3" may use directory naming that differs from single-part specs. The script attempts to find the correct directory by:
   - Checking if the full spec number (including part) appears in directory names
   - For single-part specs, using standard 100-number range calculation

6. **Known issue with EG 202 396-3**: This specification exists at `https://www.etsi.org/deliver/etsi_eg/202300_202399/20239603/` but the script's range detection logic may not always identify the correct directory for multi-part EG specifications. Manual verification may be required for such cases.

## Manual Retrieval Fallback

If the script fails, retrieve metadata manually:

1. **Find spec directory**: Browse to `https://www.etsi.org/deliver/etsi_<type>/`
   - Where `<type>` is `ts`, `es`, `eg`, `tr`, etc.

2. **Locate spec number** in the appropriate prefix range directory (e.g., `103000_103099/`)

3. **List version directories** (sorted alphabetically = chronological)
   - Latest version is last directory in list

4. **Download PDF** from version directory
   - Try common filename patterns

5. **Extract metadata** from PDF:
   - Title: First page or PDF metadata
   - Date: PDF creation date (`/CreationDate` field)

## Reference Documentation

For detailed ETSI standards organization and search capabilities, see:
- ETSI Search Engine: https://www.etsi.org/standards
- ETSI Document Types: https://www.etsi.org/standards/types-of-standards
- ETSI Delivery Directory: https://www.etsi.org/deliver

## Requirements

The script requires:
- Python 3.7+
- `requests` - HTTP library (installed via `uv`)
- `beautifulsoup4` - HTML parsing (install: `uv add beautifulsoup4`)
- `PyPDF2` - PDF metadata extraction (install: `uv add PyPDF2`)

Install dependencies:
```bash
uv add beautifulsoup4 PyPDF2
```
