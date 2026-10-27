import json
from typing import Any


def process_transcript(transcript: dict[str, Any]) -> str:
    """Print text to console and save JSON to file.

    Args:
        transcript (dict): Completed AssemblyAI transcript object

    Returns:
        str: The extracted text from the transcript.
    """

    transcript_text: str = transcript["text"]
    print(transcript_text)

    with open("transcript.json", "w", encoding="utf-8") as f:
        json.dump(transcript, f, indent=4)

    return transcript_text
