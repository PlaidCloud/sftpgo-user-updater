from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/", methods=['GET'])
def get_new_user_data():
    content = request.get_json()
    print(json.dumps(content))
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
