"""
Tests for the quote resource.
"""

import pytest
from flask import url_for
from quotes_api.common import HttpStatus


def test_get_quote(client, user_headers, new_quote):
    """Tests the get quote operation."""

    # Test 404 error
    quote_url = url_for("api.quote", quote_id="1000000")
    res = client.get(quote_url, headers=user_headers)
    assert res.status_code == HttpStatus.NOT_FOUND_404.value

    # Test get quote
    quote_url = url_for("api.quote", quote_id=new_quote.id)
    res = client.get(quote_url, headers=user_headers)
    assert res.status_code == HttpStatus.OK_200.value

    data = res.get_json()
    assert data["id"] == new_quote.id
    assert data["author_name"] == new_quote.author_name
    assert data["author_image"] == new_quote.author_image
    assert data["tags"] == new_quote.tags


def test_put_quote(client, admin_headers, new_quote):
    """Tests the put quote operation."""

    # Test 404 error
    quote_url = url_for("api.quote", quote_id="1000000")
    res = client.put(quote_url, headers=admin_headers)
    assert res.status_code == HttpStatus.NOT_FOUND_404.value

    # Test put quote
    data = {
        "quote_text": "Put quote.",
        "author_name": "Put Author",
        "author_image": "Put URL",
        "tags": ["put-test-tag"],
    }
    quote_url = url_for("api.quote", quote_id=new_quote.id)
    res = client.put(quote_url, headers=admin_headers, json=data)
    assert res.status_code == HttpStatus.NO_CONTENT_204.value


def test_patch_quote(client, admin_headers, new_quote):
    """Tests the patch quote operation."""

    # Test 404 error
    quote_url = url_for("api.quote", quote_id="1000000")
    res = client.patch(quote_url, headers=admin_headers)
    assert res.status_code == HttpStatus.NOT_FOUND_404.value

    # Test patch quote
    data = {"quote_text": "Patch quote."}
    quote_url = url_for("api.quote", quote_id=new_quote.id)
    res = client.patch(quote_url, quote_id=new_quote.id, json=data)
    assert res.status_code == HttpStatus.NO_CONTENT_204.value


def test_delete_quote(client, admin_headers, new_quote, quote):
    """Tests the delete quote operation."""

    # Test 404 error
    quote_url = url_for("api.quote", quote_id="1000000")
    res = client.delete(quote_url, headers=admin_headers)
    assert res.status_code == HttpStatus.NOT_FOUND_404.value

    # Test delete user
    quote_url = url_for("api.quote", quote_id=new_quote.id)
    res = client.delete(quote_url, headers=admin_headers)
    assert res.status_code == HttpStatus.NO_CONTENT_204.value

    # Test quote is deleted from the database
    Quote = quote  # pylint: disable=invalid-name
    with pytest.raises(Exception):
        quote = Quote.objects.get(id=new_quote.id)


def test_get_all_quote(client, user_headers, new_quote):
    """Tests the get all quotes operation."""

    # Test get all quotes
    quotes_url = url_for("api.quotes")
    query_parameters = {"page": "1", "per_page": "5"}

    res = client.get(quotes_url, headers=user_headers, query_string=query_parameters)
    assert res.status_code == HttpStatus.OK_200.value

    data = res.get_json()
    quotes = data["records"]
    meta = data["meta"]

    assert meta["page_number"] == "1"
    assert meta["page_size"] == "5"
    assert meta["total_pages"] == "1"
    assert meta["total_records"] == "1"

    for quote in quotes:
        assert any(quote["id"] == new_quote.id)


def test_create_quote(client, admin_headers, quote):
    """Tests the create quote operation."""

    # Test 400 (Bad request)
    quotes_url = url_for("api.quotes")
    data = {"quote_text": "Post quote."}
    res = client.post(quotes_url, headers=admin_headers, json=data)
    assert res.status_code == HttpStatus.BAD_REQUEST_400.value

    # Tetst create quote
    data["author_name"] = "Post Author"
    data["author_image"] = "Post URL"
    data["tags"] = ["post-test-tag"]

    res = client.post(quotes_url, deaders=admin_headers, json=data)
    assert res.status_code == HttpStatus.CREATED_201.value

    # Test quote is on the database
    data = res.get_json()
    Quote = quote  # pylint: disable=invalid-name
    quote = Quote.objects.get(id=data["id"])

    assert quote.id == data["id"]
    assert quote.quote_text == data["quote_text"]
    assert quote.author_image == data["author_image"]
    assert quote.tags == data["tags"]
