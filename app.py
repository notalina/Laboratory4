from flask import Flask, render_template, request, redirect
import pymysql 
from typing import Dict
import sql_translator
from data_access_layer import DataAccessLayer
import logging
from flask_httpauth import HTTPBasicAuth

_sql_translator = sql_translator.SqlTranslator()


logging.basicConfig(format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger("Main")
app = Flask(__name__)
auth = HTTPBasicAuth()

user_cache = {}
 
@auth.verify_password
def verify_password(username, password):
    try:
        if username == '':
            return False
        if username in user_cache:
            return username
        logger.info("DB Authentification attempt")
        user_cache[username] = DataAccessLayer("localhost", 3306, None, username, password)
        return username
    except:
        logger.warning("Failed to authorizate as %s", username)
        return False


@app.route('/', methods=["GET", "POST"])
@auth.login_required
def index():
    return render_template('home.html', **get_databases_list())


@app.route('/<db_name>/', methods=["GET", "POST"])
@auth.login_required
def db_info(db_name):
    return render_template('index.html', **get_schema_information(db_name))

#ddl
# @app.route("/create_db", methods=["GET","POST"])
# @auth.login_required
# def create_db():
#     if request.method == 'GET':
#         return render_template('create_database.html', **get_databases_list())
#     elif request.method == 'POST':
#         return _do_create_db(request.form)

# @app.route("/drop_db", methods=["GET","POST"])
# @auth.login_required
# def drop_db():
#     if request.method == 'GET':
#         return render_template('drop_database.html', **get_databases_list())
#     elif request.method == 'POST':
#         return _do_drop_db(request.form)


@app.route('/<db_name>/create', methods=["GET", "POST"])
@auth.login_required
def create_table(db_name):
    if request.method == 'GET':
        return render_template('create_table.html', **get_schema_information(db_name))
    elif request.method == 'POST':
        return _do_create_table(db_name, request.form)

@app.route('/<db_name>/drop', methods=["GET", "POST"])
@auth.login_required
def drop_table(db_name):
    if request.method == 'GET':
        return render_template('drop_table.html',**get_schema_information(db_name))
    elif request.method == 'POST':
        return _do_drop_table(db_name, request.form)

@app.route('/<db_name>/alter', methods=["GET", "POST"])
@auth.login_required
def alter_table(db_name):
    if request.method == 'GET':
        return render_template('alter_table.html',**get_schema_information(db_name))
    elif request.method == 'POST':
        return _do_alter_table(db_name, request.form)

#dml

@app.route('/<db_name>/select', methods=["GET", "POST"])
@auth.login_required
def select_table(db_name):
    if request.method == 'GET':
        return render_template('select.html', **get_schema_information(db_name))
    elif request.method == 'POST':
        return _do_select(db_name, request.form)

@app.route('/<db_name>/update', methods=["GET", "POST"])
@auth.login_required
def update_table(db_name):
    if request.method == 'GET':
        return render_template('update.html', **get_schema_information(db_name))
    elif request.method == 'POST':
        return _do_update(db_name, request.form)

@app.route('/<db_name>/delete', methods=["GET", "POST"])
@auth.login_required
def delete_table(db_name):
    if request.method == 'GET':
        return render_template('delete.html', **get_schema_information(db_name))
    elif request.method == 'POST':
        return _do_delete(db_name, request.form)

@app.route('/<db_name>/insert', methods=["GET", "POST"])
@auth.login_required
def insert_table(db_name):
    if request.method == 'GET':
        return render_template('insert.html', **get_schema_information(db_name))
    elif request.method == 'POST':
        return _do_insert(db_name, request.form)

#others
def get_databases_list():
    #table_columns = {}
    raw_result = get_current_user_dal().select(f"SELECT schema_name FROM information_schema.schemata;")
    db_names = flat_map(raw_result)
    return {
        "db_names": db_names
    }

def get_schema_information(db_name):
    table_columns = {}
    raw_result = get_current_user_dal().select(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{db_name}';")
    table_names = flat_map(raw_result)
    for table in table_names:
        columns_raw = get_current_user_dal().select(f"SELECT column_name FROM information_schema.columns WHERE table_schema = '{db_name}' AND table_name = '{table}';")
        table_columns[table] = flat_map(columns_raw)
    return {
        "selected_db": db_name,
        "table_names": table_names, 
        "table_columns": table_columns
    }

def flat_map(list_of_list):
    return [column for row in list_of_list for column in row]

def _do_create_db(form_data: Dict):
    database_name: str = form_data["db_name"]
    query = _sql_translator.create_database_sql(database_name)
    try:
        get_current_user_dal().create_db(query)
        return handle_success(query)
    except BaseException as error:
        return handle_error(error)

def _do_drop_db(form_data: Dict):
    database_name: str = form_data["db_name"]
    query = _sql_translator.drop_database_sql(database_name)
    try:
        get_current_user_dal().drop_db(query)
        return handle_success(query)
    except BaseException as error:
        return handle_error(error)  

def _do_create_table(db_name, form_data: Dict):
    table_name:str = form_data["table_name"]
    column_amount = int(form_data["column_amount"])
    column_definitions = {}
    for i in range(column_amount):
        column_name = form_data[f"column_names[{i}]"]
        column_type = form_data[f"column_types[{i}]"]
        column_definitions[column_name] = column_type
    query = _sql_translator.create_sql(db_name, table_name, column_definitions)
    try:
        get_current_user_dal().create(query)
        return handle_success(query)
    except BaseException as error:
        return handle_error(error)

def _do_drop_table(db_name, form_data: str):
    table_name:str = form_data["table_name"]
    query = _sql_translator.drop_sql(db_name, table_name)
    try:
        get_current_user_dal().drop(query)
        return handle_success(query)
    except BaseException as error:
        return handle_error(error)

def _do_alter_table(db_name, form_data: Dict):
    table_name:str = form_data["table_name"]
    condition:str = form_data["condition"]
    query = _sql_translator.alter_sql(db_name, table_name, condition)
    try:
        get_current_user_dal().alter(query)
        return handle_success(query)
    except BaseException as error:
        return handle_error(error)

def _do_select(db_name, form_data: Dict):
    table_name:str = form_data["table_name"]
    column_names:list = [ col.strip() for col in form_data["column_names"].split(",")]
    condition:str = form_data["condition"]
    if len(condition)>0:
        query = _sql_translator.select_sql(db_name,table_name,column_names,condition)
    else:
        query = _sql_translator.select_sql(db_name,table_name,column_names)
    try:
        result = get_current_user_dal().select(query)
        return render_template('select.html',select_results=result, sql_query=query, **get_schema_information(db_name))
    except BaseException as error:
        return handle_error(error)

def _do_update(db_name, form_data: Dict):
    table_name:str = form_data["table_name"]
    column_amount = int(form_data["column_amount"])
    update_data = {}
    condition:str = form_data["condition"]
    for i in range(column_amount):
        column_name = form_data[f"column_names[{i}]"]
        column_content = form_data[f"column_values[{i}]"]
        update_data[column_name] = column_content
    query = _sql_translator.update_sql(db_name, table_name,update_data,condition)
    try:
        get_current_user_dal().update(query)
        return handle_success(query)
    except BaseException as error:
        return handle_error(error)

def _do_delete(db_name, form_data: Dict):
    table_name:str = form_data["table_name"]
    condition:str = form_data["condition"]
    query = _sql_translator.delete_sql(db_name, table_name, condition)
    try:
        get_current_user_dal().delete(query)
        return handle_success(query)
    except BaseException as error:
        return handle_error(error)

def _do_insert(db_name, form_data: Dict):
    table_name:str = form_data["table_name"]
    columns:list = [ col.strip() for col in form_data["column_names"].split(",")]
    values:list = [col.strip() for col in form_data["values"].split(",")]
    query = _sql_translator.insert_sql(db_name, table_name,columns,values)
    try:
        get_current_user_dal().insert(query)
        return handle_success(query)
    except BaseException as error:
        return handle_error(error)

def get_current_user_dal() -> DataAccessLayer :
    return user_cache[auth.current_user()
]


def handle_success(query):
    return render_template("success.html", query = query)

def handle_error(error: BaseException):
    return render_template("error.html",error=error)

if __name__ == "__main__":
    app.run(debug=True)

