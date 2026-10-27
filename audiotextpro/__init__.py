"""
This module provides a convenient import interface for the assemblyai package.

The module exposes the core functionalities from the `api`, `utils`, and
`transcript_processor` modules, allowing them to be accessed directly from the
`assemblyai` package level. This provides a simplified API for users of the package.

Example usage:
    import assemblyai
    upload_url = assemblyai.upload_file(API_TOKEN, FILENAME)
"""

# Importing the `upload_file` and `create_transcript` functions from the `api` module.
# These functions facilitate direct interaction with the AssemblyAI API,
# such as uploading audio files and requesting transcripts.
from .api import create_transcript, upload_file

# Importing the `process_transcript` function from the `transcript_processor` module.
# This function processes the obtained transcript data from the AssemblyAI API,
# printing the transcription to the console and saving it as a JSON file.
from .transcript_processor import process_transcript

# Importing the `read_file` function from the `utils` module.
# This function is a utility that allows reading a file in chunks and can
# be used in various contexts where large files need to be read efficiently.
from .utils import read_file

__all__ = ["create_transcript", "process_transcript", "read_file", "upload_file"]
