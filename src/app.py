from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from dotenv import load_dotenv
from Database.database import get_dynamodb_table, update_user_data
from Utils.constants import Database
from Utils.database_utils import forecast_tool,other_tools


app = Flask(__name__)
cors = CORS(app)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

load_dotenv()

table = get_dynamodb_table()

@app.route('/', methods=['GET'])
def insert_client_database():
    try:
        return jsonify("200 : Status Okay")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update_user', methods=['POST'])
def update_user():
    try:
        data = request.json

        cid = data.get(Database.Cid)
        modules = data.get(Database.Modules)

        if not cid or not modules:
            return jsonify({"error": "Invalid input"}), 400

        user_data = {}

        for module_name, module_info in modules.items():
            module_data = {}
            
            case_handlers = {
                "commodities": forecast_tool,
                "default": other_tools,
            }
            
            case_key = "commodities" if "commodities" in module_info else "default"
            case_handlers[case_key](module_info, module_data)

            user_data[module_name] = module_data

        update_user_data(table, cid, user_data)

        return jsonify({"status": "User updated successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    try:
        app.run(host="0.0.0.0", debug=True)
    except NoCredentialsError:
        print("Error: AWS credentials not found. Make sure to set up your credentials.")
