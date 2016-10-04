from os.path import dirname, abspath, join

from flask import Flask, redirect, request, render_template
from flask_sqlalchemy import SQLAlchemy

local_dir = dirname(abspath(__file__))
db_file = join(local_dir, 'todo.db')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_file
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, nullable=False)
    text = db.Column(db.String)


@app.route('/')
@app.route('/todo')
def todo():
    items = Item.query.filter_by(active=True).all()
    return render_template('todo_list.html', rows=items)


@app.route('/new-item', methods=['GET', 'POST'])
def new_item():
    if request.method == 'GET':
        return render_template('new_item.html')
    db.session.add(Item(text=request.form['task'].strip(), active=True))
    db.session.commit()
    return redirect('/todo')


@app.route('/edit-item/<number>', methods=['GET', 'POST'])
def edit_item(number):
    item = Item.query.filter_by(id=number).first()
    if request.method == 'GET':
        return render_template('edit_item.html', old=item)
    item.text = request.form['task'].strip()
    item.active = request.form['status'] == 'open'
    db.session.add(item)
    db.session.commit()
    return redirect('/todo')


@app.cli.command()
def create_db():
    print('creating db')
    db.create_all()


def preload_db():
    print('loading default db')
    db.session.add_all([
        Item(
            text='Read A-byte-of-python to get a good introduction into Python',
            active=False,
        ),
        Item(
            text='Visit the Python website',
            active=True,
        ),
        Item(
            text='Test various editors for and check the syntax highlighting',
            active=True,
        ),
        Item(
            text='Choose your favorite WSGI-Framework',
            active=False,
        )
    ])
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
