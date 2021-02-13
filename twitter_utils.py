import json
import requests
import spacy
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
        self.records = []

    def search(self, query, next_token, start_time):
        payload = {}
        next_token = '' if next_token is None else f'next_token={next_token}'
        url = f'{self.search_url}{query}&max_results=100&{next_token}&start_time={start_time}'
        response = requests.request("GET", url, headers=self.headers, data=payload)

        results = json.loads(response.text.encode('utf8'))
        self.records += results['data']

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
        excluded_tags = ['MISC', 'PUNCT', 'ADJ', 'ADP', 'DET']
        tags = {}
        doc = self.nlp(tweet['text'])

        for ent in doc.ents:
            if ent.label_ not in excluded_tags:
                tags = self.add_tag(tags, ent.label_, ent.text)

        for token in doc:
            if token.pos_ not in excluded_tags:
                tags = self.add_tag(tags, token.pos_, token.lemma_)

        tweet_tokens = [token for token in tknzr.tokenize(tweet['text']) if token[0] == '#' or 'http' in token]
        for token in tweet_tokens:
            if token[0] == '#':
                tags = self.add_tag(tags, 'HASHTAGS', token)
            elif 'http' in token:
                tags = self.add_tag(tags, 'URLS', token)
        tweet['tags'] = tags
        return tweet

    def save(self, start_time):
        records = [f"{self.get_tags(record)}\n" for record in self.records]
        file = open(f"datasets/{start_time}.log", "w")
        file.writelines(records)

