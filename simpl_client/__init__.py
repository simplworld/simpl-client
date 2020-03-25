_version = "0.8.0"
__version__ = VERSION = tuple(map(int, _version.split('.')))

# provided for backward compatibility:
from simpl_client.asyn import GamesAPIClient  # noqa
