import tweepy
from tweepy import Client

from server.util.EnvironmentReader import EnvironmentReader


class TwitterClient:
    bearerToken = EnvironmentReader.get("BEARER_TOKEN")

    @classmethod
    def getClient(cls) -> Client:
        return tweepy.Client(bearer_token=cls.bearerToken)
