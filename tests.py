from pytest import fixture

from app import app, ToDoItem, todo_list


@fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()


@fixture
def existing_item():
    import app
    return app.todo_list[0]


@fixture
def new_item():
    return ToDoItem('something new')


def test_todo_list_doesnt_return_an_error(client):
    response = client.get('/')
    assert response.status_code < 400


def test_todo_list_doesnt_show_completed_tasks(client):
    response = client.get('/')
    assert 'clean the house' not in response.get_data(as_text=True)


def test_completed_items_doesnt_return_an_error(client):
    response = client.get('/completed-items/')
    assert response.status_code < 400


def test_completed_items_doesnt_show_active_items(client):
    response = client.get('/completed-items/')
    assert 'feed the fish' not in response.get_data(as_text=True)


def test_get_edit_item_doesnt_return_an_error(client, existing_item):
    response = client.get('/edit-item/%s' % existing_item.id)
    assert response.status_code < 400


def test_get_edit_item_has_correct_item(client, existing_item):
    response = client.get('/edit-item/%s' % existing_item.id)
    assert str(existing_item.id) in response.get_data(as_text=True)


def test_post_change_to_item_doesnt_return_error(client, existing_item):
    form = {'task': existing_item.text, 'status': 'open'}
    response = client.post('/edit-item/%s' % existing_item.id, data=form)
    assert response.status_code < 400


def test_can_post_change_to_item(client, existing_item):
    new_status = not existing_item.active
    status_to_text = {True: 'open', False: 'closed'}
    form = {'task': existing_item.text, 'status': status_to_text[new_status]}
    client.post('/edit-item/%s' % existing_item.id, data=form)
    assert existing_item.active == new_status


def test_can_view_new_item_page(client):
    response = client.get('/new-item/')
    assert response.status_code < 400


def test_can_add_new_item(client):
    form = {'task': 'something new'}
    client.post('/new-item/', data=form)
    assert form['task'] in [task.text for task in todo_list]
