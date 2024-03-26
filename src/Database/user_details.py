import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from flask import jsonify
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

def update_client_details(table,data):
    userid = data.get('userid')
    if not userid:
        return jsonify({"error": "Invalid input"}), 400
    username = data.get('username')
    email = data.get('email')
    phone = data.get('phone')
    company = data.get('company')
    if not userid or not username or not phone or not company:
        return jsonify({"error": "Invalid input. Please provide userid, username, email, phone, and company."}), 400
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


def get_user_details(email, table):
    try:
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('email').eq(email)
        )
        items = response.get('Items', [])
        return items

    except NoCredentialsError:
        raise Exception("Error: AWS credentials not found. Make sure to set up your credentials.")
    except Exception as e:
        raise Exception(f"Error in get_user_data_from_database: {e}")


def update_personal_details(table, data):
    email = data.get('email')
    if not email:
        return jsonify({"error": "Invalid input"}), 400
    username = data.get('username')
    userid = data.get('userid')
    phone = data.get('phone')
    company = data.get('company')
    if not username or not phone or not company:
        return jsonify({"error": "Invalid input. Please provide userid, username, email, phone, and company."}), 400

    try:
        response=table.update_item(
            Key={
                'email': email
            },
            UpdateExpression='set userid = :userid, username = :username, phone = :phone, company = :company',
            ExpressionAttributeValues={
                ':userid': userid,
                ':username': username,
                ':phone': phone,
                ':company': company
            },
            ReturnValues='UPDATED_NEW'
        )
        updated_user=response.get('Attributes',[])
        return True, updated_user
    except Exception as e:
        return False, str(e)






