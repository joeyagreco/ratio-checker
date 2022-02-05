from server.enums.TweetField import TweetField
from server.twitter.TwitterSearcher import TwitterSearcher

"""
General Guide: https://dev.to/twitterdev/a-comprehensive-guide-for-using-the-twitter-api-v2-using-tweepy-in-python-15d9#:~:text=Tweepy%20is%20a%20popular%20package,the%20academic%20research%20product%20track.
Search Queries: https://github.com/twitterdev/getting-started-with-the-twitter-api-v2-for-academic-research/blob/main/modules/5-how-to-write-search-queries.md
"conversation_id field is always the Tweet ID of the original Tweet in the conversation reply thread."
"""

if __name__ == "__main__":

    tweetFields = [TweetField.IN_REPLY_TO_USER_ID, TweetField.PUBLIC_METRICS, TweetField.CONVERSATION_ID,
                   TweetField.CREATED_AT]
    # query info: https://developer.twitter.com/en/docs/twitter-api/enterprise/rules-and-filtering/operators-by-product
    query = "ratio lang:en is:reply"

    tweets = TwitterSearcher.getRecentTweets(query, tweetFields, 10)
    print(len(tweets.data))

    for tweet in tweets.data:
        # get the tweet it is replying to
        parentTweet = TwitterSearcher.getTweet(tweet["conversation_id"], tweetFields)
        if parentTweet is not None and parentTweet[0] is not None:
            print("------")
            print("PARENT:")
            print(parentTweet[0].data["text"])
            print(parentTweet[0].data["public_metrics"]["like_count"])
            print("REPLY:")
            print(tweet.text)
            print(tweet.data["public_metrics"]["like_count"])
            print(tweet.data["created_at"])
            print(tweet.id)
            print("-----\n\n")
        else:
            print("ERROR")
