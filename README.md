# Mini Web Scanner

A Python 3.11+ project for a modular web security scanner. Version 3.0.0 is under development. The current codebase provides foundational scan and finding models plus validated scanner configuration; the scanning engine and user interface are not implemented yet.

## Current status

Implemented in `src/webscanner/`:

- `Scan` and `ScanStatus` model a scan, its lifecycle timestamps, and findings.
- `Finding` and `Severity` represent a security finding and its severity.
- `ScannerConfig` stores scanner settings and validates timeout, redirect, delay, and request-count limits.

The legacy `scanner.py` script belongs to the earlier version and is separate from the 3.0.0 package.

## Requirements

- Python 3.11 or newer

## Install for development

```bash
python -m venv .venv
# Activate the virtual environment, then:
python -m pip install -e ".[dev]"
```

## Tests

```bash
python -m pytest
```

The current tests cover model behavior and configuration validation. They do not yet exercise HTTP scanning, report generation, or a CLI.

## Project layout

```text
src/webscanner/
  core/config.py
  models/finding.py
  models/scan.py
tests/
  test_models.py
```

## License

GNU GPL v3. See [LICENSE](LICENSE).
