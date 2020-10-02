import boto3

import json
import os


dynamodb = boto3.client('dynamodb')

DEFAULT_RESULTS = os.getenv('DEFAULT_RESULTS', 10)
RESTAURANTS_TABLE = os.getenv('RESTAURANTS_TABLE')


class Restaurant:

    def __init__(self, item):
        self.name = item.get('name').get('S')
        self.image = item.get('image').get('S')
        self.themes = [o.get('S') for o in item.get('themes').get('L')]

    def __repr__(self):
        return f'Restaurant<{self.name}>'


def get_restaurants(count):
    # TODO: try-except ?
    resp = dynamodb.scan(
        TableName=RESTAURANTS_TABLE,
        Limit=count,
    )
    return [Restaurant(item).__dict__ for item in resp['Items']]


def handler(event, context):
    restaurants = get_restaurants(count=DEFAULT_RESULTS)

    response = {
        "statusCode": 200,
        "body": json.dumps(restaurants)
    }

    return response
