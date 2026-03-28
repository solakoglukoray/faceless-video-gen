"""Core pipeline: topic → script → audio → visuals → video."""

import shutil
import tempfile
from pathlib import Path

from faceless_video_gen.llm import generate_script
from faceless_video_gen.tts import generate_audio
from faceless_video_gen.video import assemble_from_clips, assemble_video
from faceless_video_gen.visuals import fetch_images, fetch_video_clips


def generate_video(
    topic: str,
    output: str = "output.mp4",
    voice: str = "en-US-AriaNeural",
    duration: int = 60,
    image_count: int = 10,
) -> str:
    """Run the full faceless-video pipeline and return the output file path.

    Steps:
    1. Generate a script with an LLM.
    2. Convert the script to speech (edge-tts).
    3. Fetch B-roll video clips (Pexels) or images as fallback.
    4. Assemble visuals + audio into an MP4.
    """
    workdir = Path(tempfile.mkdtemp(prefix="faceless_"))
    try:
        script = generate_script(topic, duration_seconds=duration)

        audio_path = str(workdir / "narration.mp3")
        generate_audio(script, voice=voice, output_path=audio_path)

        clips_dir = str(workdir / "clips")
        clip_paths = fetch_video_clips(topic, count=image_count, output_dir=clips_dir)

        if clip_paths:
            result = assemble_from_clips(clip_paths, audio_path, output_path=output)
        else:
            images_dir = str(workdir / "images")
            image_paths = fetch_images(
                topic, count=image_count, output_dir=images_dir
            )
            result = assemble_video(image_paths, audio_path, output_path=output)

        return result
    finally:
        shutil.rmtree(workdir, ignore_errors=True)
