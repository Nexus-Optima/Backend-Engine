from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from datetime import datetime, timedelta
from Utils.constants import Database
import os

app = Flask(__name__)
cors = CORS(app)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

@app.route('/', methods=['GET'])
def insert_client_database():
    try:
        return jsonify("200 : Status Okay")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access = os.getenv("AWS_SECRET_ACCESS_KEY")

print(f"AWS Access Key: {aws_access_key}")
print(f"AWS Secret Access Key: {aws_secret_access}")

dynamodb = boto3.resource(
    Database.Dynamodb,
    region_name=Database.region,
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_access
)
table = dynamodb.Table(Database.table_name)

@app.route('/update_user', methods=['POST'])
def update_user():
    try:
        data = request.json

        cid = data.get(Database.Cid)
        modules = data.get(Database.Modules)

        if not cid or not modules:
            return jsonify({"error": "Invalid input"}), 400

        user_data = {
            "modules": {}
        }

        for module_name, module_info in modules.items():
            module_data = {
                # "description": f"Tool for {module_name}",
            }
            if "commodities" in module_info:
                if not module_info["commodities"]:
                    raise ValueError("Commodities field cannot be empty")
              
            if "commodities" in module_info:
                module_data["commodities"] = {}
                for commodity_name, commodity_info in module_info["commodities"].items():
                    days_to_subscribe_commodity = commodity_info.get("days_to_subscribe", 0)
                    module_data["commodities"][commodity_name] = {
                        "endDate": (datetime.now() + timedelta(days=days_to_subscribe_commodity)).strftime("%Y-%m-%d")
                    }
            else:
                days_to_subscribe_module = module_info.get("days_to_subscribe", 0)
                module_data["endDate"] = (datetime.now() + timedelta(days=days_to_subscribe_module)).strftime("%Y-%m-%d")

            user_data["modules"][module_name] = module_data

        update_user_data(cid, user_data)

        return jsonify({"status": "User updated successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_user_data(cid, user_data):
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

load_dotenv()

if __name__ == '__main__':
    try:
        app.run(host="0.0.0.0", debug=True)
    except NoCredentialsError:
        print("Error: AWS credentials not found. Make sure to set up your credentials.")
