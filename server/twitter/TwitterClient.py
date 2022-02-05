import tweepy
from tweepy import Client

from server.auth.TwitterAuth import TwitterAuth


class TwitterClient:
    bearerToken = TwitterAuth.bearerToken

    @classmethod
    def getClient(cls) -> Client:
        return tweepy.Client(bearer_token=cls.bearerToken)
