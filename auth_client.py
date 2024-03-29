import config
from intuitlib.client import AuthClient

# Instantiate client
auth_client = AuthClient(
    client_id=config.client_id,
    client_secret=config.client_secret,
    redirect_uri=config.redirect_uri,
    environment=config.environment, # “sandbox” or “production”
)