import hmac

from simpl_client.auth import generate_external_auth_hmac


def test_generate_external_auth_hmac():
    # Test our hash generation process is valid
    shared_secret = "testing-12345"
    email = "bob@example.com"

    h = hmac.new(
        key=shared_secret.encode("utf-8"),
        msg=email.encode("utf-8"),
        digestmod="sha256",
    )

    expected_value = f"::simpl-external-auth::{h.hexdigest()}"

    assert expected_value == generate_external_auth_hmac(email=email, shared_secret=shared_secret)

