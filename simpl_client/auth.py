import hmac


def generate_external_auth_hmac(email, shared_secret):
    """
    This is used by Simpl UI apps that need to use some sort of external
    authentication system like LTI, OAuth2, etc.

    Instead of sending the actual simpl-games-api User's password down the
    websocket, we used a specially formatted HMAC messages authenticated by
    a shared secret between the modelservice and the UI.
    """
    # Build the hash
    h = hmac.new(
        key=shared_secret.encode("utf-8"),
        msg=email.encode("utf-8"),
        digestmod="sha256",
    )

    return f"::simpl-external-auth::{h.hexdigest()}"