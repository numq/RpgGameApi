import pytest

""" 
run with: 

python -m pytest tests

"""


@pytest.fixture
def test_app():
    from app import create_app
    from config import TestConfig
    from main import register_blueprints, db as _db

    app = create_app(TestConfig)
    register_blueprints(app)
    _db.init_app(app)
    _db.app = app
    _db.create_all()
    return app


def test_index(test_app):
    with test_app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert b"index" in response.data
