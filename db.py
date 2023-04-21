import os
import time
from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError

def execute(query, params, max_retries=3, delay=1):
    for attempt in range(max_retries):
        try:
            result = db.session.execute(query, params)
            return result
        except OperationalError as e:
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                raise

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL").replace("://", "ql://")
db = SQLAlchemy(app)