from datetime import datetime


class ReplyTweet:

    def __init__(self, id: int, tweetId: str, parentTweetId: str, tweetedAt: datetime):
        self.id = id
        self.tweetId = tweetId
        self.parentTweetId = parentTweetId
        self.tweetedAt = tweetedAt

    def __str__(self):
        return f"\nid: {self.id}\ntweetId: {self.tweetId}\nparentTweetId: {self.parentTweetId}\ntweetedAt: {self.tweetedAt}"

    def __repr__(self):
        return f"\nid: {self.id}\ntweetId: {self.tweetId}\nparentTweetId: {self.parentTweetId}\ntweetedAt: {self.tweetedAt}"
