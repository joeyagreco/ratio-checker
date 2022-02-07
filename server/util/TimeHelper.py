from datetime import datetime


class TimeHelper:
    SECONDS_IN_MINUTE = 60

    @classmethod
    def secondsToMinutes(cls, seconds: int) -> float:
        return seconds / cls.SECONDS_IN_MINUTE

    @staticmethod
    def printCurrentDateTime():
        # https://www.programiz.com/python-programming/datetime/strftime
        print(datetime.now().strftime("%A, %B %#d %#I:%M %p"))
