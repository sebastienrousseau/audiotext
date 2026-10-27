import json


def process_transcript(transcript):
    """Print text to console and save JSON to file.

    Args:
        transcript (dict): Completed AssemblyAI transcript object

    Returns:
        str: The extracted text from the transcript.
    """

    transcript_text = transcript['text']
    print(transcript_text)

    with open('transcript.json', 'w', encoding='utf-8') as f:
        json.dump(transcript, f, indent=4)

    return transcript_text
