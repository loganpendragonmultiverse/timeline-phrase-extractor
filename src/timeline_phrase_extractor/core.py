from __future__ import annotations

import json
import re
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
        "date": "\\b(?:in\\s+)?(?:1[5-9]\\d{2}|20\\d{2})\\b",
    }
    phrases = []
    for kind, pattern in patterns.items():
        for match in re.finditer(pattern, text, re.IGNORECASE):
            phrases.append(
                {
                    "kind": kind,
                    "phrase": match.group(0),
                    "offset": match.start(),
                    "line": text.count("\n", 0, match.start()) + 1,
                }
            )
    phrases.sort(key=lambda item: item["offset"])
    return {"count": len(phrases), "phrases": phrases}


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
