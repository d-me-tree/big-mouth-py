import os
from datetime import date
from urllib.parse import urlparse

import pymustache
import requests
from aws_requests_auth.boto_utils import BotoAWSRequestsAuth


html = None

RESTAURANTS_API_ROOT = os.getenv('RESTAURANTS_API_ROOT')
auth = BotoAWSRequestsAuth(aws_host=urlparse(RESTAURANTS_API_ROOT).hostname,
                           aws_region=os.environ.get('AWS_REGION'),
                           aws_service='execute-api')


def load_html():
    global html

    if html is None:
        with open('static/index.html', 'r') as f:
            html = f.read()

    return html


def get_restaurants():
    response = requests.get(RESTAURANTS_API_ROOT, auth=auth)
    return response.json()


def handler(event, context):
    template = load_html()
    restaurants = get_restaurants()
    html = pymustache.render(template, {
        'dayOfWeek': date.today().strftime('%A'),
        'restaurants': restaurants
        })

    response = {
        'statusCode': 200,
        'body': html,
        'headers': {
            'Content-Type': 'text/html; charset=UTF-8'
            },
    }

    return response
