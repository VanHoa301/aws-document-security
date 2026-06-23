from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

from routes.auth import auth_bp
from routes.documents import documents_bp

app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(documents_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
