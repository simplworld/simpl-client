_version = "0.7.4"
__version__ = VERSION = tuple(map(int, _version.split('.')))

# provided for backward compatibility:
from simpl_client.async import GamesAPIClient  # noqa
