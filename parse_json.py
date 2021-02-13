import json
import time
import spacy
import tqdm
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


if __name__ == '__main__':
    start_time = time.time()
    with open('backup/1357758169083215874.json') as json_file:
        data = json.load(json_file)
        records = [f"{get_tags(record)}\n" for record in tqdm.tqdm(data['data'])]
        file = open("records.log", "w")
        file.writelines(records)
    print("--- %s seconds ---" % (time.time() - start_time))

