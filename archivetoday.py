from constants import USER_AGENT
from utils import parse_timemap
import logging
import requests
from typing import Optional


def find_archivetoday_entry(link: str) -> Optional[str]:
    """
    Find an existing archived copy of the specified link.
    :param link:
    :return: Archive URL, or None if no archived copy is found
    """
    logger = logging.getLogger("paywall-bot")
    try:
        # Try to get a recent archived copy
        logger.debug("Looking for recent archive of link: {}".format(link))
        resp = requests.get(
            "https://archive.is/timemap/{}".format(link),
            headers={"User-Agent": USER_AGENT},
        )
        if resp.status_code == 404:
            # No archived copies exist, try to save a new one
            return None
        else:
            timemap = parse_timemap(resp.text)
            if "last" in timemap:
                return timemap["last"]
            elif "timegate" in timemap:
                return timemap["timegate"]
    except Exception as e:
        logger.exception(
            "Error looking up archive.today archive for link: %s. %s", link, e
        )
    return None


def archivetoday_archive_url(link: str) -> Optional[str]:
    """
    Get an archive link, either by retrieving an existing archived copy or creating one, and return its URL.
    :param link: Link details for this given link
    :return: Archive link
    """
    existing = find_archivetoday_entry(link)
