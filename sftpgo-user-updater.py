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
    
    gcskey = '{"type":"service_account","project_id":"pct-kellen-hvszo","private_key_id":"d479b1837b207e0136539e7affe8afe04d414860","private_key":"-----BEGIN\
      PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDVAIMtPaCj9mI5\n7o3uSzCgJ10tqyLO38u0wPERKemqgyhsSqCj8JdAkfNDErl7rQDSFhjMeYDLgwzM\nUYsElHlWwji0JQ+EvuGPIfuG0pXu/cZjEnLVu0F0WkniXAGAHZA5f491M9QMFn/d\nw33LbjNIDh1+IREtTb338+iQQMjip0riE2o/G783XVWNMH4RySNvUI4y9Kue5P5Z\nCgG+jxpzh8PQuzlGaKic83926l21epE+Sq2UPNWLOQaM+8V1CsNufJfS8/3yKsIy\nNLB/l6l0966iQjUnezXPs60D/K6sURqVO3p4zr6pe0L/90J6McW1FQxv7qtMsNI4\nivECo2xdAgMBAAECggEABMsmVlAhNLCS6GikArVV1zRIJ6drWPEo6Y8kdtwryl7n\nVzxGAHA4Egwv9VqTxh45SK7M+yTF30oMsYFybl6iUbizvzL6dgkl1JSM4b+xbVVd\nz8d45sTTrKtGgsA4iWx3wcZdddEr0SzTKlnf04uE40k1Lceq8Z2HUNSJOJUBzhFm\nuhoshZdocR9nTvAgqwWQPQtv566O640M0qvKSXCVYcoWAsgVjP+QeJOD6YZWWf0Q\n+DZfaRylxoK9kGPjqXzGN8RJPBx0Vu2NEzVoIS//uD6HcsaMt3kNiKVJxGhIa2Ni\nnB99sxUEcVc4xOQrjnegbeaVwWIWd79o2xgODydXWQKBgQD3KwQfW2FjroeYIjBS\nlQIFmk67pAlY5O+VuORDkBD6BV2JT+e3uhv3qs3g3N0R4OvFS42yNYQIWLbwIJ4o\nDP9cgkC2TbGwkw/2il/O1MQl9ZBMWQP+SYZ+bYPNtK22D3ApS8lnZPkaC59ElqF2\nQDsETtcu2lSwZXy2UnqsjwPkiQKBgQDcnPXnmo+cFFB8X+WgPpFgKthcJJmzrBJk\nbXtjrGxKx3X75DxEZ8k9ltHK4WVy5t2E0OArvlM7YCehmV9PfnieF8soeTf7tsPc\nOuMpPKj+BA5wMxaRHtmOsJqvCp1pjbsyeWCZbyuM9grjhOmiYlZP9yJx8b7tXLIi\nnibt2908NQKBgALoY6UGyy+EBx5YEJ94F0z/kruMY3vDPbpSMYVF9Z0rYP1TjlNQ\nAjI4tTFXB9bFAaERkXouPP5oJMbQa2vnMz3gXmiGo3eDU2XAHP5u7FvR9r+fMHfW\nX5mvKiTKYlzI87XYqWbo/jE7P8VrzDx65vbXApsPgH2OxBfVApJzIEWZAoGBAJ/K\nvL5VkEFf4XBE0YDA8PFz9yS+iem+7894EVB/uixrzsR1a0Ws2vFWRXyqx51zJO4n\nkMd+YrD2E56UBZoBpAH2f/s/2dHjbngc2x6qRkk+zOptxqG0c6ZLuq6ghKXIt9d2\nXQalpCjEqdxkEAnDKntfKL7ZeA5a/tfeL5pHjzYlAoGAOTkkIkJn707Rz7a42SZf\neLYiW1OR9P9Lespbubmf07dMAdw6gktMs9IWRE7MLoDj71CJ2NHVQahd/gz7Q22l\nJB8mE6CKswPNFDJvxr1Y39fRKPSZRx4tr+pZR4sDOHPrERiLwQ1hMCosa0ejAEVi\nRGif9eqmhN1RTx4kSPUhYpU=\n-----END\
      PRIVATE KEY-----\n","client_email":"storage-admin@942859895077.iam.gserviceaccount.com","client_id":"117422648810571228972","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/storage-admin%40942859895077.iam.gserviceaccount.com","universe_domain":"googleapis.com"}'
    content = request.get_json()
    
    if(os.environ['STORAGE_PROVIDER'] == "GCS"):
        
        default_permissions = ['list', 'upload', 'overwrite', 'rename', 'copy']
        gcs_secret = {'status' : Provider.GCS.value, 'key' : gcskey}
        
        content['status'] = 1
        content['home_dir'] = '/'
        content['filesystem']['provider'] = Provider.GCS.value
        content['filesystem']['gcsconfig']['bucket'] = os.environ['DEFAULT_USER_BUCKET']
        content['filesystem']['gcsconfig']['automatic_credentials'] = 0
        content['filesystem']['gcsconfig']['credentials'] = gcs_secret
        content['permissions'] = {'/' : default_permissions} 
        
    return jsonify(content)
    
@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
