from flask import Flask, request, jsonify
import json
from enum import Enum
import os


class Provider(Enum):
    Local = 0
    S3 = 1
    GCS = 2
    Azure = 3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def get_new_user_data():
    
    content = request.get_json()
    
    if(os.environ['STORAGE_PROVIDER'] == "GCS"):
        
        content['filesystem']['provider'] = Provider.GCS.value
        content['filesystem']['gcsconfig']['bucket'] = os.environ['DEFAULT_USER_BUCKET']
        content['filesystem']['gcsconfig']['automatic_credentials'] = 1
        content['permissions']['/'] = ["*"]
        
    return jsonify(content)
    
@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
