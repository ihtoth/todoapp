from flask import Flask, render_template, request, redirect

app = Flask(__name__)


class ToDoItem(object):
    def __init__(self, text, active=True):
        self.text = text
        self.active = active
        self.id = id(self)

    @staticmethod
    def get_by_id(number):
        for item in todo_list:
            if item.id == number:
                return item

    def __repr__(self):
        return "ToDoItem('%s', active=%s)" % (self.text, self.active)


todo_list = [
    ToDoItem('feed the fish'),
    ToDoItem('clean the house', active=False),
    ToDoItem('win the lottery'),
]


@app.route('/')
def index():
    active = [i for i in todo_list if i.active]
    return render_template('list.html', title='To Do List', rows=active)


@app.route('/completed-items/')
def completed_items():
    completed = [i for i in todo_list if not i.active]
    return render_template('list.html', title='Completed Items', rows=completed)


@app.route('/edit-item/<int:number>', methods=['GET', 'POST'])
def edit_item(number):
    item = ToDoItem.get_by_id(number)
    if request.method == 'GET':
        return render_template('edit_item.html', old=item)
    item.text = request.form['task']
    active = request.form['status'] == 'open'
    item.active = active
    return redirect('/')


@app.route('/new-item/', methods=['GET', 'POST'])
def new_item():
    if request.method == 'GET':
        return render_template('new_item.html')
    todo_list.append(ToDoItem(request.form['task']))
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
