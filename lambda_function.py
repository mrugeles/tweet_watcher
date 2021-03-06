import json
import boto3
from urllib.parse import unquote_plus

s3_obj = boto3.client('s3')
dynamodb_client = boto3.client('dynamodb')


def get_item(record, key_word):
    return {
        'timestamp': record['created_at'],
        'id': record['id'],
        'key_word': key_word

    }


def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])

        s3_clientobj = s3_obj.get_object(Bucket=bucket, Key=key)
        s3_obj = s3_clientobj['Body'].read().decode('utf-8')
        record = json.loads(s3_obj)
        print("json loaded data")
        print(record)
        items = [get_item(record, key_word) for key_word in record['key_words']]

        print(items)

    return {
        'statusCode': 200,
        'body': json.dumps('Completed')
    }