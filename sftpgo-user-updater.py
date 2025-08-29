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

    filepath = "/credentials"
    content = request.get_json()
    
    if(os.environ['STORAGE_PROVIDER'] == "GCS"):
        
        default_permissions = ['list', 'upload', 'overwrite', 'rename', 'copy']
        
        with open(f"{filepath}/gcs-credentials.json", 'r') as credential_file:
            gcskey = json.load(credential_file)
            gcs_secret = {'status' : 'GCS', 'key' : gcskey}
        
        content['status'] = 1
        content['home_dir'] = '/'
        content['filesystem']['provider'] = Provider.GCS.value
        content['filesystem']['gcsconfig']['bucket'] = os.environ['DEFAULT_USER_BUCKET']
        content['filesystem']['gcsconfig']['automatic_credentials'] = 0
        content['filesystem']['gcsconfig']['credentials'] = gcs_secret
        content['permissions'] = {'/' : default_permissions} 
        
        app.logger.debug('RESPONDING WITH: %s', content)
        
    return jsonify(content)
    
@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
