import json

from tests.unit import test_value, test_name


class TestDungeon:

    def test_create_dungeon(self, test_app):
        with test_app.test_client() as client:
            response = client.post('/dungeons/create', json=json.loads(
                json.dumps({u'name': test_name, u'level': test_value, u'experience': test_value})))
            assert response.status_code == 200

    def test_get_dungeon(self, test_app):
        with test_app.test_client() as client:
            response = client.get('/dungeons/%s' % test_value)
            assert response.status_code == 200

    def test_get_dungeons(self, test_app):
        with test_app.test_client() as client:
            response = client.get('/dungeons')
            assert response.status_code == 200

    def test_update_dungeon(self, test_app):
        with test_app.test_client() as client:
            test_id = client.get('/dungeons').json[-1]['id']
            response = client.put('/dungeons/%s' % test_id,
                                  json=json.loads(json.dumps(
                                      {u'id': test_value, u'name': test_name, u'level': test_value,
                                       u'experience': test_value})))
            assert response.status_code == 200

    def test_delete_dungeon(self, test_app):
        with test_app.test_client() as client:
            response = client.delete('/dungeons/%s' % test_value)
            assert response.status_code == 200

    def test_generate_dungeon(self, test_app):
        with test_app.test_client() as client:
            response = client.post('/dungeons/generate')
            assert response.status_code == 200
