from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/", methods=['GET'])
def get_new_user_data():
    content = request.get_json()
    app.logger.debug('Formatted Body: %s', json.dumps(content))
    
@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
