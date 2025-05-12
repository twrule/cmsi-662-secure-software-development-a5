import os
import sqlite3
import datetime
from functools import wraps
from flask import request, g, render_template
from passlib.hash import pbkdf2_sha256
import jwt
from dotenv import load_dotenv

load_dotenv()
# Load environment variables from .env file
SECRET = os.getenv('SECRET')


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not logged_in():
            return render_template('login.html')
        return func(*args, **kwargs)
    return wrapper


def get_user_with_credentials_safe(email, password):
    try:
        con = sqlite3.connect('bank.db')
        cur = con.cursor()
        cur.execute('''
            SELECT email, name, password FROM users where email=?''',
                    (email,))
        row = cur.fetchone()
        # Initial Hash verification to prevent user_enumeration
        # If the user does not exist, we still hash a dummy password
        if row is None:
            pbkdf2_sha256.verify(
                password, pbkdf2_sha256.hash('dummy_password'))
            return None
        email, name, hash = row
        if not pbkdf2_sha256.verify(password, hash):
            return None
        return {"email": email, "name": name, "token": create_token(email)}
    finally:
        con.close()


def logged_in():
    token = request.cookies.get('auth_token')
    try:

        data = jwt.decode(token, SECRET, algorithms=['HS256'])
        g.user = data['sub']
        return True
    except jwt.InvalidTokenError:
        return False


def create_token(email):
    now = datetime.datetime.now(datetime.timezone.utc)
    payload = {'sub': email, 'iat': now,
               'exp': now + datetime.timedelta(minutes=60)}
    token = jwt.encode(payload, SECRET, algorithm='HS256')
    return token
