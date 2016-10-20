from flask import Flask, render_template

app = Flask(__name__)


class ToDoItem(object):
    def __init__(self, text, active=True):
        self.text = text
        self.active = active


todo_list = [
    ToDoItem('feed the fish'),
    ToDoItem('clean the house', active=False),
    ToDoItem('win the lottery'),
]


@app.route('/')
def index():
    return render_template('list.html', title='To Do List', rows=todo_list)


if __name__ == '__main__':
    app.run(debug=True)
