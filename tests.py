from pytest import fixture

from app import app


@fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()


@fixture
def item():
    import app
    return app.todo_list[0]


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


def test_get_edit_item_doesnt_return_an_error(client, item):
    response = client.get('/edit-item/%s' % item.id)
    assert response.status_code < 400


def test_get_edit_item_has_correct_item(client, item):
    response = client.get('/edit-item/%s' % item.id)
    assert str(item.id) in response.get_data(as_text=True)


def test_post_change_to_item_doesnt_return_error(client, item):
    form = {'task': item.text, 'status': 'open'}
    response = client.post('/edit-item/%s' % item.id, data=form)
    assert response.status_code < 400


def test_can_post_change_to_item(client, item):
    new_status = not item.active
    status_to_text = {True: 'open', False: 'closed'}
    form = {'task': item.text, 'status': status_to_text[new_status]}
    client.post('/edit-item/%s' % item.id, data=form)
    assert item.active == new_status
