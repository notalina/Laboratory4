import time
from flask import Flask, render_template, request, redirect
import pymysql 
db = pymysql.connect("localhost", "flask_user", "flask_user", "flask_user", port=3306)
app = Flask(__name__)

@app.route('/', methods=["POST","GET"])
def start():
    return render_template('index.html')

@app.route('/time')
def tim():
    t = time.ctime(time.time())
    return render_template('time.html', current_time=t)

@app.route('/select')
def selectTable():
    cursor = db.cursor()
    sql = "SELECT * FROM examples"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template('select.html', results=results)

@app.route('/show')
def showTables():
    cursor = db.cursor()
    sql = "SHOW TABLES FROM flask_user"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template('show.html', results=results)

# if __name__ == "__main__":
#     app.run(debug=True)