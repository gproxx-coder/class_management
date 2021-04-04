from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask import session

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1111@localhost/classdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Setting up secret key for Session handling
app.config['SECRET_KEY'] = "GXB^txn39Y^&#(*xy9%^@#$%NMHgdiGd7s8^&*(Ne903YY"

# Mail setup
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'fashionadda.ab@gmail.com'
app.config['MAIL_PASSWORD'] = 'Fuck@777'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

db = SQLAlchemy(app)

mail = Mail(app)