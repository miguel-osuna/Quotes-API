""" Test authentication. """
from flask import url_for

from quotes_api.common import HttpStatus


def test_get_all_user_tokens(client, user_headers, new_access_token):
    user_tokens_url = url_for("auth.tokens")
    query_parameters = {"page": "1", "per_page": "5"}

    res = client.get(
        user_tokens_url, headers=user_headers, query_string=query_parameters
    )
    assert res.status_code == HttpStatus.OK_200.value

    data = res.get_json()
    tokens = data["records"]
    meta = data["meta"]

    assert meta["page_number"] == "1"
    assert meta["page_size"] == "5"

    for t in tokens:
        assert any(t["id"] == new_access_token.id)


def test_revoke_access_token(client, admin_headers):
    # Revoke access token
    revoke_access_token_url = url_for("auth.revoke_access_token")
    res = client.delete(revoke_access_token_url, headers=admin_headers)
    assert res.status_code == HttpStatus.NO_CONTENT_204.value

    # Try to access a protected endpoint with the same token
    users_url = url_for("auth.users")
    res = client.get(users_url, headers=admin_headers)
    assert res.status_code == HttpStatus.UNAUTHORIZED_401.value


def test_revoke_refresh_token(client, admin_refresh_headers):
    revoke_refresh_token_url = url_for("auth.revoke_refresh_token")
    res = client.delete(revoke_refresh_token_url, headers=admin_refresh_headers)
    assert res.status_code == HttpStatus.NO_CONTENT_204.value

    # Try to access a protected endpoint with the same token
    refresh_url = url_for("auth.token_refresh")
    res = client.post(refresh_url, headers=admin_refresh_headers)
    assert res.status_code == HttpStatus.UNAUTHORIZED_401.value


def test_create_trial_token(client, admin_headers):
    trial_token_url = url_for("auth.trial_token")
    res = client.post(trial_token_url, headers=admin_headers)
    assert res.status_code == HttpStatus.CREATED_201.value

    # Try to access a protected endpoint with the new token
    token = res.get_json()["permanent_api_key"]

    users_url = url_for("auth.users")
    query_parameters = {"page": "1", "per_page": "5"}
    headers = {
        "content-type": "application/json",
        "authorization": "Bearer {}".format(token),
    }
    res = client.get(users_url, headers=headers, query_string=query_parameters)
    assert res.status_code == HttpStatus.OK_200.value


def test_create_permanent_token(client, admin_headers):
    permanent_token_url = url_for("auth.permanent_token")
    res = client.post(permanent_token_url, headers=admin_headers)
    assert res.status_code == HttpStatus.CREATED_201.value

    # Try to access a protected endpoint with the new token
    token = res.get_json()["trial_api_key"]

    users_url = url_for("auth.users")
    query_parameters = {"page": "1", "per_page": "5"}
    headers = {
        "content-type": "application/json",
        "authorization": "Bearer {}".format(token),
    }
    res = client.get(users_url, headers=headers, query_string=query_parameters)
    assert res.status_code == HttpStatus.OK_200.value
