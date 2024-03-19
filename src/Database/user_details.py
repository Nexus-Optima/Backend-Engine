import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from src.Utils.constants import Database
import os


def get_dynamodb_client_table():
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access = os.getenv("AWS_SECRET_ACCESS_KEY")

    dynamodb = boto3.resource(
        Database.Dynamodb,
        region_name=Database.region,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_access
    )

    table = dynamodb.Table(Database.client_table)
    return table

def update_client_details(table, userid, username,email, phone, company):
    try:
        item = {
            'userid': userid,
            'username': username,
            'email': email,
            'phone': phone,
            'company': company,
        }
        table.put_item(Item=item)
        return True, None  # Operation succeeded
    except ClientError as e:
        error_message = e.response['Error']['Message']
        return False, error_message




