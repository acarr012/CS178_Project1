import boto3
from boto3.dynamodb.conditions import Key
import creds

# DynamoDB Connection
session = boto3.Session()
dynamodb = session.resource('dynamodb')
travel_log_table = dynamodb.Table('UserTravelLog')

def add_travel_log(username, log_id, country, rating):
    try:
        travel_log_table.put_item(Item={
            'username': username,
            'log_id': log_id,
            'country': country,
            'rating': rating
        })
        return True, 'Trip logged successfully!'
    except Exception as e:
        return False, f'Error: {str(e)}'

def get_all_travel_logs():
    try:
        response = travel_log_table.scan()
        return response.get('Items', [])
    except Exception as e:
        return [], f'Error: {str(e)}'

