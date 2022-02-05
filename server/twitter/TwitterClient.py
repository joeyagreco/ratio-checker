import tweepy
from tweepy import Client

from server.auth.TwitterAuth import TwitterAuth


class TwitterClient:
    bearerToken = TwitterAuth.bearerToken
    apiKey = TwitterAuth.apiKey
    apiKeySecret = TwitterAuth.apiKeySecret
    accessToken = TwitterAuth.accessToken
    accessTokenSecret = TwitterAuth.accessTokenSecret

    @classmethod
    def getClient(cls) -> Client:
        return tweepy.Client(bearer_token=cls.bearerToken,
                             consumer_key=cls.apiKey,
                             consumer_secret=cls.apiKeySecret,
                             access_token=cls.accessToken,
                             access_token_secret=cls.accessTokenSecret)
