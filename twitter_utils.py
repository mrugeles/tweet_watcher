import json
import pandas as pd
import requests


class TwitterUtils:

    def __init__(self):

        self.consumer_key = 'rQFLsgcmxgaAj9R3d99SrgatN'
        self.consumer_secret = '1xtoU7RG65VPrODOrS3LlC9Ud3YxSWvoulSl9ry5v85U28l6O2'
        self.bearer_token = 'AAAAAAAAAAAAAAAAAAAAAA4JLwEAAAAAXIyoETwtg%2BiTlR1VTNxGXnphfu4%3D6iSv0IXHo4NWGndWWLC8Bk3XuPkLMyATMxM0h6CfomnfRbGpgK'

        self.access_token = '12538522-AQK9B1FOt4kAPtrMB52FG5qKHaCDkmFVUtGWRXHEl'
        self.access_token_secret = 'J0jSrPvmpHwj7OtnVKp3uzbAVbUPOeujcy43GqogyfAxk'

        self.search_url = 'https://api.twitter.com/2/tweets/search/recent?query='
        self.tweet_dataset = 'tweet_dataset.csv'

        self.headers = {
            'Authorization': f'Bearer {self.bearer_token}',
            'Cookie': 'personalization_id="v1_QkaLnYDqvHh1tWN9GAP18A=="; guest_id=v1%3A158255925665512507'
        }
        self.records = []

    def search(self, query, next_token, start_time, max_results):
        payload = {}
        next_token = '' if next_token is None else f'next_token={next_token}'
        url = f'{self.search_url}{query}&max_results={max_results}&{next_token}&start_time={start_time}&tweet.fields=created_at'
        response = requests.request("GET", url, headers=self.headers, data=payload)

        results = json.loads(response.text.encode('utf8'))
        with open('tweets.json', 'w') as outfile:
            json.dump(results, outfile)

        if "data" in results:
            for tweet in results['data']:
                self.records += [tweet]

        if "next_token" in results["meta"]:
            return results["meta"]['next_token'], results["meta"]["newest_id"]
        else:
            return None

    def save(self, log_path, timestamp):
        tweets_df = pd.DataFrame(self.records)
        tweets_df.to_json(f"{log_path}/{timestamp}.json", orient="records", lines=True)


