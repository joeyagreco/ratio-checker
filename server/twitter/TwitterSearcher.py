from typing import List

from tweepy import Response, Tweet

from server.twitter.TwitterClient import TwitterClient
from server.enums.TweetField import TweetField
from server.util.EnvironmentReader import EnvironmentReader


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

    @classmethod
    def getTweetsThatMentionBot(cls, tweetFields: List[TweetField]) -> List[Tweet]:
        tweets = list()
        client = TwitterClient.getClient()
        botId = EnvironmentReader.get("BOT_TWITTER_ACCOUNT_ID")
        tweetFieldsStr = [TweetField.normalized(tweetField) for tweetField in tweetFields]
        response = client.get_users_mentions(botId, tweet_fields=tweetFieldsStr)
        if response.data is not None:
            # ignore all tweets that were authored by the bot
            for tweet in response.data:
                if str(tweet.author_id) != botId:
                    tweets.append(tweet)
        return tweets
