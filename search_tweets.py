import sys
import time
import datetime
from twitter_utils import TwitterUtils

month_limit = 500000

twitterUtils = TwitterUtils()

if __name__ == '__main__':

    log_path = sys.argv[1]
    search_query = open(sys.argv[2], "r").read()
    frequency = int(sys.argv[3])
    max_results = 11*frequency
    if max_results < 10:
        max_results = 10
    elif max_results > 100:
        max_results = 100
    start = time.time()
    next_token = None
    newest_id = None
    prev_token = "000"
    timestamp = datetime.datetime.now() - datetime.timedelta(minutes=frequency)
    timestamp_twitter = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
    timestamp_long = timestamp.strftime("%Y%m%d%H%M%S")
    while prev_token != next_token:
        prev_token = next_token
        result = twitterUtils.search(search_query, next_token, timestamp_twitter, max_results)
        if result is not None:
            next_token, newest_id = result
        time.sleep(5)

    twitterUtils.save(log_path, timestamp_twitter)
    end = time.time()
    print(f"Elapsed time {(end-start)/60} mins.")
