from pytest import fixture

from app import app, ToDoItem


def setup_function():
    """this is run before every test function in the file"""
    # make sure that we don't accumulate items in the todo list
    # as each test is run
    import app  # prevent aliasing name
    app.todo_list = []


@fixture
def client():
    """crate a new test client"""
    app.config['TESTING'] = True
    return app.test_client()


@fixture
def item():
    """create a new item"""
    import app  # prevent aliasing name
    item = ToDoItem('fake')
    app.todo_list.append(item)
    return item


def test_get_by_id_finds_correct_item(item):
    assert item is ToDoItem.get_by_id(item.id)


def test_can_access_edit_item(client, item):
    response = client.get('/edit-item/%s' % item.id)
    assert response.status_code < 400


def test_completed_items_do_not_appear_in_todo(client, item):
    item.active = False
    response = client.get('/todo')
    assert item.text not in response.get_data(as_text=True)
