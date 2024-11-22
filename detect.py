"""
Sanity check for Last.fm scrobbles.
"""

from datetime import datetime, timezone
import requests

# Configuration
API_KEY = ""
USER = ""


def get_recent_scrobble(user, api_key):
    """
    Get information on the most recent scrobble.

    Parameters:
    - user (str): Last.fm username
    - api_key (str): Last.fm API key

    Returns:
    - tuple of (track name (str), artist name (str), timestamp (datetime))
    """
    url = (
        "http://ws.audioscrobbler.com/2.0/"
        f"?method=user.getrecenttracks&user={user}&api_key={api_key}&format=json&limit=1"
    )
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        if "recenttracks" in data and "track" in data["recenttracks"]:
            tracks = data["recenttracks"]["track"]
            if tracks:
                most_recent = tracks[0]
                if "@attr" not in most_recent:  # Not currently playing
                    timestamp = int(most_recent["date"]["uts"])
                    return (
                        most_recent["name"],
                        most_recent["artist"]["#text"],
                        datetime.fromtimestamp(timestamp, tz=timezone.utc),
                    )
    return None


def check_scrobble_age():
    """
    Retrieves the most recent scrobble and checks if it's older than 6 hours.
    """
    name, artist, most_recent_time = get_recent_scrobble(USER, API_KEY)
    if most_recent_time:
        now = datetime.now(timezone.utc)
        delta = now - most_recent_time
        if delta.total_seconds() > 21600:
            print(
                "Alert: No scrobble in the past 6 hours."
                f'Last scrobble at {most_recent_time} with "{artist} - {name}"'
            )
        else:
            print(
                f'All good. Last scrobble at {most_recent_time} with "{artist} - {name}"'
            )
    else:
        print("No recent scrobble found or error fetching data.")


if __name__ == "__main__":
    check_scrobble_age()
