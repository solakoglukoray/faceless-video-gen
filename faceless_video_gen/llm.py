"""LLM client for video script generation.

Supports OpenAI-compatible endpoints including Ollama.
Set OPENAI_BASE_URL=http://localhost:11434/v1 and LLM_MODEL=llama3
to run fully offline with Ollama.
"""

import os

from openai import OpenAI

from faceless_video_gen.prompts import SCRIPT_PROMPT


def generate_script(topic: str, duration_seconds: int = 60) -> str:
    """Generate a spoken video script for the given topic and target duration."""
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY", "ollama"),
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    )
    model = os.getenv("LLM_MODEL", "gpt-4o-mini")
    words = int(duration_seconds * 150 / 60)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional YouTube scriptwriter. "
                    "You write engaging, conversational scripts optimised for "
                    "text-to-speech narration."
                ),
            },
            {
                "role": "user",
                "content": SCRIPT_PROMPT.format(
                    topic=topic,
                    duration=duration_seconds,
                    words=words,
                ),
            },
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content or ""
