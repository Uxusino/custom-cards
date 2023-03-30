import os
from flask import Flask

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

languages = []
with open("languages.txt", "r") as file:
    languages = file.readlines()

import routes