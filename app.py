from flask import Flask, redirect, request, render_template
from flask.helpers import url_for
from werkzeug.exceptions import abort

app = Flask(__name__)
todo_list = []


class ToDoItem:
    def __init__(self, text, active=True):
        self.text = text
        self.active = active
        self.id = id(self)

    @staticmethod
    def get_by_id(number):
        for item in todo_list:
            if item.id == number:
                return item


@app.route('/')
@app.route('/todo')
def index():
    active = [i for i in todo_list if i.active]
    return render_template('list.html', title='Tasks', rows=active)


@app.route('/new-item', methods=['GET', 'POST'])
def new_item():
    if request.method == 'GET':
        return render_template('new_item.html')
    todo_list.append(ToDoItem(text=request.form['task'].strip(), active=True))
    return redirect(url_for('index'))


@app.route('/edit-item/<int:number>', methods=['GET', 'POST'])
def edit_item(number):
    item = ToDoItem.get_by_id(number) or abort(400)
    if request.method == 'GET':
        return render_template('edit_item.html', old=item)
    item.text = request.form['task'].strip()
    item.active = request.form['status'] == 'open'
    return redirect(url_for('index'))


@app.route('/old-items')
def deleted_items():
    items = [item for item in todo_list if not item.active]
    return render_template('list.html', title='Completed', rows=items)


if __name__ == '__main__':
    app.run(debug=True)
