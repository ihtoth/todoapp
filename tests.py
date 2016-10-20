from pytest import fixture

from app import app


@fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()


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
