from tweepy import Tweet

from server.enums.TweetField import TweetField
from server.models.ReplyTweet import ReplyTweet
from server.repositories.ReplyTweetRepository import ReplyTweetRepository
from server.twitter.TwitterSearcher import TwitterSearcher
from server.twitter.TwitterTweeter import TwitterTweeter


class RatioService:

    def __init__(self):
        self.__replyTweetRepository = ReplyTweetRepository()
        self.__MAX_ROWS_TO_SAVE = 100
        # amount of tweets Twitter requires as a minimum for searching recent tweets
        self.__TWITTER_MINIMUM_AMOUNT = 10
        # how many days old a reply tweet has to be before being considered for this bot to serve
        self.__DAYS_BEFORE_RESPONDING = 0
        # the minimum score a parent tweet has to have before any reply can be considered for this bot to serve
        self.__BASELINE_TWEET_SCORE = 3
        # the amount of tweet score that the parent tweet has to have ABOVE the reply tweet to be considered for this bot to serve
        self.__TWEET_SCORE_BUFFER = 5
        self.__SUCCESSFUL_RATIO_TEXT = "RATIO SUCCESSFUL!"
        self.__FAILED_RATIO_TEXT = "RATIO FAILED."

    def __getTweetScore(self, tweet: Tweet) -> int:
        """
        Returns the score of a tweet.
        Based off of likes and retweets.
        """
        return tweet.data["public_metrics"]["like_count"] + tweet.data["public_metrics"]["retweet_count"]

    def harvestRatioReplies(self, numberOfRepliesToHarvest: int) -> bool:
        """
        This method will "harvest" the given number of tweets that are replies and save them to a database.
        Returns a boolean of whether any ratio replies were harvested
        """
        # first, check if we have hit the limit of total tweet replies we want to save
        # (or are within 9, in which case we will stop since we must grab at least 10 tweets with each query)
        numberOfRows = self.__replyTweetRepository.getNumberOfRows()
        if numberOfRows + (self.__TWITTER_MINIMUM_AMOUNT - 1) >= self.__MAX_ROWS_TO_SAVE:
            return False
        else:
            # we'll adjust the number of reply tweets to retrieve if numberOfRepliesToHarvest will put us over the MAX_ROWS_TO_SAVE
            if numberOfRows + numberOfRepliesToHarvest > self.__MAX_ROWS_TO_SAVE:
                numberOfRepliesToHarvest = self.__MAX_ROWS_TO_SAVE - numberOfRows
            # make sure we always have at least 10 (Twitter's minimum) replies to harvest
            numberOfRepliesToHarvest = numberOfRepliesToHarvest if numberOfRepliesToHarvest >= self.__TWITTER_MINIMUM_AMOUNT else self.__TWITTER_MINIMUM_AMOUNT

        # info we are interested in for "ratio" tweets
        tweetFields = [TweetField.IN_REPLY_TO_USER_ID, TweetField.PUBLIC_METRICS, TweetField.CONVERSATION_ID,
                       TweetField.CREATED_AT]
        # query info: https://developer.twitter.com/en/docs/twitter-api/enterprise/rules-and-filtering/operators-by-product
        query = "ratio lang:en is:reply"

        # get tweets from Twitter
        ratioReplyTweets = TwitterSearcher.getRecentTweets(query, tweetFields, numberOfRepliesToHarvest)

        # prevent any tweets that are already saved to the database from being added again by keeping track of the ids we already have
        savedTweetIds = self.__replyTweetRepository.getAllTweetIds()

        # save all valid reply tweets in a list
        validReplyTweets = list()

        for tweet in ratioReplyTweets.data:
            # get the tweet it is replying to
            parentTweet = TwitterSearcher.getTweet(tweet["conversation_id"], tweetFields)[0]
            if parentTweet is not None and str(tweet.id) not in savedTweetIds:
                validReplyTweets.append(ReplyTweet(None, str(tweet.id), str(parentTweet.id), tweet.data["created_at"]))

        # add all valid reply tweets to a database
        self.__replyTweetRepository.addReplyTweets(validReplyTweets)
        return True

    def serveRatioResults(self, numberOfResultsToServe: int):
        """
        This method will "serve" the given number of results to reply tweets, stating whether the ratio was successful or not.
        """
        # get as many reply tweets as requested that are at least N days old
        replyTweets = self.__replyTweetRepository.getAllReplyTweetsAtLeastNDaysOld(self.__DAYS_BEFORE_RESPONDING,
                                                                                   limit=numberOfResultsToServe)
        # now that we have them saved locally, we delete them from the database
        self.__replyTweetRepository.deleteReplyTweetsByIds([rt.id for rt in replyTweets])
        # go through each reply tweet and determine if it was a successful ratio or not
        # info we are interested in
        tweetFields = [TweetField.PUBLIC_METRICS]
        for replyTweet in replyTweets:
            # first get the reply tweet
            actualReplyTweet = TwitterSearcher.getTweet(replyTweet.tweetId, tweetFields).data
            # then get the parent tweet
            actualParentTweet = TwitterSearcher.getTweet(replyTweet.parentTweetId, tweetFields).data
            # make sure both tweets still exist
            if actualReplyTweet is not None and actualParentTweet is not None:
                # check if the parent tweet has a high enough score to be considered for ratios
                parentTweetScore = self.__getTweetScore(actualParentTweet)
                replyTweetScore = self.__getTweetScore(actualReplyTweet)
                if parentTweetScore >= self.__BASELINE_TWEET_SCORE and abs(
                        parentTweetScore - replyTweetScore) >= self.__TWEET_SCORE_BUFFER:
                    # check if the reply has a higher score than its parent
                    if replyTweetScore > parentTweetScore:
                        # this is a ratio
                        tweetText = self.__SUCCESSFUL_RATIO_TEXT
                    else:
                        # this is not a ratio
                        tweetText = self.__FAILED_RATIO_TEXT
                    # respond with results
                    print(TwitterTweeter.createReplyTweet(tweetText, int(replyTweet.tweetId)))
                else:
                    print("REQUIREMENTS NOT MET FOR THIS BOT TO SERVE")

            else:
                print("CANNOT SERVE: TWEET/S DELETED")
