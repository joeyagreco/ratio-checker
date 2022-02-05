import requests
import tweepy
from requests.auth import HTTPBasicAuth

from server.enums.TweetField import TweetField
from server.twitter.TwitterClient import TwitterClient
from server.twitter.TwitterSearcher import TwitterSearcher
from server.twitter.TwitterTweeter import TwitterTweeter
from server.util.EnvironmentReader import EnvironmentReader

"""
General Guide: https://dev.to/twitterdev/a-comprehensive-guide-for-using-the-twitter-api-v2-using-tweepy-in-python-15d9#:~:text=Tweepy%20is%20a%20popular%20package,the%20academic%20research%20product%20track.
Search Queries: https://github.com/twitterdev/getting-started-with-the-twitter-api-v2-for-academic-research/blob/main/modules/5-how-to-write-search-queries.md
"conversation_id field is always the Tweet ID of the original Tweet in the conversation reply thread."
"""

if __name__ == "__main__":
    # response = TwitterTweeter.createTweet("this is a test tweet")
    # print(response)

    tweetFields = [TweetField.IN_REPLY_TO_USER_ID, TweetField.PUBLIC_METRICS, TweetField.CONVERSATION_ID]
    query = "ratio lang:en"

    tweets = TwitterSearcher.getRecentTweets(query, tweetFields, 10)
    print(tweets)

    # for replyTweet in tweets.data:
    #     if replyTweet['in_reply_to_user_id'] is not None:
    #         # this is a reply, get the tweet it is replying to
    #         parentTweet = client.get_tweet(id=replyTweet['conversation_id'], tweet_fields=tweetFields)
    #         if parentTweet is not None and parentTweet[0] is not None:
    #             print("------")
    #             print("PARENT:")
    #             print(parentTweet[0].data["text"])
    #             print(parentTweet[0].data["public_metrics"]["like_count"])
    #             print("REPLY:")
    #             print(replyTweet.text)
    #             print(replyTweet.data["public_metrics"]["like_count"])
    #             print("-----\n\n")
    #         else:
    #             print("ERROR")
