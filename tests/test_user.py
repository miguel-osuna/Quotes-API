""" Test user. """
import pytest
from flask import url_for

from quotes_api.common import HttpStatus


# def test_user_signup(client):
#     pass


# def test_user_login(client):
#     pass


# def test_user_logout(client):
#     pass


def test_get_user(client, admin_headers, new_user):

    # Test 404 error
    user_url = url_for("auth.user_by_id", user_id="1000000")
    res = client.get(user_url, headers=admin_headers)
    assert res.status_code == HttpStatus.not_found_404.value

    # Test get user
    user_url = url_for("auth.user_by_id", user_id=new_user.id)
    res = client.get(user_url, headers=admin_headers)
    assert res.status_code == HttpStatus.ok_200.value

    data = res.get_json()
    assert data["id"] == new_user.id
    assert data["username"] == new_user.username
    assert data["email"] == new_user.email
    assert data["active"] == new_user.active
    assert data["roles"] == new_user.roles


def test_put_user(client, admin_headers, new_user):
    # Test 404 error
    user_url = url_for("auth.user_by_id", user_id="1000000")
    res = client.put(user_url, headers=admin_headers)
    assert res.status_code == HttpStatus.not_found_404.value

    # Test put user
    data = {"username": "test", "email": "test@email.com", "password": "test"}
    user_url = url_for("auth.user_by_id", user_id=new_user.id)
    res = client.put(user_url, headers=admin_headers, json=data)
    assert res.status_code == HttpStatus.no_content_204.value


def test_patch_user(client, admin_headers, new_user):
    # Test 404 error
    user_url = url_for("auth.user_by_id", user_id="1000000")
    res = client.patch(user_url, headers=admin_headers)
    assert res.status_code == HttpStatus.not_found_404.value

    # Tets patch user
    data = {"username": "test"}
    user_url = url_for("auth.user_by_id", user_id=new_user.id)
    res = client.patch(user_url, headers=admin_headers, json=data)
    assert res.status_code == HttpStatus.no_content_204.value


def test_delete_user(client, admin_headers, new_user, user):
    # Test 404 error
    user_url = url_for("auth.user_by_id", user_id="1000000")
    res = client.delete(user_url, headers=admin_headers)
    assert res.status_code == HttpStatus.not_found_404.value

    # Test delete user
    user_url = url_for("auth.user_by_id", user_id=new_user.id)
    res = client.delete(user_url, headers=admin_headers)
    assert res.status_code == HttpStatus.no_content_204.value

    # Test user is deleted from the database
    User = user
    with pytest.raises(Exception) as e_info:
        user = User.objects.get(id=new_user.id)


def test_get_all_user(client, admin_headers, new_user):
    # Test get all users
    users_url = url_for("auth.users")
    query_parameters = {"page": "1", "per_page": "5"}

    res = client.get(users_url, headers=admin_headers, query_string=query_parameters)
    assert res.status_code == HttpStatus.ok_200.value

    data = res.get_json()
    users = data["records"]
    meta = data["meta"]

    assert meta["page_number"] == "1"
    assert meta["page_size"] == "5"
    assert meta["total_pages"] == "1"
    assert meta["total_records"] == "1"

    for u in users:
        assert any(u["id"] == new_user.id)
