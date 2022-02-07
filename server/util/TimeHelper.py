class TimeHelper:
    SECONDS_IN_MINUTE = 60

    @classmethod
    def secondsToMinutes(cls, seconds: int) -> float:
        return seconds / cls.SECONDS_IN_MINUTE
