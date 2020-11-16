from flask import Blueprint, redirect, url_for,render_template, session, request
from data_access_layer import DataAccessLayer
from typing import Dict
import functools
import logging
logger = logging.getLogger("auth_module")

SESSION_USER_KEY = "username"
USER_TO_DAL = {}
# сюда вынесем всю логику с авторизацией
authentication = Blueprint('authentication', __name__, template_folder="templates")

@authentication.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        # если юзер есть в сесии то редиректим на /
        if check_authetication():
            return redirect("/") 
        else:
            return render_template("login.html")
    elif request.method == 'POST':
        if autheticate(request.form):
            return redirect("/")
        else:
            return render_template("login.html", error_message="не верные учетные данные")

@authentication.route('/logout', methods=["GET"])
def logout():
    current_username = session[SESSION_USER_KEY]
    del USER_TO_DAL[current_username]
    del session[SESSION_USER_KEY]
    return redirect(url_for('authentication.login'))

def check_authetication():
    return SESSION_USER_KEY in session

def autheticate(auth_form: Dict):
    username = auth_form['username']
    password = auth_form['password']
    try:
        # где то тут потерялась логика
        session.permanent = True
        if check_authetication():
            return username
        logger.info("DB Authentification attempt")
        dal = DataAccessLayer("localhost", 3306, None, username, password)
        _ = dal.select("select curdate() from dual;")
        session[SESSION_USER_KEY] = username
        USER_TO_DAL[username] = dal
        return True
    except BaseException as e:
        logger.warning("Failed to authorizate as %s", username, exc_info=e)
        return False

def requires_authorization(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if check_authetication():
            return f(*args, **kwargs)
        else:
            return redirect(url_for("authentication.login"))
            
    return decorated