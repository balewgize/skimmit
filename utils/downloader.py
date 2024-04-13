from typing import Optional

import os
import random
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
}


def get_user_agents(filename: str) -> Optional[list[str]]:
    """Read user agent list from file"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(current_dir, filename)
        with open(full_path) as f:
            user_agents = f.read().splitlines()
    except Exception as e:
        user_agents = None

    return user_agents


def download_page(url: str) -> tuple[requests.Response, bool]:
    """Download HTML page from URL"""

    filename = "user_agents.txt"
    user_agents = get_user_agents(filename)
    error = False
    try:
        if user_agents:
            headers["user-agent"] = random.choice(user_agents)

        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(e, response.status_code)
        error = True

    return response, error


def get_article_text(url: str) -> str:
    """Get article text from URL"""
    response, error = download_page(url)
    if error:
        return ""

    # TODO: remove unimportant tags like header and footer
    soup = BeautifulSoup(response.text, "html.parser")
    article_text = soup.find("body").get_text()
    return article_text


def get_youtube_transcript(url: str) -> str:
    """Get YouTube transcript from URL"""
    source_text = ""
    try:
        video_id = url.split("v=")[1].split("&")[0]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = TextFormatter()
        source_text = formatter.format_transcript(transcript)
    except Exception as e:
        print(e)
    return source_text
