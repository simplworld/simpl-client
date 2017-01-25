from unittest import TestCase

import responses

from simpl_client import ModelServiceClient
from genericclient.exceptions import ResourceNotFound, MultipleResourcesFound

from .utils import request_callback

MODELSERVICE_URL = 'http://dummy.org'

service_client = ModelServiceClient(url=MODELSERVICE_URL)


# Create your tests here.
class SimplTestCase(TestCase):

    def test_call(self):
        with responses.RequestsMock() as rsps:
            rsps.add_callback(
                responses.POST, MODELSERVICE_URL + '/call',
                callback=request_callback,
                content_type='application/json',
            )
            result = service_client.call('edu.upenn.sims.mysim.myscope.add', 1, 2)
            self.assertEqual(result, 3)

    def test_publish(self):
        with responses.RequestsMock() as rsps:
            rsps.add_callback(
                responses.POST, MODELSERVICE_URL + '/publish',
                callback=request_callback,
                content_type='application/json',
            )
            result = service_client.publish('edu.upenn.sims.mysim.myscope.sometopic', 1, 2)
            # When we publish, we get a publishing id back
            self.assertEqual(result, {'id': 1234})

    def test_prefix(self):
        service_client.add_prefixes(root='edu.upenn.sims.mysim.myscope')
        with responses.RequestsMock() as rsps:
            rsps.add_callback(
                responses.POST, MODELSERVICE_URL + '/call',
                callback=request_callback,
                content_type='application/json',
            )
            result = service_client.call('root:add', 1, 2)
            self.assertEqual(result, 3)
