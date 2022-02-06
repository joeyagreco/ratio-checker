import time
from functools import wraps


def timer(func):
    # runs timer on wrapped function
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            funcName = f"{func.__qualname__}()"
        except:
            funcName = "unknownMethod"
        startTime = time.time()
        ret = func(*args, **kwargs)
        endTime = time.time()
        runtimeSecondsList = str(endTime - startTime).split('.')
        runtimeSeconds = f"{runtimeSecondsList[0]}.{runtimeSecondsList[1][:2]}"
        print(f"--- Function {funcName} ran in {runtimeSeconds} seconds ---\n")
        return ret

    return wrapper
