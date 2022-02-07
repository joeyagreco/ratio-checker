import time

from tweepy import TooManyRequests

from server.util.TimeHelper import TimeHelper
from services.RatioService import RatioService

"""
General Guide: https://dev.to/twitterdev/a-comprehensive-guide-for-using-the-twitter-api-v2-using-tweepy-in-python-15d9#:~:text=Tweepy%20is%20a%20popular%20package,the%20academic%20research%20product%20track.
Search Queries: https://github.com/twitterdev/getting-started-with-the-twitter-api-v2-for-academic-research/blob/main/modules/5-how-to-write-search-queries.md
Get Tweet By ID UI: https://www.bram.us/2017/11/22/accessing-a-tweet-using-only-its-id-and-without-the-twitter-api/
API Request Limits: https://developer.twitter.com/en/docs/twitter-api/getting-started/about-twitter-api
"""

if __name__ == "__main__":
    ratioService = RatioService()

    # harvest tweets as long as we can
    NUMBER_OF_TWEETS_TO_HARVEST = 100
    NUMBER_OF_RESULTS_TO_SERVE = 100
    DEFAULT_SLEEP_TIME_SECONDS = 3600
    ERROR_SLEEP_TIME_SECONDS = 1200
    while True:
        try:
            print("HARVESTING TWEETS")
            for i in range(5):
                numberOfTweetsHarvested = ratioService.harvestRatioReplies(NUMBER_OF_TWEETS_TO_HARVEST)
                print(f"HARVESTED {numberOfTweetsHarvested} TWEETS")
                if numberOfTweetsHarvested == 0:
                    break
            numberOfResultsServed = ratioService.serveRatioResults(NUMBER_OF_RESULTS_TO_SERVE)
            print(f"SERVED {numberOfResultsServed} RESULTS")
            print(f"SLEEPING FOR {TimeHelper.secondsToMinutes(DEFAULT_SLEEP_TIME_SECONDS)} MINUTES...")
            time.sleep(DEFAULT_SLEEP_TIME_SECONDS)
        except TooManyRequests as e:
            print(f"ERROR: {e}")
            print(f"SLEEPING FOR {TimeHelper.secondsToMinutes(ERROR_SLEEP_TIME_SECONDS)} MINUTES...")
            time.sleep(ERROR_SLEEP_TIME_SECONDS)
