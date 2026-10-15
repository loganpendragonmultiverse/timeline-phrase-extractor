# Testing

Run `python -m pip install -e ".[dev]"`, `ruff format --check .`, `ruff check .`, `mypy src`, `pytest`, and `python -m build`.

## 1.2.0 acceptance

Exercise the optional input with the full regression suite, including validation, inclusive boundaries, deterministic ordering and legacy default behavior. Optional `glossary` is an array of literal phrases, for example `["Third Frost", "Moon+1"]`. Matches use Unicode-aware case-insensitive regex literal matching (no regex syntax, normalization, or full casefold expansion). Overlapping occurrences and built-in overlaps are retained; duplicate authored matches at the same span are emitted once. Results stay in source-offset order, with built-ins then glossary order for ties, and kind `authored`. No calendar arithmetic or chronology is inferred.
