import json

from tests.unit import random_string


class TestItem:

    def test_generate_drop(self, test_app):
        with test_app.test_client() as client:
            new_user = client.post('/users/create', json=json.loads(json.dumps({u'name': random_string,
                                                                                u'email': random_string,
                                                                                u'password': random_string})))
            user_id = new_user.json['id']
            new_character = client.post('/characters/create',
                                        json=json.loads(json.dumps({u'user_id': user_id})))
            character_id = new_character.json['id']
            new_dungeon = client.post('/dungeons/generate')
            dungeon_id = new_dungeon.json['id']

            response = client.post('/inventory/%s/drop' % character_id,
                                   json=json.loads(json.dumps({u'dungeon_id': dungeon_id})))
            client.delete('/dungeons/%s' % dungeon_id)
            client.delete('/characters/%s' % character_id)
            client.delete('/users/%s' % user_id)
            assert response.status_code == 200
            empty = client.get('/inventory/%s' % character_id)
            assert empty.json == []
