from asynctest import TestCase

from test_aiohttp import RouteManager

from simpl_client import GamesAPIClient


SIMPL_GAMES_URL = 'http://dummy.org'
SIMPL_GAMES_AUTH = ('user', 'user')

games_client = GamesAPIClient(url=SIMPL_GAMES_URL, auth=SIMPL_GAMES_AUTH)


# Create your tests here.
class SimplTestCase(TestCase):

    async def test_simpl_all(self):
        with RouteManager() as rsps:
            rsps.add('GET', SIMPL_GAMES_URL + '/users/', json=[
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

            users = await games_client.users.all()
            self.assertEqual(len(users), 3)

    async def test_simpl_filter(self):
        with RouteManager() as rsps:
            rsps.add('GET', SIMPL_GAMES_URL + '/users/', json=[
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

            users = await games_client.users.filter(role="player")
            self.assertEqual(len(users), 2)

    async def test_simpl_get_id(self):
        with RouteManager() as rsps:
            rsps.add('GET', SIMPL_GAMES_URL + '/users/2/', json={
                'id': 2,
                'username': 'user2',
                'role': 'player',
            })

            user2 = await games_client.users.get(id=2)
            self.assertEqual(user2.username, 'user2')

        with RouteManager() as rsps:
            rsps.add('GET', SIMPL_GAMES_URL + '/users/9999/', status=404)

            with self.assertRaises(games_client.ResourceNotFound):
                await games_client.users.get(id=9999)

    async def test_simpl_get_params(self):
        with RouteManager() as rsps:
            rsps.add('GET', SIMPL_GAMES_URL + '/users/', json=[
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

            with self.assertRaises(games_client.MultipleResourcesFound):
                await games_client.users.get(role='player')

        with RouteManager() as rsps:
            rsps.add('GET', SIMPL_GAMES_URL + '/users/', json=[])

            with self.assertRaises(games_client.ResourceNotFound):
                await games_client.users.get(role='cookie_monster')

        with RouteManager() as rsps:
            rsps.add('GET', SIMPL_GAMES_URL + '/users/', json=[
                {
                    'id': 3,
                    'username': 'user3',
                    'role': 'facilitator',
                },
            ])

            facilitator = await games_client.users.get(role='facilitator')
            self.assertEqual(facilitator.username, 'user3')

    async def test_simpl_bulk_unauthd(self):
        with RouteManager() as rsps:
            rsps.add('GET', SIMPL_GAMES_URL + '/bulk/users/', status=403)


            with self.assertRaises(GamesAPIClient.NotAuthenticatedError):
                resources = await games_client.bulk.users.all()
                self.assertEqual(resources, None)

    async def test_simpl_bulk_create(self):
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
        with RouteManager() as rsps:
            rsps.add('POST', SIMPL_GAMES_URL + '/bulk/users/', json=payload, status=201)

            resources = await games_client.bulk.users.create(payload)
            self.assertEqual(resources, None)

        with RouteManager() as rsps:
            rsps.add('POST', SIMPL_GAMES_URL + '/bulk/users/', json=payload, status=201)

            resources = await games_client.bulk.users.create(payload, return_ids=True)
            self.assertEqual(len(resources), 2)
            self.assertEqual(resources[0], 1)

    async def test_simpl_bulk_delete(self):
        with RouteManager() as rsps:
            rsps.add('DELETE', SIMPL_GAMES_URL + '/bulk/users/', status=204)

            resources = await games_client.bulk.users.delete(id__in=[1, 2])
            self.assertEqual(resources, None)
