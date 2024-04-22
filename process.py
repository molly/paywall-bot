import atproto
from atproto.exceptions import AtProtocolError
from bluesky import Bluesky
import logging
from queue import Queue
from typing import Any

Notification = atproto.models.AppBskyNotificationListNotifications.Notification
Record = atproto.models.AppBskyFeedPost.Record


def get_links_from_record(record: Any) -> list[str]:
    """
    Extract any links in this record, either in facets or embeds. There can be duplicate links; those are handled later.
    :param record: Record to extract links from
    :return: List of links in the record
    """
    record_links = []
    if record.facets and len(record.facets) > 0:
        for facet in record.facets:
            for feature in facet.features:
                if type(feature) == atproto.models.AppBskyRichtextFacet.Link:
                    record_links.append(feature.uri)
    if "embed" in record and "external" in record.embed:
        record_links.append(record.embed.external.uri)
    return record_links


def get_links(
    notif: Notification,
    bsky: Bluesky,
    logger: logging.Logger,
) -> list[str]:
    """
    Get all links from a notification. If the notification is a reply and does not contain a link, get links from the parent post.
    :param notif: Notification to extract links from
    :param bsky: Bluesky class
    :param logger: Logger
    :return: List of links in the post or its parent, or an empty list if no links are found.
    """
    links = []
    record = notif.record

    # First look for any links in the notification post itself
    links = links + get_links_from_record(record)
    if len(links) > 0:
        return links

    # Otherwise get the parent post, if there is one
    if notif["reason"] == "reply":
        try:
            parent = bsky.get_parent(notif.reply.parent.uri)
            if parent:
                links = links + get_links_from_record(parent.thread.post.record)
        except AtProtocolError as e:
            logger.exception("Error getting parent post: %s", e)
            return links

    return links


def notifications_worker(tasks: Queue, bsky: Bluesky, logger: logging.Logger):
    while True:
        notif = tasks.get()
        record = notif.record
        text = record.text.lower()
        to_archive = get_links(notif, bsky, logger)

        # TODO Find command

        for link in to_archive:
            unpaywall(link)
