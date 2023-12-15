from typing import Optional

import requests


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
        with open(filename) as f:
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
            headers["user-agent"] = user_agents[0]

        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(e, response.status_code)
        error = True

    return response, error
