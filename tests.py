from pytest import fixture

from app import app


@fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()


def test_todo_list_doesnt_show_completed_tasks(client):
    response = client.get('/')
    assert 'clean the house' not in response.get_data(as_text=True)
