from utils import parse_timemap, get_domain

TIMEMAP = (
    """<https://www.wired.com/story/pig-butchering-fbi-ic3-2022-report/>; rel="original",
<http://archive.md/timegate/https://www.wired.com/story/pig-butchering-fbi-ic3-2022-report/>; rel="timegate",
<http://archive.md/20230310020348/https://www.wired.com/story/pig-butchering-fbi-ic3-2022-report/>; rel="first memento"; datetime="Fri, 10 Mar 2023 02:03:48 GMT",
<http://archive.md/20230311152440/https://www.wired.com/story/pig-butchering-fbi-ic3-2022-report/>; rel="last memento"; datetime="Sat, 11 Mar 2023 15:24:40 GMT",
<http://archive.md/timemap/https://www.wired.com/story/pig-butchering-fbi-ic3-2022-report/>; rel="self"; type="application/link-format"; from="Fri, 10 Mar 2023 02:03:48 GMT"; until="Sat, 11 Mar 2023 15:24:40 GMT"""
    ""
)


def test_parse_timemap():
    result = parse_timemap(TIMEMAP)
    assert (
        result["original"]
        == "https://www.wired.com/story/pig-butchering-fbi-ic3-2022-report/"
    )
    assert (
        result["timegate"]
        == "http://archive.md/timegate/https://www.wired.com/story/pig-butchering-fbi-ic3-2022-report/"
    )
    assert (
        result["first"]
        == "http://archive.md/20230310020348/https://www.wired.com/story/pig-butchering-fbi-ic3-2022-report/"
    )
    assert (
        result["last"]
        == "http://archive.md/20230311152440/https://www.wired.com/story/pig-butchering-fbi-ic3-2022-report/"
    )
    assert len(result["mementos"]) == 2


def test_parse_timemap_first_last():
    result = parse_timemap(
        """<http://archive.md/20240422194015/https://www.nytimes.com/2024/04/22/nyregion/trump-trial-opening-statements-takeaways.html>; rel="first last memento"; datetime="Mon, 22 Apr 2024 19:40:15 GMT","""
    )
    assert (
        result["first"]
        == "http://archive.md/20240422194015/https://www.nytimes.com/2024/04/22/nyregion/trump-trial-opening-statements-takeaways.html"
    )
    assert (
        result["last"]
        == "http://archive.md/20240422194015/https://www.nytimes.com/2024/04/22/nyregion/trump-trial-opening-statements-takeaways.html"
    )


def test_parse_empty_timemap():
    result = parse_timemap("")
    assert result == {"mementos": []}


def test_get_domain():
    assert get_domain("https://nytimes.com/foo") == "nytimes.com"
    assert get_domain("https://www.nytimes.com/foo") == "nytimes.com"
