from __future__ import annotations
from enum import unique, Enum, auto


@unique
class TweetField(Enum):
    """
    All Tweet fields: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet#:~:text=Place%20objects-,Tweet,-Tweets%20are%20the
    """
    AUTHOR_ID = auto()
    CONVERSATION_ID = auto()
    CREATED_AT = auto()
    IN_REPLY_TO_USER_ID = auto()
    PUBLIC_METRICS = auto()
    REFERENCED_TWEETS = auto()
    TEXT = auto()

    @staticmethod
    def normalized(tweetField: TweetField) -> str:
        """
        This converts the enum into something the Twitter API can recognize and consume.
        """
        return tweetField.name.lower()
