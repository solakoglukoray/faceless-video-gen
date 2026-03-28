"""CLI interface for faceless-video-gen."""

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from faceless_video_gen.main import generate_video
from faceless_video_gen.tts import AVAILABLE_VOICES

app = typer.Typer(
    help=(
        "Turn any topic into a faceless YouTube video — "
        "script, voiceover, and slideshow — with one command."
    ),
    add_completion=False,
)
console = Console()


@app.command()
def generate(
    topic: str = typer.Argument(..., help="Topic for the video (e.g. 'Python tips')"),
    output: str = typer.Option(
        "output.mp4",
        "--output",
        "-o",
        help="Output MP4 file path.",
    ),
    voice: str = typer.Option(
        "en-US-AriaNeural",
        "--voice",
        "-v",
        help=(
            f"edge-tts voice. Options: {', '.join(AVAILABLE_VOICES)}"
        ),
    ),
    duration: int = typer.Option(
        60,
        "--duration",
        "-d",
        help="Target video duration in seconds.",
    ),
    images: int = typer.Option(
        10,
        "--images",
        "-i",
        help="Number of background images to use.",
    ),
) -> None:
    """Generate a faceless YouTube video from a topic."""
    console.print(f"[bold cyan]Topic:[/bold cyan] {topic}")
    console.print(f"[bold cyan]Voice:[/bold cyan] {voice}")
    console.print(f"[bold cyan]Duration:[/bold cyan] {duration}s")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Generating script, audio, and video…", total=None)
        result = generate_video(
            topic=topic,
            output=output,
            voice=voice,
            duration=duration,
            image_count=images,
        )

    console.print(
        f"\n[bold green]Done![/bold green] Video saved to: [cyan]{result}[/cyan]"
    )


@app.command()
def voices() -> None:
    """List available edge-tts voice options."""
    console.print("[bold]Available voices:[/bold]")
    for v in AVAILABLE_VOICES:
        console.print(f"  [cyan]{v}[/cyan]")
