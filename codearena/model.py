from flask_sqlalchemy import SQLAlchemy
import os
from codearena import app
from dotenv import load_dotenv

load_dotenv()

username = os.environ.get("MY_USERNAME")
password = os.environ.get("MY_PASSWORD") 
db_name = os.environ.get("MY_DB") 
host = os.environ.get("MY_HOST") 

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{username}:{password}@{host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "user"
    name = db.Column('name', db.String(50), nullable=False)
    username = db.Column('username', db.String(50), primary_key=True, nullable=False)
    email = db.Column('email', db.String(50), nullable=False, unique=True)
    password = db.Column('password', db.String(50), nullable = False)
    gender = db.Column('gender', db.String(10), nullable = False)
    college = db.Column('college', db.String(50), nullable = False)
    occupation = db.Column('profession', db.String(50), nullable = False)
    language = db.Column('languages', db.String(50), nullable = False)
    city = db.Column('city', db.String(50), nullable = False)

class Problems(db.Model):
    __tablename__ = "problems"
    name = db.Column('name', db.String(150), nullable=False)
    code = db.Column('problem code', db.String(50), primary_key=True, nullable=False)
    statement = db.Column('statement', db.String(50), nullable=False)
    input = db.Column('input', db.String(50), nullable = False)
    output = db.Column('output', db.String(10), nullable = False)
    constraint = db.Column('problem constraint', db.String(50), nullable = False)
    sampleInput = db.Column('sample input', db.String(50), nullable = False)
    sampleOutput = db.Column('sample output', db.String(50), nullable = False)
    date = db.Column('date', db.String(10), nullable = False)
