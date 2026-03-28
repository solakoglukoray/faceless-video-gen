"""Video assembly: images + audio → MP4 via MoviePy."""

from moviepy import AudioFileClip, ImageClip, concatenate_videoclips


def assemble_video(
    image_paths: list[str],
    audio_path: str,
    output_path: str = "output.mp4",
    fps: int = 24,
) -> str:
    """Assemble a slideshow MP4 from images synced to the audio track.

    Each image is shown for an equal share of the audio duration.
    Returns the path to the output file.
    """
    if not image_paths:
        raise ValueError("At least one image is required to assemble a video.")

    audio = AudioFileClip(audio_path)
    duration_per_image = audio.duration / len(image_paths)

    clips = [
        ImageClip(img).with_duration(duration_per_image)
        for img in image_paths
    ]

    video = concatenate_videoclips(clips, method="compose")
    video = video.with_audio(audio)
    video.write_videofile(output_path, fps=fps, logger=None)

    audio.close()
    video.close()

    return output_path
