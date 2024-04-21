import atproto
from process import get_links_from_record


def test_get_links_from_plaintext():
    plaintext_record = atproto.models.AppBskyFeedPost.Record(
        createdAt="2024-04-16T17:21:27.749Z",
        facets=[],
        langs=["en"],
        tags=[],
        text="this has no links",
    )
    result = get_links_from_record(plaintext_record)
    assert result == []


def test_get_links_from_facets():
    facet_record = atproto.models.AppBskyFeedPost.Record(
        createdAt="2024-04-16T17:21:27.749Z",
        facets=[
            atproto.models.AppBskyRichtextFacet.Main(
                features=[atproto.models.AppBskyRichtextFacet.Link(
                    uri="https://example.com"
                )],
                index=atproto.models.AppBskyRichtextFacet.ByteSlice(byte_start=2, byte_end=10),
            )
        ],
        langs=["en"],
        tags=[],
        text="this has a link",
    )
    result = get_links_from_record(facet_record)
    assert result == ["https://example.com"]
