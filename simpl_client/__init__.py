_version = "0.8.1"
__version__ = VERSION = tuple(map(int, _version.split('.')))

# provided for backward compatibility:
from simpl_client.asyn import GamesAPIClient  # noqa
