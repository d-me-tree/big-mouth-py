import json

import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('restaurants')

with open('scripts/restaurants.json', 'r') as f:
    restaurants = json.load(f)

with table.batch_writer() as batch:
    for item in restaurants:
        batch.put_item(Item=item)
