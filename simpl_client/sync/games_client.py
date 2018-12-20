from genericclient import GenericClient, Endpoint, Resource
from genericclient.exceptions import HTTPError
from genericclient.pagination import link_header

"""
A pre-configured synchronous generic client for the simpl-games-api

Usage::

    from simpl_client.sync import GamesAPIClient
    sync_games_client = GamesAPIClient(url=simpl_url, auth=simpl_auth)

Endpoints
---------

Endpoints are available as properties on the main instance.

``.all()``
~~~~~~~~~~

Retrieves all resources (essentially a simple ``GET`` on the endpoint)::

    sync_games_client.runusers.all()  # GET /runusers/

``.filter(**kwargs)`` calls a ``GET`` with ``kwargs`` as querystring values::

    sync_games_client.runusers.filter(run=12, world=1)  # GET /runusers/?run=12&world=1

``.get(**kwargs)``
~~~~~~~~~~~~~~~~~~

A special case of ``.filter()``.

If ``kwargs`` contains ``id``, ``pk``, ``slug`` or ``username``, that value will
be used in the URL path, in that order.

Otherwise, it calls a ``GET`` with ``kwargs`` as querystring values.

If the returned list is empty, will raise ``ResourceNotFound``.

If the returned list contains more than 1 resource, will raise ``MultipleResourcesFound``

Note that ``.get()`` will return a ``Resource``, not a list of ``Resource``s

::

    sync_games_client.runusers.filter(run=12, world=1)  # GET /runusers/?run=12&world=1
    sync_games_client.runusers.filter(id=12)  # GET /runusers/12/
    sync_games_client.users.filter(username='alice')  # GET /users/alice/

``.create(payload)``
~~~~~~~~~~~~~~~~~~~~

Will result in a ``POST``, with ``payload`` (a ``dict``) as the request's body,
returning a new ``Resource``::

    runuser = sync_games_client.runusers.create({'run': 12, 'world': 1})  # POST /runusers/

``.get_or_create(defaults, **kwargs)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Issues a GET to fetch the resource. If the resource is not found, issues a POST
to create the resource.

    # Assuming it doesn't exist
    run = sync_games_client.runs.get_or_create(game=12, defaults={'active': True})  # GET /runs/?game=12, then POST /runs/


``.create_or_update(payload)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If ``payload`` contains a key called ``'id'``, will issue a ``PUT``, otherwise
it will call ``.create``::

    runuser = sync_games_client.runusers.create_or_update({'id': 1234, 'world': 1})  # PUT /runusers/1234/


``.delete(pk)``
~~~~~~~~~~~~~~~

Will issue a ``DELETE``, and will use ``pk`` as part of the URL::

    sync_games_client.runusers.delete(24)  # DELETE /runusers/24/

Resources
---------

All endpoints methods (with the exception of ``.delete()``) return either a
``Resource`` or a list of ``Resource``s.

A ``Resource`` is just a wrapping class for a ``dict``, where keys can be accessed
as properties.

Additionally, ``Resource``s have a special property called ``.payload``, which
contains the original payload received from the server.

``Resource``s have the following methods:

``Resource.delete()`` will result in a ``DELETE``, with ``Resource.id`` as
par of the URL::

    runuser = sync_games_client.runusers.create({'run': 12, 'world': 1})  # POST /runusers/
    runuser.delete()  # DELETE /runuser/345/ -- the ID 345 was returned by the server in the previous response

``Resource.save()`` will result in a ``PUT``, with ``Resource.id`` as
par of the URL::

    runuser = sync_games_client.runusers.create({'run': 12, 'world': 1})  # POST /runusers/
    runuser.run = 13
    runuser.save()  # PUT /runuser/345/

Bulk requests
-------------

::

    sync_games_client.bulk.results.create([...], return_ids=False)
    sync_games_client.bulk.results.delete(**lookup)


Detail Routes
-------------

::

    sync_games_client.scenario(id=123).rewind() 

"""


class GameResource(Resource):
    pk_name = 'slug'


class GameEndpoint(Endpoint):
    resource_class = GameResource


class BulkEndpoint(Endpoint):
    def create(self, payload, return_ids=False):
        response = self.request('post', self.url, json=payload)
        if response.status_code != 201:
            raise HTTPError(response)

        if return_ids is True:
            return [res['id'] for res in response.data]

    def delete(self, **kwargs):
        """
        :param params: filter lookup for objects to be deleted
        :return: None
        """
        response = self.request('delete', self.url, params=kwargs)

        if response.status_code != 204:
            raise HTTPError(response)

        return None


class BulkClient(GenericClient):
    endpoint_class = BulkEndpoint


class GamesAPIClient(GenericClient):
    endpoint_classes = {
        'games': GameEndpoint,
    }

    def __init__(self, *args, **kwargs):
        kwargs['trailing_slash'] = True
        kwargs['autopaginate'] = link_header
        super(GamesAPIClient, self).__init__(*args, **kwargs)

        self.bulk = BulkClient(
            url=self.url + 'bulk/',
            session=self._session,
            auth=kwargs['auth'],
            trailing_slash=self.trailing_slash,
            autopaginate=link_header,
        )
