import boto3
from botocore.exceptions import ClientError, NoCredentialsError
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


def update_module_data(table, cid, module_name, commodity_name, module_info):
    module_id = f"{cid}#{module_name}{f'#{commodity_name}' if commodity_name else ''}"
    module_data = {
        module_name: {
            **({'commodities': {commodity_name: module_info}} if commodity_name else module_info)
        }
    }

    item = {
        'userId': cid,
        'moduleId': module_id,
        'moduleData': module_data,
        'moduleName': module_name
    }

    table.put_item(Item=item)


def get_user_data(user_id, table):
    try:
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('userId').eq(user_id)
        )
        items = response.get('Items', [])

        if items:
            combined_user_data = {}
            for item in items:
                module_data = item.get('moduleData', {})
                combined_user_data[item['moduleId']] = module_data

            return combined_user_data
        else:
            print("User not found in DynamoDB")
            return None

    except NoCredentialsError:
        raise Exception("Error: AWS credentials not found. Make sure to set up your credentials.")


    except Exception as e:
        raise Exception(f"Error in get_user_data_from_database: {e}")
