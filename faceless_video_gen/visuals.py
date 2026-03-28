"""Visual asset fetching for video background.

Priority for video clips (best quality):
1. Pexels Videos API (PEXELS_API_KEY) — free, topic-relevant B-roll

Priority for image fallback (when no video source available):
1. Pexels Photos API (PEXELS_API_KEY) — free, topic-relevant
2. Unsplash API    (UNSPLASH_ACCESS_KEY) — free, topic-relevant
3. picsum.photos   — no key, but random (not topic-relevant)
"""

import os
from pathlib import Path

import httpx


def fetch_video_clips(
    query: str,
    count: int = 5,
    output_dir: str = "clips",
) -> list[str] | None:
    """Download stock video clips for the given query.

    Returns a list of local .mp4 paths, or None if no video source is available.
    """
    pexels_key = os.getenv("PEXELS_API_KEY")
    if not pexels_key:
        return None

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    return _fetch_pexels_videos(query, count, output_dir, pexels_key)


def fetch_images(
    query: str,
    count: int = 10,
    output_dir: str = "images",
) -> list[str]:
    """Download stock images for the given query and return their local paths."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    pexels_key = os.getenv("PEXELS_API_KEY")
    unsplash_key = os.getenv("UNSPLASH_ACCESS_KEY")

    if pexels_key:
        return _fetch_pexels_photos(query, count, output_dir, pexels_key)
    if unsplash_key:
        return _fetch_unsplash(query, count, output_dir, unsplash_key)
    return _fetch_picsum(count, output_dir)


# ---------------------------------------------------------------------------
# Pexels
# ---------------------------------------------------------------------------


def _fetch_pexels_videos(
    query: str,
    count: int,
    output_dir: str,
    api_key: str,
) -> list[str]:
    url = "https://api.pexels.com/videos/search"
    params = {
        "query": query,
        "per_page": min(count, 80),
        "orientation": "landscape",
        "size": "medium",
    }
    headers = {"Authorization": api_key}

    with httpx.Client(timeout=30) as client:
        response = client.get(url, params=params, headers=headers)
        response.raise_for_status()
        videos = response.json().get("videos", [])

    paths: list[str] = []
    for i, video in enumerate(videos[:count]):
        file_url = _best_video_file(video["video_files"])
        if not file_url:
            continue
        path = f"{output_dir}/clip_{i:02d}.mp4"
        _download(file_url, path)
        paths.append(path)
    return paths


def _best_video_file(video_files: list[dict]) -> str | None:
    """Pick the best landscape HD file from a Pexels video_files list."""
    preferred = [f for f in video_files if f.get("width", 0) >= 1280]
    preferred.sort(key=lambda f: f.get("width", 0))
    if preferred:
        return preferred[0]["link"]
    # fallback: any file
    return video_files[0]["link"] if video_files else None


def _fetch_pexels_photos(
    query: str,
    count: int,
    output_dir: str,
    api_key: str,
) -> list[str]:
    url = "https://api.pexels.com/v1/search"
    params = {"query": query, "per_page": min(count, 80), "orientation": "landscape"}
    headers = {"Authorization": api_key}

    with httpx.Client(timeout=30) as client:
        response = client.get(url, params=params, headers=headers)
        response.raise_for_status()
        photos = response.json().get("photos", [])

    paths: list[str] = []
    for i, photo in enumerate(photos[:count]):
        img_url = photo["src"]["large2x"]
        path = f"{output_dir}/image_{i:02d}.jpg"
        _download(img_url, path)
        paths.append(path)
    return paths


# ---------------------------------------------------------------------------
# Unsplash
# ---------------------------------------------------------------------------


def _fetch_unsplash(
    query: str,
    count: int,
    output_dir: str,
    access_key: str,
) -> list[str]:
    url = "https://api.unsplash.com/photos/random"
    params = {"query": query, "count": min(count, 30), "orientation": "landscape"}
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


# ---------------------------------------------------------------------------
# picsum fallback
# ---------------------------------------------------------------------------


def _fetch_picsum(count: int, output_dir: str) -> list[str]:
    """Fallback: random 1280×720 images — not topic-relevant."""
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


# ---------------------------------------------------------------------------
# shared
# ---------------------------------------------------------------------------


def _download(url: str, path: str) -> None:
    with httpx.Client(timeout=60, follow_redirects=True) as client:
        response = client.get(url)
        response.raise_for_status()
        Path(path).write_bytes(response.content)
