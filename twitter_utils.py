import json
import spacy
import datetime
import requests
import pandas as pd
from nltk.tokenize import TweetTokenizer


class TwitterUtils:

    def __init__(self):
        self.nlp = spacy.load('es_core_news_md')

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
        self.records = {}

    def search(self, query, next_token, start_time, max_results):
        payload = {}
        next_token = '' if next_token is None else f'next_token={next_token}'
        url = f'{self.search_url}{query}&max_results={max_results}&{next_token}&start_time={start_time}&tweet.fields=created_at'
        response = requests.request("GET", url, headers=self.headers, data=payload)

        results = json.loads(response.text.encode('utf8'))
        if "data" in results:
            for tweet in results['data']:
                self.records[tweet['id']] = tweet

        if "next_token" in results["meta"]:
            return results["meta"]['next_token'], results["meta"]["newest_id"]
        else:
            return None

    def add_tag(self, dictionary, key, value):
        if key not in dictionary:
            dictionary[key] = [value]
        elif value not in dictionary[key]:
            dictionary[key] += [value]
        return dictionary

    def get_tags(self, tweet):
        tknzr = TweetTokenizer()
        included_tags = ['LOC', 'PER', 'NOUN', 'VERB', 'PROPN', 'HASHTAGS', 'URLS', 'ORG']
        tags = {}
        key_words = []
        doc = self.nlp(tweet['text'])

        for ent in doc.ents:
            if ent.label_ in included_tags:
                tags = self.add_tag(tags, ent.label_, ent.text)
                key_words += [ent.text]

        for token in doc:
            if token.pos_ in included_tags:
                tags = self.add_tag(tags, token.pos_, token.lemma_)
                key_words += [token.lemma_]

        tweet_tokens = [token for token in tknzr.tokenize(tweet['text']) if token[0] == '#' or 'http' in token]
        for token in tweet_tokens:
            if token[0] == '#':
                tags = self.add_tag(tags, 'HASHTAGS', token)
                key_words += [token]
            elif 'http' in token:
                tags = self.add_tag(tags, 'URLS', token)
                key_words += [token]
        for key in tags:
            tweet[key] = tags[key]
        tweet['key_words'] = list(set(key_words))

        return tweet

    '''
    def store_tags(self, row):
        s3_bucket = 'tweet.watcher'
        s3_client = boto3.resource('s3')
        tags_rows = []
        for key in row['tags']:
            for value in row['tags'][key]:
                tags_rows += [(key, value, 1)]
        df = pd.DataFrame(tags_rows, columns=['tag', 'value', 'count'])
        df = df.groupby(['tag', 'value']).count()
        csv_buffer = StringIO()
        df.to_csv(csv_buffer)
        s3_client.Object(s3_bucket, f'{row["folder"]}/{row["id"]}_tags.csv').put(Body=csv_buffer.getvalue())
    '''

    def save(self, log_path, timestamp):
        tweets = [self.get_tags(self.records[key]) for key in self.records]
        tweets_df = pd.DataFrame(tweets)
        tweets_df['created_at'] = tweets_df['created_at'].apply(
            lambda date: datetime.datetime.strptime(date[:16], "%Y-%m-%dT%H:%M"))
        tweets_df['folder'] = tweets_df['created_at'].dt.strftime('%Y/%m/%d/%H')

        tweets_df.to_json(f"{log_path}/{timestamp}.json", orient="records", lines=True)


