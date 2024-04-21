from bluesky import Bluesky
from queue import Queue
from unittest import TestCase

MOLLY_DID = "did:plc:exrxvyu6bpoym6mbnctke5tn"

class BlueskyTest(TestCase):
    @classmethod
    def setupClass(cls):
        cls.bsky = Bluesky(Queue(), Queue())
        cls.bsky.login()

    def test_get_nonexistent_post(self):
        post = self.bsky.getPost("nonexistent", MOLLY_DID)
        assert post is None