"""
AudioTextPro audio transcription module.

This module contains functions for uploading audio files to AssemblyAI, and
polling for the transcription results.

"""


def read_file(file_to_read, chunk_size=5242880):
    """Generator function to read a file in chunks.

    Args:
        file_to_read (str): Path to the file to read.
        chunk_size (int, optional): Size of chunks to read in bytes.
        Defaults to 5 MB.

    Yields:
        bytes: Chunks of file contents.
    """

    with open(file_to_read, "rb") as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data
