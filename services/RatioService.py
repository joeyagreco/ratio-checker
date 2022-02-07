from tweepy import Tweet

from server.enums.RatioGrade import RatioGrade
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
        # the percentage of tweet score that the parent tweet has to have ABOVE the reply tweet to be considered for this bot to serve
        # ex: 1 = 1%, 15 = 15%, etc...
        self.__TWEET_SCORE_BUFFER_PERCENT = 10
        # this is used to prevent division by 0 without affecting the overall score in calculations
        self.__VERY_SMALL_NUMBER = 0.000000000000000000000001
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
        tweetFields = [TweetField.CONVERSATION_ID, TweetField.CREATED_AT, TweetField.IN_REPLY_TO_USER_ID,
                       TweetField.PUBLIC_METRICS, TweetField.REFERENCED_TWEETS]
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
            parentTweetId = None
            # check if "referenced_tweets" is in the tweet data
            # if it isn't, we skip this tweet
            if "referenced_tweets" in tweet.data:
                for referencedTweet in tweet.data["referenced_tweets"]:
                    # find the "replied_to" entry
                    if referencedTweet["type"] == "replied_to":
                        parentTweetId = referencedTweet["id"]
                parentTweet = TwitterSearcher.getTweet(parentTweetId, tweetFields)[0]
                if parentTweet is not None and str(tweet.id) not in savedTweetIds:
                    validReplyTweets.append(
                        ReplyTweet(None, str(tweet.id), str(parentTweet.id), tweet.data["created_at"]))

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
                # check if the tweet scores differ enough to qualify for a serve from the bot
                parentTweetScore = self.__getTweetScore(actualParentTweet)
                replyTweetScore = self.__getTweetScore(actualReplyTweet)
                # get the ratio grade and respond accordingly
                ratioGrade = self.__getRatioGrade(replyTweetScore, parentTweetScore)
                if ratioGrade in RatioGrade.allValidGrades():
                    # check if the reply was a ratio
                    if ratioGrade in RatioGrade.allPassingGrades():
                        # this is a ratio
                        tweetText = f"{self.__SUCCESSFUL_RATIO_TEXT}\n\nRatio Grade: {ratioGrade.name}"
                    else:
                        # this is not a ratio
                        tweetText = f"{self.__FAILED_RATIO_TEXT}\n\nRatio Grade: {ratioGrade.name}"
                    # respond with results
                    print(TwitterTweeter.createReplyTweet(tweetText, int(replyTweet.tweetId)))
                else:
                    print("REQUIREMENTS NOT MET FOR THIS BOT TO SERVE")

            else:
                print("CANNOT SERVE: TWEET/S DELETED")

    def __getRatioGrade(self, replyTweetScore: int, parentTweetScore: int) -> RatioGrade:
        if parentTweetScore < self.__BASELINE_TWEET_SCORE \
                or abs(parentTweetScore - replyTweetScore) < self.__TWEET_SCORE_BUFFER:
            return RatioGrade.UNGRADABLE
        if replyTweetScore < parentTweetScore:
            return RatioGrade.F

        ratioPercentage = (replyTweetScore / (parentTweetScore + self.__VERY_SMALL_NUMBER)) - 1
        if ratioPercentage >= 100:
            return RatioGrade.A_PLUS
        elif ratioPercentage >= 50:
            return RatioGrade.A
        elif ratioPercentage >= 25:
            return RatioGrade.A_MINUS
        elif ratioPercentage >= 10:
            return RatioGrade.B_PLUS
        elif ratioPercentage >= 5:
            return RatioGrade.B
        elif ratioPercentage >= 3:
            return RatioGrade.B_MINUS
        elif ratioPercentage >= 2:
            return RatioGrade.C_PLUS
        elif ratioPercentage >= 1:
            return RatioGrade.C
        elif ratioPercentage >= 0.9:
            return RatioGrade.C_MINUS
        elif ratioPercentage >= 0.8:
            return RatioGrade.D_PLUS
        elif ratioPercentage >= 0.7:
            return RatioGrade.D
        elif ratioPercentage >= 0.6:
            return RatioGrade.D_MINUS
        else:
            return RatioGrade.UNGRADABLE
