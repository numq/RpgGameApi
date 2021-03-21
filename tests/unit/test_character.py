import json

from tests.unit import test_value, random_string


class TestCharacter:

    def test_create_character(self, test_app):
        with test_app.test_client() as client:
            new_user = client.post('/users/create', json=json.loads(json.dumps({u'name': random_string,
                                                                                u'email': random_string,
                                                                                u'password': random_string})))
            user_id = new_user.json['id']
            response = client.post('/characters/create', json=json.loads(json.dumps({u'user_id': user_id})))
            assert response.status_code == 200

    def test_get_character(self, test_app):
        with test_app.test_client() as client:
            test_id = client.get('/characters').json[-1]['id']
            response = client.get('/characters/%s' % test_id)
            assert response.status_code == 200

    def test_get_characters(self, test_app):
        with test_app.test_client() as client:
            response = client.get('/characters')
            assert response.status_code == 200

    def test_update_character_level(self, test_app):
        with test_app.test_client() as client:
            test_id = client.get('/characters').json[-1]['id']
            response = client.put('/characters/%s/level' % test_id,
                                  json=json.loads(json.dumps({u'level': test_value})))
            assert response.status_code == 200

    def test_delete_character(self, test_app):
        with test_app.test_client() as client:
            character = client.get('/characters').json[-1]
            char_id = character['id']
            user_id = character['user_id']
            response = client.delete('/characters/%s' % char_id)
            client.delete('/users/%s' % user_id)
            assert response.status_code == 200
