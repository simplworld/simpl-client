_version = "0.7.4"
__version__ = VERSION = tuple(map(int, _version.split('.')))


from simpl_client.async.games_client import GamesAPIClient  # noqa
