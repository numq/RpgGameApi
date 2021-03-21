import json

from tests.unit import test_user_id, test_value, random_string


class TestUser:

    def test_create_user(self, test_app):
        with test_app.test_client() as client:
            response = client.post('/users/create', json=json.loads(json.dumps({u'name': random_string,
                                                                                u'email': random_string,
                                                                                u'password': random_string})))
            assert response.status_code == 200

    def test_get_user(self, test_app):
        with test_app.test_client() as client:
            response = client.get('/users/%s' % test_user_id)
            assert response.status_code == 200

    def test_get_users(self, test_app):
        with test_app.test_client() as client:
            response = client.get('/users')
            assert response.status_code == 200

    def test_update_user(self, test_app):
        with test_app.test_client() as client:
            user_id = client.get('/users').json[-1]['id']
            response = client.put('/users/%s' % user_id, json=json.loads(json.dumps({u'id': test_value,
                                                                                     u'name': random_string,
                                                                                     u'email': random_string,
                                                                                     u'password': random_string})))
            assert response.status_code == 200

    def test_delete_user(self, test_app):
        with test_app.test_client() as client:
            response = client.delete('/users/%s' % test_value)
            assert response.status_code == 200
