import time

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
    numberOfTweetsToHarvest = 100
    numberOfResultsToServe = 100
    while True:
        print("HARVESTING TWEETS")
        numberOfTweetsHarvested = ratioService.harvestRatioReplies(numberOfTweetsToHarvest)
        print(f"HARVESTED {numberOfTweetsHarvested} TWEETS")
        numberOfResultsServed = ratioService.serveRatioResults(numberOfResultsToServe)
        print(f"SERVED {numberOfResultsServed} RESULTS")
        # sleep for 1 hour
        time.sleep(3600)
