"""Saving and printing a completed transcript."""

import json
from pathlib import Path

import pytest

from audiotextpro.transcript_processor import process_transcript


def test_prints_the_text_saves_the_json_and_returns_the_text(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.chdir(tmp_path)
    transcript = {"id": "tr_1", "text": "Hello there.", "confidence": 0.93}

    assert process_transcript(transcript) == "Hello there."
    assert capsys.readouterr().out == "Hello there.\n"
    assert json.loads((tmp_path / "transcript.json").read_text()) == transcript


def test_missing_text_raises_before_writing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)

    with pytest.raises(KeyError):
        process_transcript({"id": "tr_1"})
    assert not (tmp_path / "transcript.json").exists()
