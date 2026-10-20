# Changelog

## 1.3.0 - 2026-10-20

- Add exclusive end offsets and one-based columns to every phrase for precise source review.
- Reject non-object inputs and non-string manuscript text; allow empty manuscripts.
- Keep line context and coordinates consistent across LF, CRLF and CR files.
- Fence Markdown evidence safely when source text contains backticks, and create reports exclusively.

## 1.2.1

- Correct released documentation labels; package behavior is unchanged.
- Preserve the original v1.2.0 tags and artifacts. This patch supplies corrected documentation in new artifacts.

## 1.2.0 - 2026-10-15

- Optional `glossary` is an array of literal phrases, for example `["Third Frost", "Moon+1"]`.

## 1.1.0 - 2026-07-27

- Added month-name and ISO dates plus 24-hour clock-time detection.
- Added Markdown-section names, source-line context, and per-kind totals.

## 1.0.0 - 2026-07-26

- Released the first complete Timeline Phrase Extractor command-line workflow.
- Added deterministic JSON and Markdown reporting, representative examples, and cross-platform tests.
