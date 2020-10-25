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

@app.route('/create', method=["GET", "POST"])
def create_table():
    if request.method == 'GET':
        return render_template('create_table.html')
    elif request.method == 'POST':
        _do_create_table(request.form)

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

