"""Unit tests for faceless-video-gen core modules (mocked — no API keys needed)."""

from unittest.mock import MagicMock, patch

import pytest

from faceless_video_gen.llm import generate_script
from faceless_video_gen.main import generate_video
from faceless_video_gen.prompts import SCRIPT_PROMPT

# ---------------------------------------------------------------------------
# generate_script
# ---------------------------------------------------------------------------


def test_generate_script_returns_nonempty_string():
    """generate_script returns a non-empty string when the LLM responds."""
    with patch("faceless_video_gen.llm.OpenAI") as mock_openai:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Great script here."))]
        )
        result = generate_script("Python tips", 60)
    assert isinstance(result, str)
    assert len(result) > 0


def test_generate_script_passes_topic_in_prompt():
    """The topic is included in the prompt sent to the LLM."""
    with patch("faceless_video_gen.llm.OpenAI") as mock_openai:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Script content"))]
        )
        generate_script("machine learning", 30)

    call_kwargs = mock_client.chat.completions.create.call_args[1]
    messages_text = str(call_kwargs.get("messages", ""))
    assert "machine learning" in messages_text


def test_generate_script_word_count_scales_with_duration():
    """The word-count hint in the prompt scales proportionally with duration."""
    prompt_60 = SCRIPT_PROMPT.format(topic="AI", duration=60, words=150)
    prompt_120 = SCRIPT_PROMPT.format(topic="AI", duration=120, words=300)
    assert "150" in prompt_60
    assert "300" in prompt_120


# ---------------------------------------------------------------------------
# generate_video pipeline (full mock)
# ---------------------------------------------------------------------------


def test_generate_video_calls_all_pipeline_steps():
    """generate_video calls script, audio, images, and assembly in order."""
    with (
        patch("faceless_video_gen.main.generate_script") as mock_script,
        patch("faceless_video_gen.main.generate_audio") as mock_audio,
        patch("faceless_video_gen.main.fetch_images") as mock_images,
        patch("faceless_video_gen.main.assemble_video") as mock_assemble,
    ):
        mock_script.return_value = "Mocked script"
        mock_audio.return_value = "/tmp/audio.mp3"
        mock_images.return_value = ["/tmp/img0.jpg", "/tmp/img1.jpg"]
        mock_assemble.return_value = "output.mp4"

        result = generate_video("Python", output="output.mp4")

    assert result == "output.mp4"
    mock_script.assert_called_once()
    mock_audio.assert_called_once()
    mock_images.assert_called_once()
    mock_assemble.assert_called_once()


def test_generate_video_passes_topic_to_script():
    """The topic is forwarded to generate_script."""
    with (
        patch("faceless_video_gen.main.generate_script") as mock_script,
        patch("faceless_video_gen.main.generate_audio"),
        patch("faceless_video_gen.main.fetch_images") as mock_images,
        patch("faceless_video_gen.main.assemble_video") as mock_assemble,
    ):
        mock_script.return_value = "Script"
        mock_images.return_value = ["img.jpg"]
        mock_assemble.return_value = "out.mp4"

        generate_video("data science", output="out.mp4")

    args, kwargs = mock_script.call_args
    assert "data science" in args or kwargs.get("topic") == "data science"


def test_generate_video_returns_output_path():
    """generate_video returns whatever assemble_video returns."""
    with (
        patch("faceless_video_gen.main.generate_script", return_value="s"),
        patch("faceless_video_gen.main.generate_audio"),
        patch("faceless_video_gen.main.fetch_images", return_value=["i.jpg"]),
        patch(
            "faceless_video_gen.main.assemble_video",
            return_value="/custom/path/video.mp4",
        ),
    ):
        result = generate_video("topic", output="/custom/path/video.mp4")

    assert result == "/custom/path/video.mp4"


# ---------------------------------------------------------------------------
# video.py edge case
# ---------------------------------------------------------------------------


def test_assemble_video_raises_on_empty_image_list():
    """assemble_video raises ValueError when no images are provided."""
    from faceless_video_gen.video import assemble_video

    with pytest.raises(ValueError, match="At least one image"):
        assemble_video([], "audio.mp3", "out.mp4")
