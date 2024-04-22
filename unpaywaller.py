from archivetoday import find_archivetoday_entry
from wayback import find_wayback_entry
from sites import WAYBACK_AVOID
from utils import get_domain


def unpaywall(link: str) -> None:
    """
    Determine the best strategy for unpaywalling this link and perform it.
    :param link: Link to unpaywall
    """
    domain = get_domain(link)
    if not (domain in WAYBACK_AVOID):
        wayback = find_wayback_entry(link)
        if wayback:
            return wayback

    archivetoday = find_archivetoday_entry(link)
    if archivetoday:
        return archivetoday
