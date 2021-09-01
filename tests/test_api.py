import pytest
import run


@pytest.fixture(scope='module')
def client():
    with run.connex_app.app.test_client() as c:
        yield c

def test_visits(client):
    response = client.get('/api/visits')
    assert response.status_code == 200
