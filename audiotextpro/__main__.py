"""
This module serves as the main entry point for utilizing the AssemblyAI transcription service.

The script performs the following operations sequentially:
1. Uploads an audio file to AssemblyAI.
2. Requests a transcript of the uploaded audio file.
3. Processes and saves the resulting transcript.

Example usage:
    Ensure that API_TOKEN and FILENAME are set correctly, then run:
    $ python main.py

Note: Sensitive information like API tokens should typically be stored securely
and not hard-coded into scripts.
"""

# Importing the assemblyai package, which provides functions for interacting
# with the AssemblyAI API and processing transcription results.
import os

# Importing the dotenv package, which allows us to load environment variables
from dotenv import load_dotenv

import audiotextpro

# Ensuring the script is being run as the main module.
# This prevents the code inside this condition from running when this module is imported elsewhere.
if __name__ == "__main__":
    load_dotenv()

    API_TOKEN = os.getenv("API_TOKEN")
    FILENAME = os.getenv("FILENAME")

    if not API_TOKEN or not FILENAME:
        raise ValueError("API_TOKEN and FILENAME environment variables must be set.")

    # Uploading the audio file specified by FILENAME to AssemblyAI, and retrieving
    # the URL where the uploaded audio file can be accessed.
    upload_url = audiotextpro.upload_file(API_TOKEN, FILENAME)

    # Requesting a transcription of the uploaded audio file from AssemblyAI.
    # The function will poll AssemblyAI periodically until the transcription is ready.
    transcript = audiotextpro.create_transcript(API_TOKEN, upload_url)

    # Processing the resulting transcript: printing the transcription to the console
    # and saving the full transcript data as a JSON file.
    text = audiotextpro.process_transcript(transcript)
