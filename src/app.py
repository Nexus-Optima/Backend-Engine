from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from dotenv import load_dotenv

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


load_dotenv()

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)