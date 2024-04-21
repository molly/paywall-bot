import atproto
from bluesky import Bluesky
import logging
from queue import Queue
from process import get_links_from_record, get_links
from unittest import TestCase

MOLLY_DID = "did:plc:exrxvyu6bpoym6mbnctke5tn"
RECORD_WITH_LINK = atproto.models.AppBskyFeedPost.Record(
    createdAt="2024-04-16T17:21:27.749Z",
    facets=[
        atproto.models.AppBskyRichtextFacet.Main(
            features=[
                atproto.models.AppBskyRichtextFacet.Link(uri="https://example.com")
            ],
            index=atproto.models.AppBskyRichtextFacet.ByteSlice(
                byte_start=2, byte_end=10
            ),
        )
    ],
    langs=["en"],
    tags=[],
    text="this has a link",
)


class ProcessTest(TestCase):
    @classmethod
    def setupClass(cls):
        cls.bsky = Bluesky(Queue(), Queue())
        cls.bsky.login()

    def test_get_links_from_plaintext(self):
        plaintext_record = atproto.models.AppBskyFeedPost.Record(
            createdAt="2024-04-16T17:21:27.749Z",
            facets=[],
            langs=["en"],
            tags=[],
            text="this has no links",
        )
        result = get_links_from_record(plaintext_record)
        assert result == []

    def test_get_links_from_facets(self):
        facet_record = RECORD_WITH_LINK
        result = get_links_from_record(facet_record)
        assert result == ["https://example.com"]

    def test_get_links_from_embeds(self):
        embed_record = atproto.models.AppBskyFeedPost.Record(
            createdAt="2024-04-17T14:18:33.633Z",
            embed=atproto.models.AppBskyEmbedExternal.Main(
                external=atproto.models.AppBskyEmbedExternal.External(
                    description='AI can be kind of useful, but I\'m not sure that a "kind of useful" tool justifies the harm.',
                    title="AI isn't useless. But is it worth it?",
                    uri="https://www.citationneeded.news/ai-isnt-useless/",
                )
            ),
            facets=[
                atproto.models.AppBskyRichtextFacet.Main(
                    features=[
                        atproto.models.AppBskyRichtextFacet.Link(
                            uri="https://www.citationneeded.news/ai-isnt-useless/"
                        )
                    ],
                    index=atproto.models.AppBskyRichtextFacet.ByteSlice(
                        byte_start=172, byte_end=133
                    ),
                )
            ],
            langs=["en"],
            tags=[],
            text="I spent a long time experimenting with AI before finally writing about it in depth. It can be pretty useful — but is it worth it?\n\nwww.citationneeded.news/ai-isnt-usel...",
        )
        result = get_links_from_record(embed_record)
        assert result == ["https://www.citationneeded.news/ai-isnt-useless/"]

    def test_get_links_from_notification_with_link_in_post(self):
        notification_with_link = atproto.models.AppBskyNotificationListNotifications.Notification(
            author=atproto.models.AppBskyActorDefs.ProfileView(
                did=MOLLY_DID, handle="molly.wiki"
            ),
            cid="asdf",
            indexed_at="2024-04-16T17:21:27.749Z",
            is_read=False,
            reason="reply",
            uri="at://did:plc:exrxvyu6bpoym6mbnctke5tn/app.bsky.feed.post/3kqbbvy4i372y",
            record=RECORD_WITH_LINK,
        )
        result = get_links(notification_with_link, self.bsky, logging.getLogger())
        assert result == ["https://example.com"]

    def test_get_links_from_notification_with_link_in_parent(self):
        notification_with_link_in_parent = atproto.models.AppBskyNotificationListNotifications.Notification(
            author=atproto.models.AppBskyActorDefs.ProfileView(
                did=MOLLY_DID, handle="molly.wiki"
            ),
            cid="asdf",
            indexed_at="2024-04-16T17:21:27.749Z",
            is_read=False,
            reason="reply",
            uri="at://did:plc:exrxvyu6bpoym6mbnctke5tn/app.bsky.feed.post/3kqbbvy4i372y",
            record=atproto.models.AppBskyFeedPost.Record(
                createdAt="2024-04-16T17:21:27.749Z",
                facets=[],
                langs=["en"],
                tags=[],
                text="@paywallbot archive",
            ),
            reply=atproto.models.AppBskyFeedPost.ReplyRef(
                parent=atproto.models.ComAtprotoRepoStrongRef.Main(
                    cid="bafyreih6dyi6cqxa6vuk245wnvmx37u2kc3wrj5mm3rgrpnrafmlrv4h7a",
                    uri="at://did:plc:exrxvyu6bpoym6mbnctke5tn/app.bsky.feed.post/3kqdi5tquiv2l",
                ),
                root=atproto.models.ComAtprotoRepoStrongRef.Main(
                    cid="bafyreih6dyi6cqxa6vuk245wnvmx37u2kc3wrj5mm3rgrpnrafmlrv4h7a",
                    uri="at://did:plc:exrxvyu6bpoym6mbnctke5tn/app.bsky.feed.post/3kqdi5tquiv2l",
                ),
            ),
        )
        result = get_links(notification_with_link_in_parent, self.bsky, logging.getLogger())
        assert result == ["https://www.citationneeded.news/ai-isnt-useless/"]
