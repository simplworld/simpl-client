_version = "0.1.3"
__version__ = VERSION = tuple(map(int, _version.split('.')))


from .games_client import GamesAPIClient  # noqa
from .modelservice_client import ModelServiceClient  # noqa
