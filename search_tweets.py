import sys
import time
import datetime
from twitter_utils import TwitterUtils


twitterUtils = TwitterUtils()

if __name__ == '__main__':

    log_path = sys.argv[1]
    search_query = open(sys.argv[2], "r").read()

    start = time.perf_counter()
    next_token = None
    newest_id = None
    prev_token = "000"
    timestamp = datetime.datetime.now() - datetime.timedelta(minutes=5)
    timestamp_twitter = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
    timestamp_long = timestamp.strftime("%Y%m%d%H%M%S")
    while prev_token != next_token:
        prev_token = next_token
        result = twitterUtils.search(search_query, next_token, timestamp_twitter)
        if result is not None:
            next_token, newest_id = result
        time.sleep(5)

    twitterUtils.save(log_path, timestamp_long)
