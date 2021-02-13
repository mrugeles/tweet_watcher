import os
import time
import datetime
from twitter_utils import TwitterUtils


twitterUtils = TwitterUtils()

if __name__ == '__main__':

    query = '(from:elespectador OR from:ELTIEMPO OR from:AP_Noticias OR from:NoticiasUno OR from:larepublica_co OR ' \
            'from:dw_espanol)  -is:retweet lang:es '

    start = time.perf_counter()
    next_token = None
    newest_id = None
    prev_token = "000"
    total = 0
    timestamp = datetime.datetime.now() - datetime.timedelta(minutes=5)
    timestamp = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
    while prev_token != next_token:
        prev_token = next_token
        result = twitterUtils.search(query, next_token, timestamp)
        if result is not None:
            next_token, newest_id = result
        time.sleep(5)

    twitterUtils.save(timestamp)
