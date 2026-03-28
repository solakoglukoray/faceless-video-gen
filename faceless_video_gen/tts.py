"""Text-to-speech via edge-tts (Microsoft Neural voices, free, offline-capable)."""

import asyncio

import edge_tts


async def _synthesise(text: str, voice: str, output_path: str) -> None:
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)


def generate_audio(
    text: str,
    voice: str = "en-US-AriaNeural",
    output_path: str = "audio.mp3",
) -> str:
    """Convert text to an MP3 file and return its path."""
    asyncio.run(_synthesise(text, voice, output_path))
    return output_path


AVAILABLE_VOICES = [
    "en-US-AriaNeural",
    "en-US-GuyNeural",
    "en-GB-SoniaNeural",
    "en-AU-NatashaNeural",
    "en-CA-ClaraNeural",
]
