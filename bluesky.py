from atproto import Client
from secrets import BSKY_PASSWORD
from queue import Queue
from time import sleep

POLL_INTERVAL = 5


class Bluesky:
    def __init__(self, tasks: Queue, messages: Queue):
        self.client = Client()
        self.tasks = tasks
        self.messages = messages
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
                    self.tasks.put(notif)
            self.app.bsky.notification.update_seen({"seen_at": now})
            sleep(POLL_INTERVAL)

    def shutdown(self):
        self.shutdown_flag = True
