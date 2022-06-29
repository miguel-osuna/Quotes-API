"""
Tests for the authentication resource.
"""

import secrets
from flask import url_for

from quotes_api.common import HttpStatus


def test_get_user_tokens(client, admin_headers, new_admin):
    """Tests the get user tokens operation."""

    random_id = secrets.token_hex(12)

    # Test 404 error
    user_tokens_url = url_for("auth.tokens", user_id=random_id)
    res = client.get(user_tokens_url, headers=admin_headers)

    assert res.status_code == HttpStatus.NOT_FOUND_404.value
    assert res.get_json() == {"error": "User does not exist."}

    # Test get all admin tokens
    user_tokens_url = url_for("auth.tokens", user_id=new_admin.id)
    res = client.get(user_tokens_url, headers=admin_headers)
    data = res.get_json()

    assert res.status_code == HttpStatus.OK_200.value
    assert len(data["records"]) > 0


def test_revoke_access_token(client, admin_headers):
    """Tests the revoke access token operation."""

    # Revoke access token
    revoke_access_token_url = url_for("auth.revoke_access_token")
    res = client.delete(revoke_access_token_url, headers=admin_headers)

    assert res.status_code == HttpStatus.NO_CONTENT_204.value

    # Try to access a protected endpoint with the same token
    users_url = url_for("auth.users")
    res = client.get(users_url, headers=admin_headers)

    assert res.status_code == HttpStatus.UNAUTHORIZED_401.value


def test_revoke_refresh_token(client, admin_refresh_headers):
    """Tests the revoke refresh token operation."""

    revoke_refresh_token_url = url_for("auth.revoke_refresh_token")
    res = client.delete(revoke_refresh_token_url, headers=admin_refresh_headers)

    assert res.status_code == HttpStatus.NO_CONTENT_204.value

    # Try to access a protected endpoint with the same token
    refresh_url = url_for("auth.token_refresh")
    res = client.post(refresh_url, headers=admin_refresh_headers)

    assert res.status_code == HttpStatus.UNAUTHORIZED_401.value


def test_create_trial_token(client, admin_headers):
    """Tests the create trial token operation."""

    trial_token_url = url_for("auth.trial_token")
    res = client.post(trial_token_url, headers=admin_headers)

    assert res.status_code == HttpStatus.CREATED_201.value

    # Try to access a protected endpoint with the new token
    token = res.get_json()["trial_api_key"]
    users_url = url_for("auth.users")
    query_parameters = {"page": "1", "per_page": "5"}
    headers = {
        "content-type": "application/json",
        "authorization": f"Bearer {token}",
    }
    res = client.get(users_url, headers=headers, query_string=query_parameters)

    assert res.status_code == HttpStatus.OK_200.value


def test_create_permanent_token(client, admin_headers):
    """Tests the create permanent token operation."""

    permanent_token_url = url_for("auth.permanent_token")
    res = client.post(permanent_token_url, headers=admin_headers)

    assert res.status_code == HttpStatus.CREATED_201.value

    # Try to access a protected endpoint with the new token
    token = res.get_json()["permanent_api_key"]
    users_url = url_for("auth.users")
    query_parameters = {"page": "1", "per_page": "5"}
    headers = {
        "content-type": "application/json",
        "authorization": f"Bearer {token}",
    }
    res = client.get(users_url, headers=headers, query_string=query_parameters)

    assert res.status_code == HttpStatus.OK_200.value
