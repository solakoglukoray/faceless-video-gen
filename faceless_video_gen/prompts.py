"""Prompt templates for script generation."""

SCRIPT_PROMPT = """\
Write a {duration}-second YouTube script about "{topic}".

Target roughly {words} words (at 150 wpm for {duration} seconds).

Structure:
1. Hook (first 5 seconds): one punchy, attention-grabbing sentence.
2. Body: 3-5 key points with smooth transitions.
3. Call to action: ask the viewer to like and subscribe.

Rules:
- Conversational tone, no jargon.
- No stage directions, timestamps, or section labels — spoken words only.
- Do not introduce yourself or say "Welcome back."
""".strip()
