import random
import re
from datetime import timedelta

from googleapiclient.discovery import build


API_KEY = "AIzaSyAWp8yt_fJOh8sr0u9OJ6a6h3lmvbJlmiE"


def iso8601_duration_to_seconds(duration: str) -> int:
    """
    Convert YouTube ISO 8601 durations like PT10M32S into seconds.
    """
    pattern = re.compile(
        r"PT"
        r"(?:(?P<hours>\d+)H)?"
        r"(?:(?P<minutes>\d+)M)?"
        r"(?:(?P<seconds>\d+)S)?"
    )
    match = pattern.fullmatch(duration)
    if not match:
        return 0

    hours = int(match.group("hours") or 0)
    minutes = int(match.group("minutes") or 0)
    seconds = int(match.group("seconds") or 0)

    return hours * 3600 + minutes * 60 + seconds


def pretty_time(seconds: int) -> str:
    return str(timedelta(seconds=seconds))


def get_duration_bucket(target_minutes: int) -> str:
    """
    Map a target length to YouTube's broad duration filters.
    """
    if target_minutes < 4:
        return "short"
    if target_minutes <= 20:
        return "medium"
    return "long"


def find_random_video(
    query: str,
    target_minutes: int = 10,
    tolerance_minutes: int = 2,
    max_search_results: int = 25,
):
    youtube = build("youtube", "v3", developerKey=API_KEY)

    # Step 1: search videos by keywords
    search_response = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=max_search_results,
        videoDuration=get_duration_bucket(target_minutes),
        safeSearch="moderate",
    ).execute()

    video_items = search_response.get("items", [])
    if not video_items:
        return None, "No videos found from search."

    video_ids = [item["id"]["videoId"] for item in video_items]

    # Step 2: get exact durations
    videos_response = youtube.videos().list(
        part="contentDetails,snippet",
        id=",".join(video_ids),
    ).execute()

    target_seconds = target_minutes * 60
    tolerance_seconds = tolerance_minutes * 60

    matches = []
    for item in videos_response.get("items", []):
        duration_str = item["contentDetails"]["duration"]
        duration_seconds = iso8601_duration_to_seconds(duration_str)

        title = item["snippet"]["title"].lower()
        query_lower = query.lower()

        # Optional title matching logic:
        # require at least one important keyword to appear in title
        title_match = any(word in title for word in query_lower.split())

        # keep videos near the target duration
        duration_match = abs(duration_seconds - target_seconds) <= tolerance_seconds

        if duration_match and title_match:
            matches.append(
                {
                    "title": item["snippet"]["title"],
                    "video_id": item["id"],
                    "duration_seconds": duration_seconds,
                    "url": f"https://www.youtube.com/watch?v={item['id']}",
                }
            )

    if not matches:
        return None, "No close matches found after filtering by title and duration."

    return random.choice(matches), None


if __name__ == "__main__":
    search_text = input("What kind of video do you want? ").strip()
    target = input("Target length in minutes (default 10): ").strip()

    try:
        target_minutes = int(target) if target else 10
    except ValueError:
        target_minutes = 10

    video, error = find_random_video(
        query=search_text,
        target_minutes=target_minutes,
        tolerance_minutes=2,
        max_search_results=25,
    )

    if error:
        print(error)
    else:
        print("\nRandom pick:")
        print(f"Title: {video['title']}")
        print(f"Length: {pretty_time(video['duration_seconds'])}")
        print(f"Link: {video['url']}")
