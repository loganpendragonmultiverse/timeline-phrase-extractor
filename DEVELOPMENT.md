# Development contract

Extract dated, duration, and relative-time phrases into an ordered manuscript review list.

Version 1.1 adds month-name/ISO dates, clock times, Markdown sections, line context, and per-kind totals without claiming chronology.

Preserve deterministic, source-safe behavior and the interpretation boundary documented in the README. Every feature release must update tests, version metadata, `CHANGELOG.md`, README claims and limitations, repository metadata, release assets, and the Forge catalog together.

## 1.2.0 candidate

Optional `glossary` is an array of literal phrases, for example `["Third Frost", "Moon+1"]`. Matches use Unicode-aware case-insensitive regex literal matching (no regex syntax, normalization, or full casefold expansion). Overlapping occurrences and built-in overlaps are retained; duplicate authored matches at the same span are emitted once. Results stay in source-offset order, with built-ins then glossary order for ties, and kind `authored`. No calendar arithmetic or chronology is inferred.
