from __future__ import division, print_function, unicode_literals

from os.path import dirname, abspath, join
from sqlite3 import connect

from flask import Flask, redirect, request, render_template

local_dir = dirname(abspath(__file__))
db_file = join(local_dir, 'todo.db')
app = Flask(__name__)


@app.route('/todo')
def todo():
    con = connect(db_file)
    c = con.cursor()
    c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
    result = c.fetchall()
    c.close()
    return render_template('todo_list.html', rows=result)


@app.route('/new-item', methods=['GET', 'POST'])
def new_item():
    if request.method == 'GET':
        return render_template('new_item.html')
    con = connect(db_file)
    c = con.cursor()
    c.execute(
        "INSERT INTO todo (task,status) VALUES (?,?)",
        (request.form['task'].strip(), 1)
    )
    con.commit()
    c.close()
    return redirect('/todo')


@app.cli.command()
def create_db():
    print('creating db')
    con = connect(db_file)
    con.execute(
        "CREATE TABLE todo "
        "(id INTEGER PRIMARY KEY, "
        "task char(100) NOT NULL, "
        "status bool NOT NULL)"
    )
    con.commit()


@app.cli.command()
def preload_db():
    con = connect(db_file)
    con.execute(
        "INSERT INTO todo (task,status) VALUES "
        "('Read A-byte-of-python to get a good introduction into Python',0)"
    )
    con.execute(
        "INSERT INTO todo (task,status) VALUES ('Visit the Python website',1)")
    con.execute(
        "INSERT INTO todo (task,status) VALUES "
        "('Test various editors for and check the syntax highlighting',1)")
    con.execute(
        "INSERT INTO todo (task,status) VALUES "
        "('Choose your favorite WSGI-Framework',0)")
    con.commit()


if __name__ == '__main__':
    app.run(debug=True)
