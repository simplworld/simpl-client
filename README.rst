GamesAPIClient
==============

.. image:: https://travis-ci.com/simplworld/simpl-client.svg?token=cyqpBgqLC1o8qUptfcpE&branch=master
    :target: https://travis-ci.com/simplworld/simpl-client


Python clients for accessing simpl-games-api either asynchronously or synchronously

Usage
-----


To asynchronously access simpl-games-api use::

    from simpl_client.asyn import GamesAPIClient
    asyn_games_client = GamesAPIClient(url=SIMPL_GAMES_URL, auth=SIMPL_GAMES_AUTH)

for backwards compatibility, the default is asynchronous access::

    from simpl_client import GamesAPIClient
    asyn_games_client = GamesAPIClient(url=SIMPL_GAMES_URL, auth=SIMPL_GAMES_AUTH)

See simpl_client/async/games_client.py for asynchronous endpoints

To synchronously access simpl-games-api use::

    from simpl_client.syn import GamesAPIClient
    syn_games_client = GamesAPIClient(url=SIMPL_GAMES_URL, auth=SIMPL_GAMES_AUTH)

See simpl_client/syn/games_client.py for synchronous endpoints

Installation
------------
::

    pip install simpl-client




Setup development environment
-----------------------------
::

    git clone git@github.com:simplworld/simpl-client.git
    cd simpl-client
    mkvirtualenv simpl-client
    pip install -e .

Testing
-------
::

    python setup.py test

Running the tests requires having ``libmagic`` installed.

On OS X, simply run ``brew install libmagic``.

License
-------

Copyright © 2018 The Wharton School,  The University of Pennsylvania 

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
