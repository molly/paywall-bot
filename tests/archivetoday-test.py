from unpaywaller import unpaywall


def test_unpaywall():
    s = unpaywall(
        "https://www.nytimes.com/2024/04/22/nyregion/trump-trial-opening-statements-takeaways.html"
    )
