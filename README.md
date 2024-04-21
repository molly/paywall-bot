# paywall-bot
A Bluesky bot to help people find unpaywalled resources.

## Using the bot

### Replies
If you encounter a Bluesky post with a paywalled link, simply reply to the message, mentioning `@paywallbot.bsky.social` and using the phrase `unpaywall`. The bot will try to find an unpaywalled version of the link(s) in the parent post and reply with it. 

You can also use the command `@paywallbot.bsky.social archive` to specifically request that the bot archive a link (regardless of whether that link is behind a paywall). 

### Standalone posts
You can also mention `@paywallbot.bsky.social unpaywall` or `@paywallbot.bsky.social archive` in a standalone post, and the bot will try to find an unpaywalled version of the link you provide.

If you include a link in an unpaywall or archive request that is a reply, the bot will assume you want to unpaywall the provided link rather than any links in the parent post.