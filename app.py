import time
from flask import Flask, render_template, request, redirect
import pymysql 
from typing import Dict
import sql_translator
import data_access_layer

_sql_translator = sql_translator.SqlTranslator()
dal = data_access_layer.DataAccessLayer("localhost", 3306, "flask_user", "flask_user", "flask_user")
app = Flask(__name__)


@app.route('/')
def start():
    return render_template('index.html')

#ddl

@app.route('/create', methods=["GET", "POST"])
def create_table():
    if request.method == 'GET':
        return render_template('create_table.html')
    elif request.method == 'POST':
        _do_create_table(request.form)

@app.route('/drop', methods=["GET", "POST"])
def drop_table():
    if request.method == 'GET':
        return render_template('drop_table.html')
    elif request.method == 'POST':
        _do_drop_table(request.form)

@app.route('/alter', methods=["GET", "POST"])
def alter_table():
    if request.method == 'GET':
        return render_template('alter_table.html')
    elif request.method == 'POST':
        _do_alter_table(request.form)

#dml

@app.route('/select', methods=["GET", "POST"])
def select_table():
    if request.method == 'GET':
        return render_template('select_table.html')
    elif request.method == 'POST':
        _do_select(request.form)

@app.route('/update', methods=["GET", "POST"])
def update_table():
    if request.method == 'GET':
        return render_template('update_table.html')
    elif request.method == 'POST':
        _do_update(request.form)

@app.route('/delete', methods=["GET", "POST"])
def delete_table():
    if request.method == 'GET':
        return render_template('delete_table.html')
    elif request.method == 'POST':
        _do_delete(request.form)

@app.route('/insert', methods=["GET", "POST"])
def insert_table():
    if request.method == 'GET':
        return render_template('insert_table.html')
    elif request.method == 'POST':
        _do_insert(request.form)

#others

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
    column_names:list = form_data["column_names"]
    condition:str = form_data["condition"]
    if len(condition)>0:
        query = _sql_translator.select_sql(table_name,column_names,condition)
    else:
        query = _sql_translator.select_sql(table_name,column_names)
    try:
        result = dal.select(query)
        return render_template('select.html',results=result)
    except BaseException as error:
        return handle_error(error)

def _do_update(form_data: Dict):
    table_name:str = form_data["table_name"]
    column_names: list = form_data["column_names"]
    column_content: list = form_data["column_content"]
    condition:str = form_data["conditon"]
    update_data = {column_names[i]:column_content for i in range(len(column_names))}
    if len(condition)>0:
        query = _sql_translator.update_sql(table_name,update_data,condition)
    else:
        query = _sql_translator.update_sql(table_name,update_data)
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
    columns:list = form_data["columns"]
    values:list = form_data["values"]
    query = _sql_translator.insert_sql(table_name,columns,values)
    try:
        dal.insert(query)
        return handle_success(query)
    except BaseException as error:
        return handle_error(error)


def handle_success(query):
    return render_template("success.html")

def handle_error(error: BaseException):
    return f"<h1 >{error}</h1>"

if __name__ == "__main__":
    app.run(debug=True)

