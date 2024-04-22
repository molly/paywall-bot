import logging
from constants import USER_AGENT
from typing import Optional
from waybackpy import WaybackMachineSaveAPI, WaybackMachineCDXServerAPI
from waybackpy.exceptions import (
    WaybackError,
    NoCDXRecordFound,
    MaximumSaveRetriesExceeded,
    TooManyRequestsError,
)


def save_wayback_url(link: str) -> Optional[str]:
    """
    Save a new archived copy of the specified link.
    :param link: Link to archive
    :return: Archive URL, or None if archiving fails
    """
    logger = logging.getLogger("paywall-bot")
    try:
        logger.debug("Trying to save a new copy of link: {}".format(link))
        save_api = WaybackMachineSaveAPI(link, user_agent=USER_AGENT)
        archive_href = save_api.save()
        logger.debug("Saved copy of link {}".format(link.index))
        return archive_href
    except (MaximumSaveRetriesExceeded, TooManyRequestsError):
        logger.debug("Archive link {} exceeded max retries.".format(link))
    return None


def find_wayback_entry(link: str) -> Optional[str]:
    """
    Find an existing archived copy of the specified link.
    :param link:
    :return: Archive URL, or None if no archived copy is found
    """
    logger = logging.getLogger("paywall-bot")
    try:
        # Try to get a recent archived copy
        logger.debug("Looking for recent archive of link: {}".format(link))
        cdx = WaybackMachineCDXServerAPI(
            link, user_agent=USER_AGENT, filters=["statuscode:200"], limit=1
        )
        newest = cdx.newest()
        return newest.archive_url
    except NoCDXRecordFound:
        logger.debug("Link {} has no archived copies.".format(link.index))
    except WaybackError as e:
        logger.exception("Error looking up archive for link: %s. %s", link, e)


def wayback_archive_url(link: str) -> Optional[str]:
    """
    Get an archive link, either by retrieving an existing archived copy or creating one, and return its URL.

    :param link: Link details for this given link
    :return: Archive link
    """
    existing = find_wayback_entry(link)
    if existing:
        return existing
    new_archive = save_wayback_url(link)
    return None
