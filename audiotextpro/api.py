"""
This module provides functions to interact with the AssemblyAI API.
It includes functionality to upload audio files and retrieve transcriptions.
"""

import time
from typing import Any

import requests

from .file import read_file


def upload_file(api_token: str, file_path: str, timeout: float = 30) -> str | None:
    """Upload a file to the AssemblyAI API.

    Args:
        api_token (str): Your API token for AssemblyAI.
        file_path (str): Path to the local file.
        timeout (int, optional): Timeout for the request in seconds.

    Returns:
        str | None: The upload URL, or None when the request timed out.
    """

    headers = {"authorization": api_token}

    try:
        response = requests.post(
            "https://api.assemblyai.com/v2/upload",
            headers=headers,
            data=read_file(file_path),
            timeout=timeout,
        )
        upload_url: str = response.json()["upload_url"]
        return upload_url
    except requests.Timeout:
        print("Request timed out")
        return None


def create_transcript(
    api_token: str, audio_url: str, timeout: float = 30
) -> dict[str, Any]:
    """Create a transcript using AssemblyAI API.

    Args:
        api_token (str): Your API token for AssemblyAI.
        audio_url (str): URL of the audio file to be transcribed.
        timeout (int, optional): Timeout for requests in seconds.

    Returns:
        dict: Completed transcript object.
    """

    headers = {"authorization": api_token, "content-type": "application/json"}

    data = {"audio_url": audio_url}

    start_time = time.time()

    # Make request
    request_end_time = time.time()

    response = requests.post(
        "https://api.assemblyai.com/v2/transcript",
        json=data,
        headers=headers,
        timeout=timeout,
    )
    request_end_time = time.time()

    print(f"Request time: {request_end_time - start_time:.2f} secs")

    transcript_id = response.json()["id"]

    polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

    while True:
        result: dict[str, Any] = requests.get(
            polling_endpoint, headers=headers, timeout=timeout
        ).json()
        if result["status"] == "completed":
            end_time = time.time()
            break
        if result["status"] == "error":
            raise ValueError(f"Transcript failed: {result['error']}")
        time.sleep(5)

    print(f"Response time: {end_time - request_end_time:.2f} secs")
    print(f"Confidence: {result['confidence']:.2%}")

    return result
