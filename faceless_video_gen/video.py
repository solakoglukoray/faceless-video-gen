"""Video assembly: visuals + audio → MP4 via MoviePy."""

from moviepy import AudioFileClip, ImageClip, VideoFileClip, concatenate_videoclips


def assemble_from_clips(
    clip_paths: list[str],
    audio_path: str,
    output_path: str = "output.mp4",
    fps: int = 30,
) -> str:
    """Assemble stock video clips into an MP4 synced to the audio track.

    Each clip is trimmed (or looped) to fill an equal share of the audio duration.
    Returns the path to the output file.
    """
    if not clip_paths:
        raise ValueError("At least one video clip is required.")

    audio = AudioFileClip(audio_path)
    duration_per_clip = audio.duration / len(clip_paths)

    clips = []
    for path in clip_paths:
        clip = VideoFileClip(path).without_audio()
        if clip.duration >= duration_per_clip:
            clip = clip.subclipped(0, duration_per_clip)
        else:
            # loop the clip to fill the required duration
            loops = int(duration_per_clip / clip.duration) + 1
            clip = concatenate_videoclips([clip] * loops).subclipped(
                0, duration_per_clip
            )
        clips.append(clip)

    video = concatenate_videoclips(clips, method="compose")
    video = video.with_audio(audio)
    video.write_videofile(output_path, fps=fps, logger=None)

    audio.close()
    video.close()
    for c in clips:
        c.close()

    return output_path


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
