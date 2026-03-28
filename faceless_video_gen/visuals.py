"""Image fetching for video slideshow.

Uses the Unsplash API when UNSPLASH_ACCESS_KEY is set.
Falls back to picsum.photos (no key required) for offline/dev use.
"""

import os
from pathlib import Path

import httpx


def fetch_images(
    query: str,
    count: int = 10,
    output_dir: str = "images",
) -> list[str]:
    """Download `count` images related to `query` and return their local paths."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    access_key = os.getenv("UNSPLASH_ACCESS_KEY")

    if access_key:
        return _fetch_unsplash(query, count, output_dir, access_key)
    return _fetch_picsum(count, output_dir)


def _fetch_unsplash(
    query: str,
    count: int,
    output_dir: str,
    access_key: str,
) -> list[str]:
    url = "https://api.unsplash.com/photos/random"
    params = {
        "query": query,
        "count": min(count, 30),
        "orientation": "landscape",
    }
    headers = {"Authorization": f"Client-ID {access_key}"}

    with httpx.Client(timeout=30) as client:
        response = client.get(url, params=params, headers=headers)
        response.raise_for_status()
        photos = response.json()

    paths: list[str] = []
    for i, photo in enumerate(photos):
        img_url = photo["urls"]["regular"]
        path = f"{output_dir}/image_{i:02d}.jpg"
        _download(img_url, path)
        paths.append(path)
    return paths


def _fetch_picsum(count: int, output_dir: str) -> list[str]:
    """Fallback: download random 1280×720 images from picsum.photos."""
    paths: list[str] = []
    with httpx.Client(timeout=30, follow_redirects=True) as client:
        for i in range(count):
            url = f"https://picsum.photos/seed/{i}/1280/720"
            path = f"{output_dir}/image_{i:02d}.jpg"
            response = client.get(url)
            response.raise_for_status()
            Path(path).write_bytes(response.content)
            paths.append(path)
    return paths


def _download(url: str, path: str) -> None:
    with httpx.Client(timeout=30, follow_redirects=True) as client:
        response = client.get(url)
        response.raise_for_status()
        Path(path).write_bytes(response.content)
