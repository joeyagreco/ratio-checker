from typing import List, Optional

import psycopg2
from psycopg2.extras import execute_values

from server.models.ReplyTweet import ReplyTweet
from server.util.EnvironmentReader import EnvironmentReader


class ReplyTweetRepository:

    def __init__(self):
        self.__conn = None
        self.__schema = "ratio_checker"
        self.__table = "reply_tweet"
        # POSTGRESQL ERROR CODES
        # DOCUMENTATION: https://www.postgresql.org/docs/current/errcodes-appendix.html#ERRCODES-TABLE
        self.__UNIQUE_VIOLATION_ERROR_CODE = "23505"
        # QUERIES
        self.__getAllReplyTweetsQuery = """
                                        SELECT id, tweet_id, parent_tweet_id, tweeted_at
                                        FROM {schema}.{table}
        """
        self.__getAllReplyTweetsAtLeastNDaysOldQuery = """
                                        SELECT id, tweet_id, parent_tweet_id, tweeted_at
                                        FROM {schema}.{table}
                                        WHERE tweeted_at < (NOW() AT TIME ZONE 'utc') - INTERVAL '{numberOfDays} day'
        """
        self.__addReplyTweetsQuery = """
                                        INSERT INTO {schema}.{table} (tweet_id, parent_tweet_id, tweeted_at)
                                        VALUES %s
                                        RETURNING id, tweet_id, parent_tweet_id, tweeted_at
        """
        self.__getNumberOfRowsQuery = """
                                        SELECT COUNT(*) FROM {schema}.{table}
        """

    def __connect(self):
        self.__conn = psycopg2.connect(
            host=EnvironmentReader.get("DB_HOST"),
            database=EnvironmentReader.get("DB_DATABASE"),
            user=EnvironmentReader.get("DB_USER"),
            password=EnvironmentReader.get("DB_PASSWORD"))

    def __close(self):
        self.__conn.close()
        self.__conn = None

    def __objectifyReplyTweet(self, replyTweetResult: List) -> Optional[ReplyTweet]:
        replyTweet = None
        if replyTweetResult:
            replyTweet = ReplyTweet(replyTweetResult[0],
                                    replyTweetResult[1],
                                    replyTweetResult[2],
                                    replyTweetResult[3])
        return replyTweet

    def __objectifyReplyTweetList(self, replyTweetListResult: List) -> List[ReplyTweet]:
        replyTweetList = list()
        for replyTweetResult in replyTweetListResult:
            replyTweetList.append(self.__objectifyReplyTweet(replyTweetResult))
        return replyTweetList

    def getAllReplyTweets(self):
        self.__connect()
        with self.__conn.cursor() as cursor:
            cursor.execute(
                self.__getAllReplyTweetsQuery.format(schema=self.__schema,
                                                     table=self.__table)
            )
            replyTweetResults = cursor.fetchall()
        self.__close()
        return self.__objectifyReplyTweetList(replyTweetResults)

    def getAllReplyTweetsAtLeastNDaysOld(self, numberOfDays: int):
        self.__connect()
        with self.__conn.cursor() as cursor:
            cursor.execute(
                self.__getAllReplyTweetsAtLeastNDaysOldQuery.format(schema=self.__schema,
                                                                    table=self.__table,
                                                                    numberOfDays=numberOfDays)
            )
            replyTweetResults = cursor.fetchall()
        self.__close()
        return self.__objectifyReplyTweetList(replyTweetResults)

    def addReplyTweets(self, replyTweetList: List[ReplyTweet]) -> List[ReplyTweet]:

        try:
            self.__connect()
            with self.__conn.cursor() as cursor:
                addReplyTweetsQuery = self.__addReplyTweetsQuery.format(schema=self.__schema,
                                                                        table=self.__table)
                allReplyTweets = [(rt.tweetId, rt.parentTweetId, rt.tweetedAt) for rt in replyTweetList]
                execute_values(cursor, addReplyTweetsQuery, allReplyTweets)
                self.__conn.commit()
                replyTweetResults = cursor.fetchall()
                self.__close()
                return self.__objectifyReplyTweetList(replyTweetResults)
        except psycopg2.Error as e:
            # get error code
            # ERROR CODES: https://www.postgresql.org/docs/current/errcodes-appendix.html#ERRCODES-TABLE
            errorCode = e.pgcode
            print(errorCode)
            raise e

    def getNumberOfRows(self):
        self.__connect()
        with self.__conn.cursor() as cursor:
            cursor.execute(
                self.__getNumberOfRowsQuery.format(schema=self.__schema,
                                                   table=self.__table)
            )
            replyTweetResults = cursor.fetchone()
        self.__close()
        return replyTweetResults[0]
