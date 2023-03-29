import os
from flask import Flask

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

import routes