from unittest import TestCase

import responses

from simpl_client import GamesAPIClient


SIMPL_GAMES_URL = 'http://dummy.org'
SIMPL_GAMES_AUTH = ('user', 'user')

games_client = GamesAPIClient(url=SIMPL_GAMES_URL, auth=SIMPL_GAMES_AUTH)


# Create your tests here.
class SimplTestCase(TestCase):

    def test_simpl_all(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, SIMPL_GAMES_URL + '/users/', json=[
                {
                    'id': 1,
                    'username': 'user1',
                    'role': 'player',
                },
                {
                    'id': 2,
                    'username': 'user2',
                    'role': 'player',
                },
                {
                    'id': 3,
                    'username': 'user3',
                    'role': 'facilitator',
                },
            ])

            users = games_client.users.all()
            self.assertEqual(len(users), 3)

    def test_simpl_filter(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, SIMPL_GAMES_URL + '/users/', json=[
                {
                    'id': 1,
                    'username': 'user1',
                    'role': 'player',
                },
                {
                    'id': 2,
                    'username': 'user2',
                    'role': 'player',
                },
            ])

            users = games_client.users.filter(role="player")
            self.assertEqual(len(users), 2)

    def test_simpl_get_id(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, SIMPL_GAMES_URL + '/users/2/', json={
                'id': 2,
                'username': 'user2',
                'role': 'player',
            })

            user2 = games_client.users.get(id=2)
            self.assertEqual(user2.username, 'user2')

        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, SIMPL_GAMES_URL + '/users/9999/', status=404)

            self.assertRaises(games_client.ResourceNotFound, games_client.users.get, id=9999)

    def test_simpl_get_params(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, SIMPL_GAMES_URL + '/users/', json=[
                {
                    'id': 1,
                    'username': 'user1',
                    'role': 'player',
                },
                {
                    'id': 2,
                    'username': 'user2',
                    'role': 'player',
                },
            ])

            self.assertRaises(games_client.MultipleResourcesFound, games_client.users.get, role='player')

        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, SIMPL_GAMES_URL + '/users/', body='[]')

            self.assertRaises(games_client.ResourceNotFound, games_client.users.get, role='cookie_monster')

        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, SIMPL_GAMES_URL + '/users/', json=[
                {
                    'id': 3,
                    'username': 'user3',
                    'role': 'facilitator',
                },
            ])

            facilitator = games_client.users.get(role='facilitator')
            self.assertEqual(facilitator.username, 'user3')

    def test_simpl_bulk_create(self):
        payload = [
            {
                'id': 1,
                'username': 'user1',
                'role': 'player',
            },
            {
                'id': 2,
                'username': 'user2',
                'role': 'player',
            },
        ]
        with responses.RequestsMock() as rsps:
            rsps.add(responses.POST, SIMPL_GAMES_URL + '/bulk/users/', json=payload, status=201)

            resources = games_client.bulk.users.create(payload)
            self.assertEqual(resources, None)

        with responses.RequestsMock() as rsps:
            rsps.add(responses.POST, SIMPL_GAMES_URL + '/bulk/users/', json=payload, status=201)

            resources = games_client.bulk.users.create(payload, return_ids=True)
            self.assertEqual(len(resources), 2)
            self.assertEqual(resources[0], 1)

    def test_simpl_bulk_delete(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.DELETE, SIMPL_GAMES_URL + '/bulk/users/', status=204)

            resources = games_client.bulk.users.delete(id__in=[1, 2])
            self.assertEqual(resources, None)
