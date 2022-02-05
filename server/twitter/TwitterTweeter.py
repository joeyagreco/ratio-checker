from tweepy import Response

from server.twitter.TwitterClient import TwitterClient


class TwitterTweeter:

    @classmethod
    def createTweet(cls, text: str) -> Response:
        client = TwitterClient.getClient()
        return client.create_tweet(text=text)
