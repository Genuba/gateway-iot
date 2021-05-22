import boto3
from boto3.dynamodb.conditions import Key, Attr

DDB = boto3.resource('dynamodb','us-east-1')