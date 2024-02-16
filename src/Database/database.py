import boto3
from botocore.exceptions import ClientError,NoCredentialsError
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
        for module_name, module_info in user_data.items():
            # For each module, generate a unique moduleId (e.g., by combining user ID and module name)
            # This assumes that module_name is a unique identifier for each type of module.
            module_id = f"{cid}#{module_name}"
 
            # Prepare the item to be updated/inserted in DynamoDB
            item = {
                'userId': cid,
                'moduleName':module_name,
                'moduleId': module_id,
                'moduleData': module_info,  # Storing the entire module info under 'moduleData'
                # Add other attributes as needed
            }

            # Insert/Update the item in DynamoDB
            table.put_item(Item=item)
            
    except ClientError as e:
         raise Exception(f"Error updating user data in DynamoDB: {e}")
    
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