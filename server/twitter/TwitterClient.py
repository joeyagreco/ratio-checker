import tweepy
from tweepy import Client

from server.auth.TwitterAuth import TwitterAuth


class TwitterClient:
    __bearerToken = TwitterAuth.bearerToken
    __apiKey = TwitterAuth.apiKey
    __apiKeySecret = TwitterAuth.apiKeySecret
    __accessToken = TwitterAuth.accessToken
    __accessTokenSecret = TwitterAuth.accessTokenSecret

    @classmethod
    def getClient(cls) -> Client:
        return tweepy.Client(bearer_token=cls.__bearerToken,
                             consumer_key=cls.__apiKey,
                             consumer_secret=cls.__apiKeySecret,
                             access_token=cls.__accessToken,
                             access_token_secret=cls.__accessTokenSecret)
