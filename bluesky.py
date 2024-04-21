import atproto
from atproto import Client
from atproto.exceptions import BadRequestError
import logging
from queue import Queue
from time import sleep
from typing import Optional

from secrets import BSKY_PASSWORD

POLL_INTERVAL = 5


class Bluesky:
    def __init__(self, tasks: Queue, messages: Queue):
        self.client = Client()
        self.tasks = tasks
        self.messages = messages
        self.logger = logging.getLogger('paywall-bot')
        self.shutdown_flag = False

    def login(self):
        self.client.login("paywallbot.bsky.social", BSKY_PASSWORD)

    def loop(self) -> None:
        """
        Polls for notifications and adds mentions and replies to the task queue.
        """
        self.login()
        while True and not self.shutdown_flag:
            resp = self.client.models.app.bsky.notification.list_notifications()
            now = self.client.get_current_time_iso()
            for notif in resp.notifications:
                if not notif.is_read and (notif.reason == "mention" or notif.reason == "reply"):
                    self.logger.debug('Queueing notification: %s', notif.cid)
                    self.tasks.put(notif)
            self.app.bsky.notification.update_seen({"seen_at": now})
            sleep(POLL_INTERVAL)

    def getPost(self, slug: str, author: str) -> Optional[atproto.models.AppBskyFeedPost.Record]:
        """
        Get a post by its rkey and author
        :param slug: slug of the post
        :param author: DID of the author of the post
        :return: Post record or None if not found
        """
        try:
            post = self.client.get_post(slug, author)
            return post
        except BadRequestError:
            return None

    def shutdown(self):
        self.shutdown_flag = True
