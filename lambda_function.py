import requests

import json
import spacy
from nltk.tokenize import TweetTokenizer


def add_tag(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = [value]
    elif value not in dictionary[key]:
        dictionary[key] += [value]
    return dictionary


def get_tags(tweet):
    nlp = spacy.load('es_core_news_lg')
    tknzr = TweetTokenizer()
    excluded_tags = ['MISC', 'PUNCT', 'ADJ', 'ADP', 'DET']
    tags = {}
    doc = nlp(tweet['text'])

    for ent in doc.ents:
        if ent.label_ not in excluded_tags:
            tags = add_tag(tags, ent.label_, ent.text)

    for token in doc:
        if token.pos_ not in excluded_tags:
            tags = add_tag(tags, token.pos_, token.lemma_)

    tweet_tokens = [token for token in tknzr.tokenize(tweet['text']) if token[0] == '#' or 'http' in token]
    for token in tweet_tokens:
        if token[0] == '#':
            tags = add_tag(tags, 'HASHTAGS', token)
        elif 'http' in token:
            tags = add_tag(tags, 'URLS', token)
    tweet['tags'] = tags
    return tweet


def lambda_handler(event, context):
    tweet = {"id": "1358491216770306048", "text": "Ibrahimovic lleg\u00f3 al gol 500 en clubes y le dio tambi\u00e9n el liderato a Milan. https://t.co/2rbId8OHzb https://t.co/c3nbQZGTio"}
    tweet = get_tags(tweet)
    print(tweet)
    return None