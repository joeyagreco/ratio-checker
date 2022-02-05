import requests
import tweepy
from requests.auth import HTTPBasicAuth

"""
General Guide: https://dev.to/twitterdev/a-comprehensive-guide-for-using-the-twitter-api-v2-using-tweepy-in-python-15d9#:~:text=Tweepy%20is%20a%20popular%20package,the%20academic%20research%20product%20track.
Search Queries: https://github.com/twitterdev/getting-started-with-the-twitter-api-v2-for-academic-research/blob/main/modules/5-how-to-write-search-queries.md
"conversation_id field is always the Tweet ID of the original Tweet in the conversation reply thread."
"""

if __name__ == "__main__":
    apiKey = "k99fwGI9KxZWD0ZlwWbOFtCvC"
    apiKeySecret = "TwWOLai1JwgQ8eLA2lLrlasVgujKRdCZDlyG2lEETwv0p87JZz"
    bearerToken = "AAAAAAAAAAAAAAAAAAAAAC6MYwEAAAAAyryJnwUKyiyAZelkz0RYNGTqhE8%3DuuCBzj1HSDQaY25eTbqSdtg7zdAmj7sXbFIPZsVFzdkUDnoabn"
    accessToken = "1489809011545358340-VcDlHmQy72CJYmjelbu1SNQKRm2vMq"
    accessTokenSecret = "jSYJ0PHrco7mwYwJ4xRXcOSBPZT7Y7Gd6Cnn4mSIAPuZv"

    # client = tweepy.Client(consumer_key=apiKey,
    #                        consumer_secret=apiKeySecret,
    #                        access_token=accessToken,
    #                        access_token_secret=accessTokenSecret)
    # response = client.create_tweet(text="This is my first tweet")

    client = tweepy.Client(bearer_token=bearerToken)
    tweetFields = ['in_reply_to_user_id', 'public_metrics', 'conversation_id']
    query = "ratio lang:en"

    tweets = client.search_recent_tweets(query=query, max_results=100,
                                         tweet_fields=tweetFields)

    for replyTweet in tweets.data:
        if replyTweet['in_reply_to_user_id'] is not None:
            # this is a reply, get the tweet it is replying to
            parentTweet = client.get_tweet(id=replyTweet['conversation_id'], tweet_fields=tweetFields)
            if len(parentTweet) > 0:
                print("------")
                print("PARENT:")
                print(parentTweet[0].data["text"])
                print(parentTweet[0].data["public_metrics"]["like_count"])
                print("REPLY:")
                print(replyTweet.text)
                print(replyTweet.data["public_metrics"]["like_count"])
                print("-----\n\n")
            else:
                print("ERROR")
    # replyId = "1489818994290921477"
    # mainTweetId = "1489813897540513795"
    #
    # mainTweet = client.get_tweet(id=mainTweetId,
    #                              tweet_fields=['public_metrics', 'in_reply_to_user_id', 'conversation_id'])
    # replyTweet = client.get_tweet(id=mainTweetId,
    #                               tweet_fields=['public_metrics', 'in_reply_to_user_id', 'conversation_id'])
    # print(mainTweet.data['conversation_id'])
    # print(replyTweet.data['conversation_id'])
