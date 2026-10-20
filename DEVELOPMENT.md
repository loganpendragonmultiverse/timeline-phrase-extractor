# Development contract

Extract dated, duration, and relative-time phrases into an ordered manuscript review list.

Version 1.1 adds month-name/ISO dates, clock times, Markdown sections, line context, and per-kind totals without claiming chronology.

Preserve deterministic, source-safe behavior and the interpretation boundary documented in the README. Every feature release must update tests, version metadata, `CHANGELOG.md`, README claims and limitations, repository metadata, release assets, and the Forge catalog together.

## 1.2.0

Optional `glossary` is an array of literal phrases, for example `["Third Frost", "Moon+1"]`. Matches use Unicode-aware case-insensitive regex literal matching (no regex syntax, normalization, or full casefold expansion). Overlapping occurrences and built-in overlaps are retained; duplicate authored matches at the same span are emitted once. Results stay in source-offset order, with built-ins then glossary order for ties, and kind `authored`. No calendar arithmetic or chronology is inferred.

## Version 1.3.0: precise source evidence

Each phrase includes `offset` and exclusive `end_offset` in Python Unicode code points,
plus one-based `line` and `column`. CRLF, CR and LF are line boundaries; other Unicode
separators remain source characters. Slicing the original text at the offsets reproduces
the matched phrase. The input must be a JSON object with string `text`; an empty string
produces an empty report. Reports use exclusive output creation and safely fenced Markdown.
No date validation, chronology resolution or calendar arithmetic is inferred.

## 1.3.1 distribution acceptance

Install both actual tagged distributions into separate virtual environments outside the
source tree. Require all four operating documents and the sample under
`share/doc/timeline-phrase-extractor`, compare them byte-for-byte with the tag, run the
installed sample from another directory, and run the full suite against installed imports.
Do not substitute checkout-relative samples for bundled examples in this acceptance.
