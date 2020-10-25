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

@app.route('/create', method=["GET", "POST"])
def create_table():
    if request.method == 'GET':
        return render_template('create_table.html')
    elif request.method == 'POST':
        _do_create_table(request.form)

@app.route('/drop', method=["GET", "POST"])
def drop_table():
    if request.method == 'GET':
        return render_template('drop_table.html')
    elif request.method == 'POST':
        _do_drop_table(request.form)

@app.route('/alter', method=["GET", "POST"])
def alter_table():
    if request.method == 'GET':
        return render_template('alter_table.html')
    elif request.method == 'POST':
        _do_alter_table(request.form)

#dml

@app.route('/select', method=["GET", "POST"])
def select_table():
    if request.method == 'GET':
        return render_template('select_table.html')
    elif request.method == 'POST':
        _do_select(request.form)

@app.route('/update', method=["GET", "POST"])
def update_table():
    if request.method == 'GET':
        return render_template('update_table.html')
    elif request.method == 'POST':
        _do_update(request.form)

@app.route('/delete', method=["GET", "POST"])
def delete_table():
    if request.method == 'GET':
        return render_template('delete_table.html')
    elif request.method == 'POST':
        _do_delete(request.form)

@app.route('/insert', method=["GET", "POST"])
def insert_table():
    if request.method == 'GET':
        return render_template('insert_table.html')
    elif request.method == 'POST':
        _do_insert(request.form)


def _do_create_table(form_data: Dict):
    table_name:str = form_data["table_name"]
    column_names: list = form_data["column_names"]
    column_types: list = form_data["column_types"]
    column_definitions = {column_names[i]:column_types for i in range(len(column_names))}
    query = _sql_translator.create_sql(table_name, column_definitions)
    try:
        dal.create(query)
        return f"<h1 style='color:green'>The query '${query} executed'</h1>"
    except BaseException as error:
        return f"<h1 >{error}</h1>"

def _do_drop_table(form_data: str):
    table_name:str = form_data;
    query = _sql_translator.drop_sql(table_name)
    try:
        dal.drop(query)
        return f"<h1 style='color:green'>The query '${query} executed'</h1>"
    except BaseException as error:
        return f"<h1 >{error}</h1>"

def _do_alter_table(form_data: Dict)
    table_name:str = form_data["table_name"]
    column_names:str = form_data["condition"]
    query = _sql_translator.alter_sql(table_name, condition)
    try:
        dal.alter(query)
        return f"<h1 style='color:green'>The query '${query} executed'</h1>"
    except BaseException as error:
        return f"<h1 >{error}</h1>"

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
        return f"<h1 >{error}</h1>"

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
        return f"<h1 style='color:green'>The query '${query} executed'</h1>"
    except BaseException as error:
        return f"<h1 >{error}</h1>"

def _do_delete(form_data: Dict):
    table_name:str = form_data["table_name"]
    condition:str = form_data["condition"]
    query = _sql_translator.delete_sql(table_name, condition)
    try:
        dal.delete(query)
        return f"<h1 style='color:green'>The query '${query} executed'</h1>"
    except BaseException as error:
        return f"<h1 >{error}</h1>"

def _do_insert(form_data: Dict):
    table_name:str = form_data["table_name"]
    columns:list = form_data["columns"]
    values:list = form_data["values"]
    query = _sql_translator.insert_sql(table_name,columns,values)
    try:
        dal.insert(query)
        return f"<h1 style='color:green'>The query '${query} executed'</h1>"
    except BaseException as error:
        return f"<h1 >{error}</h1>"

if __name__ == "__main__":
    app.run(debug=True)

"""
<input type="text" name="column_names[]" value="comment1"/>
<input type="text" name="column_names[]" value="comment2"/>
<input type="text" name="column_names[]" value="comment3"/>
<input type="text" name="column_names[]" value="comment4"/>


<input type="text" name="column_types[]" value="comment1"/>
<input type="text" name="column_types[]" value="comment2"/>
<input type="text" name="column_types[]" value="comment3"/>
<input type="text" name="column_types[]" value="comment4"/>

https://www.postman.com/downloads/
"""

