import logging

from genericclient import GenericClient
from genericclient.exceptions import ResourceNotFound, MultipleResourcesFound  # noqa


# silence 'Resetting dropped connection' logs

logger = logging.getLogger('requests.packages.urllib3.connectionpool')
logger.setLevel(logging.WARN)


class GamesAPIClient(GenericClient):
    """
    A pre-configured generic client for the simpl-games-api

    Usage::

        from simpl_client import GamesAPIClient
        games_client = GamesAPIClient(url=SIMPL_GAMES_URL, auth=SIMPL_GAMES_AUTH)

    Endpoints
    ---------

    Endpoints are available as properties on the main instance.

    ``.all()``
    ~~~~~~~~~~

    Retrieves all resources (essentially a simple ``GET`` on the endpoint)::

        games_client.runusers.all()  # GET /runusers/

    ``.filter(**kwargs)`` calls a ``GET`` with ``kwargs`` as querystring values::

        games_client.runusers.filter(run=12, world=1)  # GET /runusers/?run=12&world=1

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

        games_client.runusers.filter(run=12, world=1)  # GET /runusers/?run=12&world=1
        games_client.runusers.filter(id=12)  # GET /runusers/12/
        games_client.users.filter(username='alice')  # GET /users/alice/

    ``.create(payload)``
    ~~~~~~~~~~~~~~~~~~~~

    Will result in a ``POST``, with ``payload`` (a ``dict``) as the request's body,
    returning a new ``Resource``::

        runuser = games_client.runusers.create({'run': 12, 'world': 1})  # POST /runusers/

    ``.get_or_create(defaults, **kwargs)``
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Issues a GET to fetch the resource. If the resource is not found, issues a POST
    to create the resource.

        # Assuming it doesn't exist
        run = myclient.run.get_or_update(game=12, defaults={'active': True})  # GET /runs/?game=12, then POST /runs/


    ``.create_or_update(payload)``
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    If ``payload`` contains a key called ``'id'``, will issue a ``PUT``, otherwise
    it will call ``.create``::

        runuser = games_client.runusers.create_or_update({'id': 1234, 'world': 1})  # PUT /runusers/1234/


    ``.delete(pk)``
    ~~~~~~~~~~~~~~~

    Will issue a ``DELETE``, and will use ``pk`` as part of the URL::

        games_client.runusers.delete(24)  # DELETE /runusers/24/

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

        runuser = games_client.runusers.create({'run': 12, 'world': 1})  # POST /runusers/
        runuser.delete()  # DELETE /runuser/345/ -- the ID 345 was returned by the server in the previous response

    ``Resource.save()`` will result in a ``PUT``, with ``Resource.id`` as
    par of the URL::

        runuser = games_client.runusers.create({'run': 12, 'world': 1})  # POST /runusers/
        runuser.run = 13
        runuser.save()  # PUT /runuser/345/

    """

    def __init__(self, *args, **kwargs):
        kwargs['trailing_slash'] = True
        super(GamesAPIClient, self).__init__(*args, **kwargs)