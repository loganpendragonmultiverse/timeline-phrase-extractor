import json
from pathlib import Path

import pytest

from timeline_phrase_extractor.cli import main
from timeline_phrase_extractor.core import PROJECT, analyze, render_json, render_markdown


def test_representative_sample_has_expected_result():
    data = json.loads(
        (Path(__file__).parents[1] / "examples" / "sample.json").read_text(encoding="utf-8")
    )
    report = analyze(data)
    assert report["version"] == 1
    assert report["project"] == PROJECT
    assert [item["kind"] for item in report["phrases"]] == ["duration", "date", "relative"]
    assert report["by_kind"] == {"duration": 1, "date": 1, "relative": 1}
    assert report["phrases"][0]["section"] == "(document)"
    assert f'"project": "{PROJECT}"' in render_json(report)
    assert PROJECT.replace("-", " ").title() in render_markdown(report)


def test_missing_required_input_is_rejected():
    with pytest.raises(ValueError):
        analyze({})


def test_calendar_dates_clock_times_sections_and_context():
    report = analyze(
        {"text": "# Departure\nMeet on March 4, 2027 at 08:30.\n## Return\nBack 2 days later."}
    )
    assert [item["kind"] for item in report["phrases"]] == ["date", "clock_time", "duration"]
    assert report["phrases"][0]["section"] == "Departure"
    assert report["phrases"][2]["section"] == "Return"
    assert report["phrases"][0]["context"].startswith("Meet on")


def test_cli_json_and_output_safety(tmp_path, capsys):
    source = Path(__file__).parents[1] / "examples" / "sample.json"
    assert main([str(source), "--format", "json"]) == 0
    assert json.loads(capsys.readouterr().out)["project"] == PROJECT
    output = tmp_path / "report.md"
    output.write_text("keep", encoding="utf-8")
    assert main([str(source), "--output", str(output)]) == 2
