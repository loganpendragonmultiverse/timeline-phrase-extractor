import pytest

from timeline_phrase_extractor.cli import main
from timeline_phrase_extractor.core import analyze, render_markdown


@pytest.mark.parametrize("value", [None, [], "text", 3, True])
def test_root_requires_object(value):
    with pytest.raises(TypeError, match="object"):
        analyze(value)


@pytest.mark.parametrize("value", [None, [], {}, 3, True])
def test_text_requires_string(value):
    with pytest.raises(TypeError, match="string"):
        analyze({"text": value})


def test_empty_manuscript_is_valid():
    assert analyze({"text": ""})["phrases"] == []


@pytest.mark.parametrize("newline", ["\n", "\r\n", "\r", "\u2028"])
def test_exact_coordinates_preserve_original_text(newline):
    text = "# Heading" + newline + "Éon next day" + newline + "Third Frost"
    report = analyze({"text": text, "glossary": ["Third Frost"]})
    for phrase in report["phrases"]:
        assert text[phrase["offset"] : phrase["end_offset"]] == phrase["phrase"]
    expected_line = 1 if newline == "\u2028" else 2
    assert report["phrases"][0]["line"] == expected_line
    assert report["phrases"][0]["column"] == (
        len("# Heading" + newline) + 5 if expected_line == 1 else 5
    )
    assert report["phrases"][1]["line"] == (1 if newline == "\u2028" else 3)


def test_markdown_uses_fence_longer_than_source_backticks():
    report = analyze({"text": "``` next day ````"})
    markdown = render_markdown(report)
    assert "`````json" in markdown
    assert markdown.count("`````json") == 1


def test_cli_rejects_nonobject_and_preserves_existing_output(tmp_path, capsys):
    source = tmp_path / "input.json"
    source.write_text("[]", encoding="utf-8")
    assert main([str(source)]) == 2
    assert "object" in capsys.readouterr().err
    source.write_text('{"text": "next day"}', encoding="utf-8")
    output = tmp_path / "report.md"
    output.write_text("keep", encoding="utf-8")
    assert main([str(source), "--output", str(output)]) == 2
    assert output.read_text() == "keep"


def test_cli_refuses_dangling_output_symlink(tmp_path, capsys):
    source = tmp_path / "input.json"
    source.write_text('{"text": "next day"}', encoding="utf-8")
    missing = tmp_path / "missing-target"
    output = tmp_path / "report.md"
    try:
        output.symlink_to(missing)
    except OSError as exc:
        pytest.skip(f"symlink creation unavailable: {exc}")
    assert main([str(source), "--output", str(output)]) == 2
    assert "symbolic link" in capsys.readouterr().err
    assert output.is_symlink()
    assert not missing.exists()
