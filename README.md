# faceless-video-gen

[![CI](https://github.com/solakoglukoray/faceless-video-gen/actions/workflows/ci.yml/badge.svg)](https://github.com/solakoglukoray/faceless-video-gen/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Turn any topic into a faceless YouTube video — LLM-written script, neural voiceover, and image slideshow — with a single terminal command.

Content creators spend hours scripting, recording, and editing faceless YouTube videos.
This tool does it in under two minutes: you give it a topic, it writes the script, speaks it with a neural voice, fetches matching visuals, and assembles an MP4 ready to upload.

## Features

- **LLM scripting** — generates a structured, TTS-optimised script via any OpenAI-compatible endpoint (GPT, Ollama, etc.)
- **Neural voiceover** — converts the script to speech with `edge-tts` (Microsoft Neural voices, free, no API key)
- **Auto visuals** — fetches landscape images from Unsplash (or falls back to picsum.photos — no signup required)
- **One-command output** — assembles everything into an MP4 with MoviePy
- **Fully offline option** — pair with Ollama to run with zero paid API calls

## Installation

```bash
pip install faceless-video-gen
```

Requires `ffmpeg` on your system:

```bash
# macOS
brew install ffmpeg

# Ubuntu / Debian
sudo apt install ffmpeg
```

Or with Docker (ffmpeg included):

```bash
docker run --rm -v $(pwd):/output \
  -e OPENAI_API_KEY=your_key \
  ghcr.io/solakoglukoray/faceless-video-gen \
  "5 Python tricks that changed how I code" --output /output/video.mp4
```

## Usage

```bash
# Set your LLM key (or use Ollama — see .env.example)
export OPENAI_API_KEY=your_key

# Generate a 60-second video
faceless-video-gen "5 Python tricks that changed how I code"

# Custom voice, duration, and output path
faceless-video-gen "passive income ideas" \
  --voice en-GB-SoniaNeural \
  --duration 90 \
  --output passive_income.mp4

# List available voices
faceless-video-gen voices
```

### Offline with Ollama

```bash
export OPENAI_BASE_URL=http://localhost:11434/v1
export OPENAI_API_KEY=ollama
export LLM_MODEL=llama3

faceless-video-gen "why sleep is your superpower"
```

## Configuration

Copy `.env.example` to `.env` and fill in your values:

| Variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | `ollama` | OpenAI key (or `ollama` for local) |
| `OPENAI_BASE_URL` | OpenAI API | Override for Ollama or other endpoints |
| `LLM_MODEL` | `gpt-4o-mini` | Model name |
| `UNSPLASH_ACCESS_KEY` | *(unset)* | Optional. Without it, picsum.photos is used |

## Development

```bash
git clone https://github.com/solakoglukoray/faceless-video-gen
cd faceless-video-gen
pip install -e ".[dev]"
pytest
ruff check .
```

## Contributing

PRs welcome. Run `ruff check .` and `pytest` before submitting.

## License

MIT
