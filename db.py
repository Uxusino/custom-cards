import os
from app import app
from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL").replace("://", "ql://")
db = SQLAlchemy(app)