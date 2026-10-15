import pytest

from timeline_phrase_extractor.core import analyze


def test_literals_unicode_case_overlap_order_duplicates():
    report = analyze(
        {"text": "# Era\nÉON+ [day] ababa Éon+", "glossary": ["Éon+", "[day]", "aba", "ÉON+"]}
    )
    assert [p["phrase"] for p in report["phrases"]] == ["ÉON+", "[day]", "aba", "aba", "Éon+"]
    assert [p["offset"] for p in report["phrases"]] == sorted(
        p["offset"] for p in report["phrases"]
    )
    assert report["by_kind"] == {"authored": 5}
    assert all(p["section"] == "Era" for p in report["phrases"])


def test_builtin_overlap_and_legacy():
    base = analyze({"text": "March 4 then Moonday"})
    report = analyze({"text": "March 4 then Moonday", "glossary": ["March", "March 4"]})
    assert [p["kind"] for p in report["phrases"]] == ["date", "authored", "authored"]
    assert analyze({"text": "March 4 then Moonday", "glossary": []}) == base


@pytest.mark.parametrize("value", [None, {}, "day", [""], ["  "], [1]])
def test_invalid_glossary(value):
    with pytest.raises(ValueError, match="glossary"):
        analyze({"text": "day", "glossary": value})
