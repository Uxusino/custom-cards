import os
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

CORS(app)

languages = []
with open("languages.txt", "r") as file:
    languages = file.readlines()

import routes