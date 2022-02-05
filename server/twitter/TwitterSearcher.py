from typing import List

from tweepy import Response

from server.twitter.TwitterClient import TwitterClient
from server.enums.TweetField import TweetField


class TwitterSearcher:

    @classmethod
    def getRecentTweets(cls, query: str, tweetFields: List[TweetField], maxResults: int) -> Response:
        client = TwitterClient.getClient()
        # convert tweet fields to strings
        tweetFieldsStr = [TweetField.normalized(tweetField) for tweetField in tweetFields]
        return client.search_recent_tweets(query=query, tweet_fields=tweetFieldsStr, max_results=maxResults)

    @classmethod
    def getTweet(cls, id: str, tweetFields: List[TweetField]) -> Response:
        client = TwitterClient.getClient()
        # convert tweet fields to strings
        tweetFieldsStr = [TweetField.normalized(tweetField) for tweetField in tweetFields]
        return client.get_tweet(id=id, tweet_fields=tweetFieldsStr)
