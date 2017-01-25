import json
from urllib.parse import urljoin

import requests


class ModelServiceClient(object):
    """
    An http client that can be used to talk to the modelservice.

    Note that the modelservice will accept the client's requests only in DEBUG
    mode.

    Usage::

        from simpl_client import ModelServiceClient
        client = ModelServiceClient('http://modelservice:8080')

        result = client.call('procedure', 1, 2, 3, arg1='a', arg2='b')

        # or

        client.publish('topic', 1, 2, 3, arg1='a', arg2='b')

    The client support prefix, either on instantiation::

        client = ModelServiceClient('http://modelservice:8080', prefixes={'model': 'edu.upenn.sims.mysim'})

    or via the `add_prefixes()` method::

        client.add_prefixes(model='edu.upenn.sims.mysim')

    Then you can call::

        client.publish('prefix:mytopic')

    """

    def __init__(self, url, call_path='/call', publish_path='/publish', prefixes=None):
        self.url = url
        if prefixes is None:
            prefixes = {}
        self.prefixes = prefixes
        self.call_path = call_path
        self.publish_path = publish_path
        self.session = requests.session()
        self.session.headers.update({'Content-Type': 'application/json'})
        super(ModelServiceClient, self).__init__()

    def add_prefixes(self, **kwargs):
        self.prefixes.update(kwargs)

    def _resolve_prefix(self, prefix):
        try:
            return self.prefixes[prefix]
        except KeyError:
            raise ValueError("Prefix `{}` not found.".format(prefix))

    def _resolve_uri(self, uri):
        if ':' in uri:
            prefix, remainder = uri.split(':', 1)
            uri = "{}.{}".format(
                self._resolve_prefix(prefix),
                remainder,
            )
        return uri

    def _post_json(self, url, payload):
        response = self.session.post(url, json.dumps(payload))
        return json.loads(response.text)

    def call(self, procedure, *args, **kwargs):
        url = urljoin(self.url, self.call_path)
        payload = {
            "procedure": self._resolve_uri(procedure),
            "args": args,
            "kwargs": kwargs,
        }
        return self._post_json(url, payload)

    def publish(self, topic, *args, **kwargs):
        url = urljoin(self.url, self.publish_path)
        payload = {
            "topic": self._resolve_uri(topic),
            "args": args,
            "kwargs": kwargs,
        }
        return self._post_json(url, payload)
