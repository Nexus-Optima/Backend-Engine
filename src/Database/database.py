import boto3
from botocore.exceptions import ClientError
from Utils.constants import Database
import os

def get_dynamodb_table():
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access = os.getenv("AWS_SECRET_ACCESS_KEY")

    dynamodb = boto3.resource(
        Database.Dynamodb,
        region_name=Database.region,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_access
    )
    
    table = dynamodb.Table(Database.table_name)
    return table

def update_user_data(table, cid, user_data):
    try:
        table.put_item(
            Item={
                'cid': cid,
                'data': user_data
            }
        )
        print(f"Data added to DynamoDB for CID: {cid}")
    except ClientError as e:
        raise Exception(f"Error updating user data in DynamoDB: {e}")
