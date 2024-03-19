from botocore.exceptions import NoCredentialsError
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from dotenv import load_dotenv
from Database.user_details import get_dynamodb_client_table, update_client_details
from Database.database import get_dynamodb_table, update_module_data, get_user_data

app = Flask(__name__)
cors = CORS(app)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

load_dotenv()

table = get_dynamodb_table()
client_table=get_dynamodb_client_table()


@app.route('/', methods=['GET'])
def insert_client_database():
    try:
        return jsonify("200 : Status Okay")
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get_user', methods=['GET'])
def get_user():
    try:
        user_id = request.args.get('userId')

        if not user_id:
            return jsonify({"error": "Missing 'cid' parameter"}), 400

        user_data = get_user_data(user_id, table)

        if user_data is not None:
            return jsonify(user_data)
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/update_user', methods=['POST'])
def update_user():
    data = request.json
    print(data)

    cid = data.get('email')
    modules_dict = data.get('modules')

    # Early return on invalid input
    if not cid or not modules_dict:
        return jsonify({"error": "Invalid input"}), 400

    try:
        # Process each module, delegate to update_module_data
        [update_module_data(table, cid, module_name, commodity_name, commodity_details)
         if module_name == 'forecasting' else
         update_module_data(table, cid, module_name, None, module_info)
         for module_name, module_info in modules_dict.items()
         for commodity_name, commodity_details in (module_info.get('commodities', {}).items()
                                                   if module_name == 'forecasting' else [(None, module_info)])]

        return jsonify({"status": "User updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update_details', methods=['POST'])
def update_details():
    data = request.json
    print(data)
    userid = data.get('userid')
    if not userid:
        return jsonify({"error": "Invalid input"}), 400
    username = data.get('username')
    email = data.get('email')
    phone = data.get('phone')
    company = data.get('company')
    if not userid or not username or not phone or not company:
        return jsonify({"error": "Invalid input. Please provide userid, username, email, phone, and company."}), 400

    table = get_dynamodb_client_table()
    success, error_message = update_client_details(table, userid, username,email, phone, company)

    if success:
        return jsonify({"success": True}), 200
    else:
        return jsonify({"error": "Failed to update client details.", "message": error_message}), 500

    #update_client_details(table, userid,username, phone, company)




if __name__ == '__main__':
    try:
        app.run(host="0.0.0.0", debug=True)
    except NoCredentialsError:
        raise Exception("Error: AWS credentials not found. Make sure to set up your credentials.")