"""The `python -m audiotextpro` entry point, with the API calls stubbed."""

from __future__ import annotations

import runpy
import sys
from typing import Any

import pytest

import audiotextpro
from audiotextpro import __main__ as entry


@pytest.fixture
def env(monkeypatch: pytest.MonkeyPatch) -> pytest.MonkeyPatch:
    monkeypatch.setattr(entry, "load_dotenv", lambda: True)
    monkeypatch.setenv("API_TOKEN", "token")
    monkeypatch.setenv("FILENAME", "call.mp3")
    return monkeypatch


def test_main_uploads_transcribes_and_saves(env: pytest.MonkeyPatch) -> None:
    steps: list[tuple[str, Any]] = []
    transcript = {"status": "completed", "text": "hi"}

    def upload_file(token: str, filename: str) -> str:
        steps.append(("upload", (token, filename)))
        return "https://cdn.example/abc"

    def create_transcript(token: str, url: str) -> dict[str, Any]:
        steps.append(("transcribe", (token, url)))
        return transcript

    def process_transcript(result: dict[str, Any]) -> str:
        steps.append(("process", result))
        return "hi"

    env.setattr(audiotextpro, "upload_file", upload_file)
    env.setattr(audiotextpro, "create_transcript", create_transcript)
    env.setattr(audiotextpro, "process_transcript", process_transcript)

    entry.main()

    assert steps == [
        ("upload", ("token", "call.mp3")),
        ("transcribe", ("token", "https://cdn.example/abc")),
        ("process", transcript),
    ]


@pytest.mark.parametrize("missing", ["API_TOKEN", "FILENAME"])
def test_main_requires_both_variables(env: pytest.MonkeyPatch, missing: str) -> None:
    env.delenv(missing)

    with pytest.raises(ValueError, match="must be set"):
        entry.main()


def test_main_stops_when_the_upload_times_out(env: pytest.MonkeyPatch) -> None:
    def create_transcript(token: str, url: str) -> dict[str, Any]:
        raise AssertionError("must not transcribe a failed upload")

    env.setattr(audiotextpro, "upload_file", lambda token, filename: None)
    env.setattr(audiotextpro, "create_transcript", create_transcript)

    with pytest.raises(RuntimeError, match="call.mp3 to AssemblyAI timed out"):
        entry.main()


def test_running_the_module_calls_main(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("API_TOKEN", raising=False)
    monkeypatch.delenv("FILENAME", raising=False)
    monkeypatch.setattr("dotenv.load_dotenv", lambda: True)
    # runpy re-executes the module; drop the copy imported above so it runs fresh.
    monkeypatch.delitem(sys.modules, "audiotextpro.__main__", raising=False)

    with pytest.raises(ValueError, match="must be set"):
        runpy.run_module("audiotextpro", run_name="__main__")
