# Timeline Phrase Extractor

[![CI](https://github.com/loganpendragonmultiverse/timeline-phrase-extractor/actions/workflows/ci.yml/badge.svg)](https://github.com/loganpendragonmultiverse/timeline-phrase-extractor/actions/workflows/ci.yml)

Extract dated, duration, and relative-time phrases into an ordered manuscript review list. The command runs locally, uses explicit UTF-8 JSON input, and produces deterministic JSON or Markdown reports without modifying the supplied source material.

## Three-minute start

```bash
python -m pip install .
timeline-phrases examples/sample.json
timeline-phrases examples/sample.json --format json --output report.json
```

The example documents the complete input shape. Version 1.1 recognizes month-name and ISO dates plus 24-hour clock times, and adds source-line context, Markdown-section names, and per-kind totals. Markdown is intended for immediate review; JSON preserves structured evidence for scripts and later comparison. An existing output file is never overwritten.

## Privacy and platforms

All manuscript text stays local.

Python 3.10 or newer is supported on Windows, macOS, and Linux. The package has no runtime dependencies, telemetry, account, or hosted service.

## Interpretation boundary

Regex matches are review prompts. The tool preserves document order and does not resolve fictional calendars, ambiguous references, or chronology.

## Development

```bash
python -m pip install -e ".[dev]"
ruff format --check .
ruff check .
mypy src
pytest
python -m build
```

The project is feature-complete for its documented v1 scope. Maintenance focuses on correctness, security, compatibility, and well-supported input improvements.

Part of the [Logan Pendragon Forge open-source collection](https://www.loganpendragonforge.com/open-source/). Licensed under the [MIT License](LICENSE).

## Version 1.2.0

Optional `glossary` is an array of literal phrases, for example `["Third Frost", "Moon+1"]`. Matches use Unicode-aware case-insensitive regex literal matching (no regex syntax, normalization, or full casefold expansion). Overlapping occurrences and built-in overlaps are retained; duplicate authored matches at the same span are emitted once. Results stay in source-offset order, with built-ins then glossary order for ties, and kind `authored`. No calendar arithmetic or chronology is inferred.

## Version 1.2.1: documentation correction

Version 1.2.0 was released on October 15, 2026. Version 1.2.1 corrects its release labels without changing behavior. The original v1.2.0 tag and downloadable artifacts remain unchanged; use v1.2.1 for the corrected packaged documentation.

## Version 1.3.0: precise source evidence

Each phrase includes `offset` and exclusive `end_offset` in Python Unicode code points,
plus one-based `line` and `column`. CRLF, CR and LF are line boundaries; other Unicode
separators remain source characters. Slicing the original text at the offsets reproduces
the matched phrase. The input must be a JSON object with string `text`; an empty string
produces an empty report. Reports use exclusive output creation and safely fenced Markdown.
No date validation, chronology resolution or calendar arithmetic is inferred.
