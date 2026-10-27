"""The AssemblyAI calls, with requests and the clock replaced at the boundary."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import pytest
import requests

from audiotextpro import api


class FakeResponse:
    def __init__(self, payload: dict[str, Any]) -> None:
        self.payload = payload

    def json(self) -> dict[str, Any]:
        return self.payload


@pytest.fixture
def audio(tmp_path: Path) -> str:
    path = tmp_path / "call.mp3"
    path.write_bytes(b"ID3audio")
    return str(path)


def test_upload_file_posts_the_audio_and_returns_the_url(
    monkeypatch: pytest.MonkeyPatch, audio: str
) -> None:
    calls: list[dict[str, Any]] = []

    def post(url: str, **kwargs: Any) -> FakeResponse:
        calls.append({"url": url, **kwargs, "body": b"".join(kwargs["data"])})
        return FakeResponse({"upload_url": "https://cdn.example/abc"})

    monkeypatch.setattr(requests, "post", post)

    assert api.upload_file("token", audio, timeout=7) == "https://cdn.example/abc"
    assert calls == [
        {
            "url": "https://api.assemblyai.com/v2/upload",
            "headers": {"authorization": "token"},
            "data": calls[0]["data"],
            "timeout": 7,
            "body": b"ID3audio",
        }
    ]


def test_upload_file_returns_none_on_timeout(
    monkeypatch: pytest.MonkeyPatch, audio: str, capsys: pytest.CaptureFixture[str]
) -> None:
    def post(url: str, **kwargs: Any) -> FakeResponse:
        raise requests.Timeout

    monkeypatch.setattr(requests, "post", post)

    assert api.upload_file("token", audio) is None
    assert "Request timed out" in capsys.readouterr().out


@pytest.fixture
def no_sleep(monkeypatch: pytest.MonkeyPatch) -> list[float]:
    sleeps: list[float] = []
    monkeypatch.setattr(time, "sleep", sleeps.append)
    return sleeps


def stub_transcript_api(
    monkeypatch: pytest.MonkeyPatch, polls: list[dict[str, Any]]
) -> list[tuple[str, dict[str, Any]]]:
    seen: list[tuple[str, dict[str, Any]]] = []

    def post(url: str, **kwargs: Any) -> FakeResponse:
        seen.append((url, kwargs))
        return FakeResponse({"id": "tr_1"})

    def get(url: str, **kwargs: Any) -> FakeResponse:
        seen.append((url, kwargs))
        return FakeResponse(polls.pop(0))

    monkeypatch.setattr(requests, "post", post)
    monkeypatch.setattr(requests, "get", get)
    return seen


def test_create_transcript_polls_until_completed(
    monkeypatch: pytest.MonkeyPatch,
    no_sleep: list[float],
    capsys: pytest.CaptureFixture[str],
) -> None:
    done = {"status": "completed", "text": "hello", "confidence": 0.9}
    seen = stub_transcript_api(
        monkeypatch, [{"status": "queued"}, {"status": "processing"}, done]
    )

    assert api.create_transcript("token", "https://cdn.example/abc", timeout=9) == done

    post_url, post_kwargs = seen[0]
    assert post_url == "https://api.assemblyai.com/v2/transcript"
    assert post_kwargs["json"] == {"audio_url": "https://cdn.example/abc"}
    assert post_kwargs["headers"] == {
        "authorization": "token",
        "content-type": "application/json",
    }
    assert post_kwargs["timeout"] == 9
    assert [url for url, _ in seen[1:]] == [
        "https://api.assemblyai.com/v2/transcript/tr_1"
    ] * 3
    assert no_sleep == [5, 5]
    assert "Confidence: 90.00%" in capsys.readouterr().out


def test_create_transcript_raises_on_error_status(
    monkeypatch: pytest.MonkeyPatch, no_sleep: list[float]
) -> None:
    stub_transcript_api(
        monkeypatch, [{"status": "processing"}, {"status": "error", "error": "bad"}]
    )

    with pytest.raises(ValueError, match="Transcript failed: bad"):
        api.create_transcript("token", "https://cdn.example/abc")
    assert no_sleep == [5]
