from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello!, World!</p>"

@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
