from server.enums.TweetField import TweetField
from server.models.ReplyTweet import ReplyTweet
from server.repositories.ReplyTweetRepository import ReplyTweetRepository
from server.twitter.TwitterSearcher import TwitterSearcher


class RatioService:

    def __init__(self):
        self.__replyTweetRepository = ReplyTweetRepository()
        self.__MAX_ROWS_TO_SAVE = 50

    def harvestRatioReplies(self, numberOfRepliesToHarvest: int) -> bool:
        """
        This method will "harvest" the given number of tweets that are replies and save them to a database.
        Returns a boolean of whether any ratio replies were harvested
        """
        # first, check if we have hit the limit of total tweet replies we want to save
        if self.__replyTweetRepository.getNumberOfRows() >= self.__MAX_ROWS_TO_SAVE:
            return False

        # info we are interested in for "ratio" tweets
        tweetFields = [TweetField.IN_REPLY_TO_USER_ID, TweetField.PUBLIC_METRICS, TweetField.CONVERSATION_ID,
                       TweetField.CREATED_AT]
        # query info: https://developer.twitter.com/en/docs/twitter-api/enterprise/rules-and-filtering/operators-by-product
        query = "ratio lang:en is:reply"

        # get tweets from Twitter
        ratioReplyTweets = TwitterSearcher.getRecentTweets(query, tweetFields, numberOfRepliesToHarvest)

        # prevent any tweets that are already saved to the database from being added again by keeping track of the ids we already have
        savedReplyTweets = self.__replyTweetRepository.getAllReplyTweets()
        savedTweetIds = [tweet.tweetId for tweet in savedReplyTweets]

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
