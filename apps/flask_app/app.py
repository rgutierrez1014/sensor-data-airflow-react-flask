import logging

from flask import Flask, request
from flask_cors import CORS

UPLOAD_FOLDER = '/tmp/uploads'


def create_app():
    app = Flask(__name__)
    CORS(app)


    @app.route("/")
    def hello():
        return "Hello, World!"


    @app.route('/get-current-data', methods=['GET'])
    def get_current_data():
        return {}
        
    return app
    
app = create_app()