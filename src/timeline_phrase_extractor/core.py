from __future__ import annotations

import json
import re
from collections import Counter
from typing import Any

PROJECT = "timeline-phrase-extractor"


def _require(data: dict[str, Any], key: str) -> Any:
    value = data.get(key)
    if value is None or value == "" or value == []:
        raise ValueError(f"{key} is required")
    return value


def _timeline(data: dict[str, Any]) -> dict[str, Any]:
    text = str(_require(data, "text"))
    patterns = {
        "duration": "\\b(?:one|two|three|four|five|six|seven|eight|nine|ten|\\d+)\\s+(?:minutes?|hours?|days?|weeks?|months?|years?)\\s+(?:later|earlier|before|after)\\b",
        "relative": "\\b(?:the\\s+)?(?:next|previous|following|prior)\\s+(?:morning|evening|night|day|week|month|year)\\b",
        "date": r"\b(?:\d{4}-\d{2}-\d{2}|(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sept?(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2}(?:,\s*\d{4})?|(?:in\s+)?(?:1[5-9]\d{2}|20\d{2}))\b",
        "clock_time": r"\b(?:[01]?\d|2[0-3]):[0-5]\d(?:\s*(?:a\.m\.|p\.m\.|am|pm))?\b",
    }
    glossary = data.get("glossary", [])
    if not isinstance(glossary, list) or any(
        not isinstance(phrase, str) or not phrase.strip() for phrase in glossary
    ):
        raise ValueError("glossary must be an array of nonempty literal phrases")
    source_lines = text.splitlines()
    headings: list[tuple[int, str]] = [(1, "(document)")]
    for line_number, line_text in enumerate(source_lines, start=1):
        heading = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", line_text)
        if heading:
            headings.append((line_number, heading.group(1)))
    phrases: list[dict[str, int | str]] = []
    for kind, pattern in patterns.items():
        for match in re.finditer(pattern, text, re.IGNORECASE):
            line = text.count("\n", 0, match.start()) + 1
            section = next(name for start, name in reversed(headings) if start <= line)
            phrases.append(
                {
                    "kind": kind,
                    "phrase": match.group(0),
                    "offset": match.start(),
                    "line": line,
                    "section": section,
                    "context": source_lines[line - 1].strip() if source_lines else "",
                }
            )
    # Lookahead retains overlapping literal occurrences. re.escape prevents regex syntax.
    seen: set[tuple[int, int]] = set()
    for phrase in glossary:
        for match in re.finditer("(?=(" + re.escape(phrase) + "))", text, re.IGNORECASE):
            span = (match.start(), match.start() + len(match.group(1)))
            if span in seen:
                continue
            seen.add(span)
            line = text.count("\n", 0, match.start()) + 1
            phrases.append(
                {
                    "kind": "authored",
                    "phrase": match.group(1),
                    "offset": match.start(),
                    "line": line,
                    "section": next(name for start, name in reversed(headings) if start <= line),
                    "context": source_lines[line - 1].strip(),
                }
            )
    phrases.sort(key=lambda item: int(item["offset"]))
    return {
        "count": len(phrases),
        "by_kind": dict(Counter(str(item["kind"]) for item in phrases)),
        "phrases": phrases,
    }


def analyze(data: dict[str, Any]) -> dict[str, Any]:
    return {"version": 1, "project": PROJECT, **_timeline(data)}


def render_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False) + "\n"


def render_markdown(report: dict[str, Any]) -> str:
    lines = [f"# {report['project'].replace('-', ' ').title()} report", ""]
    for key, value in report.items():
        if key not in {"version", "project"}:
            lines.append(f"## {key.replace('_', ' ').title()}")
            lines.append("")
            lines.append(f"```json\n{json.dumps(value, indent=2, ensure_ascii=False)}\n```")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"
