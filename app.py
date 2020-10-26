import time
from flask import Flask, render_template, request, redirect
import pymysql 
from typing import Dict
import sql_translator
import data_access_layer

_sql_translator = sql_translator.SqlTranslator()
db_user = db_password = db_name = "flask_user"

dal = data_access_layer.DataAccessLayer("localhost", 3306, db_user, db_name, db_password)
app = Flask(__name__)


@app.route('/')
def start():
    return render_template('index.html',**get_schema_information())

#ddl

@app.route('/create', methods=["GET", "POST"])
def create_table():
    if request.method == 'GET':
        return render_template('create_table.html')
    elif request.method == 'POST':
        return _do_create_table(request.form)

@app.route('/drop', methods=["GET", "POST"])
def drop_table():
    if request.method == 'GET':
        return render_template('drop_table.html',**get_schema_information())
    elif request.method == 'POST':
        return _do_drop_table(request.form)

@app.route('/alter', methods=["GET", "POST"])
def alter_table():
    if request.method == 'GET':
        return render_template('alter_table.html',**get_schema_information())
    elif request.method == 'POST':
        return _do_alter_table(request.form)

#dml

@app.route('/select', methods=["GET", "POST"])
def select_table():
    if request.method == 'GET':
        return render_template('select.html', **get_schema_information())
    elif request.method == 'POST':
        return _do_select(request.form)

@app.route('/update', methods=["GET", "POST"])
def update_table():
    if request.method == 'GET':
        return render_template('update.html',**get_schema_information())
    elif request.method == 'POST':
        return _do_update(request.form)

@app.route('/delete', methods=["GET", "POST"])
def delete_table():
    if request.method == 'GET':
        return render_template('delete.html')
    elif request.method == 'POST':
        return _do_delete(request.form)

@app.route('/insert', methods=["GET", "POST"])
def insert_table():
    if request.method == 'GET':
        return render_template('insert.html',**get_schema_information())
    elif request.method == 'POST':
        return _do_insert(request.form)

#others

def get_schema_information():
    table_columns = {}
    raw_result = dal.select(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{db_name}';")
    table_names = flat_map(raw_result)
    for table in table_names:
        columns_raw = dal.select(f"SELECT column_name FROM information_schema.columns WHERE table_schema = '{db_name}' AND table_name = '{table}';")
        table_columns[table] = flat_map(columns_raw)
    return {
        "table_names": table_names, 
        "table_columns": table_columns
    }

def flat_map(list_of_list):
    return [column for row in list_of_list for column in row]

def _do_create_table(form_data: Dict):
    table_name:str = form_data["table_name"]
    column_amount = int(form_data["column_amount"])
    column_definitions = {}
    for i in range(column_amount):
        column_name = form_data[f"column_names[{i}]"]
        column_type = form_data[f"column_types[{i}]"]
        column_definitions[column_name] = column_type
    query = _sql_translator.create_sql(table_name, column_definitions)
    try:
        dal.create(query)
        return handle_success(query)
    except BaseException as error:
        return handle_error(error)

def _do_drop_table(form_data: str):
    table_name:str = form_data["table_name"]
    query = _sql_translator.drop_sql(table_name)
    try:
        dal.drop(query)
        return handle_success(query)
    except BaseException as error:
        return handle_error(error)

def _do_alter_table(form_data: Dict):
    table_name:str = form_data["table_name"]
    condition:str = form_data["condition"]
    query = _sql_translator.alter_sql(table_name, condition)
    try:
        dal.alter(query)
        return handle_success(query)
    except BaseException as error:
        return handle_error(error)

def _do_select(form_data: Dict):
    table_name:str = form_data["table_name"]
    column_names:list = [ col.strip() for col in form_data["column_names"].split(",")]
    condition:str = form_data["condition"]
    if len(condition)>0:
        query = _sql_translator.select_sql(table_name,column_names,condition)
    else:
        query = _sql_translator.select_sql(table_name,column_names)
    try:
        result = dal.select(query)
        return render_template('select.html',select_results=result, sql_query=query, **get_schema_information())
    except BaseException as error:
        return handle_error(error)

def _do_update(form_data: Dict):
    table_name:str = form_data["table_name"]
    column_amount = int(form_data["column_amount"])
    update_data = {}
    condition:str = form_data["condition"]
    for i in range(column_amount):
        column_name = form_data[f"column_names[{i}]"]
        column_content = form_data[f"column_values[{i}]"]
        update_data[column_name] = column_content
    query = _sql_translator.update_sql(table_name,update_data,condition)
    try:
        dal.update(query)
        return handle_success(query)
    except BaseException as error:
        return handle_error(error)

def _do_delete(form_data: Dict):
    table_name:str = form_data["table_name"]
    condition:str = form_data["condition"]
    query = _sql_translator.delete_sql(table_name, condition)
    try:
        dal.delete(query)
        return handle_success(query)
    except BaseException as error:
        return handle_error(error)

def _do_insert(form_data: Dict):
    table_name:str = form_data["table_name"]
    columns:list = [ col.strip() for col in form_data["column_names"].split(",")]
    values:list = [col.strip() for col in form_data["values"].split(",")]
    query = _sql_translator.insert_sql(table_name,columns,values)
    try:
        dal.insert(query)
        return handle_success(query)
    except BaseException as error:
        return handle_error(error)


def handle_success(query):
    return render_template("success.html", query = query)

def handle_error(error: BaseException):
    #TODO: replace to template
    return f"<h1 >{error}</h1>"

if __name__ == "__main__":
    app.run(debug=True)

