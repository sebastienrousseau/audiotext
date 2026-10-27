"""Chunked file reading, in both copies of read_file."""

from collections.abc import Callable, Iterator
from pathlib import Path

import pytest

from audiotextpro import file, utils

READERS = [file.read_file, utils.read_file]


@pytest.mark.parametrize("read_file", READERS)
def test_yields_the_file_in_chunks(
    read_file: Callable[..., Iterator[bytes]], tmp_path: Path
) -> None:
    path = tmp_path / "audio.bin"
    path.write_bytes(b"abcdefghij")

    assert list(read_file(str(path), chunk_size=4)) == [b"abcd", b"efgh", b"ij"]


@pytest.mark.parametrize("read_file", READERS)
def test_default_chunk_reads_a_small_file_whole(
    read_file: Callable[..., Iterator[bytes]], tmp_path: Path
) -> None:
    path = tmp_path / "audio.bin"
    path.write_bytes(b"x" * 1000)

    assert list(read_file(str(path))) == [b"x" * 1000]


@pytest.mark.parametrize("read_file", READERS)
def test_empty_file_yields_nothing(
    read_file: Callable[..., Iterator[bytes]], tmp_path: Path
) -> None:
    path = tmp_path / "empty.bin"
    path.write_bytes(b"")

    assert list(read_file(str(path))) == []


@pytest.mark.parametrize("read_file", READERS)
def test_missing_file_raises(
    read_file: Callable[..., Iterator[bytes]], tmp_path: Path
) -> None:
    with pytest.raises(FileNotFoundError):
        list(read_file(str(tmp_path / "missing.bin")))
