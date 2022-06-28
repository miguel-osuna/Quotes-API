"""
Tests for the quote resource.
"""

import secrets

import pytest

from flask import url_for
from quotes_api.common import HttpStatus


def test_get_quote(client, user_headers, new_quote):
    """Tests the get quote operation."""
    random_id = secrets.token_hex(12)

    # Test 404 error
    quote_url = url_for("api.quote", quote_id=random_id)
    res = client.get(quote_url, headers=user_headers)
    assert res.status_code == HttpStatus.NOT_FOUND_404.value

    # Test get quote
    quote_url = url_for("api.quote", quote_id=new_quote.id)
    res = client.get(quote_url, headers=user_headers)
    assert res.status_code == HttpStatus.OK_200.value

    data = res.get_json()
    assert data["id"] == str(new_quote.id)
    assert data["author_name"] == new_quote.author_name
    assert data["author_image"] == new_quote.author_image
    assert data["tags"] == new_quote.tags


def test_put_quote(client, admin_headers, new_quote):
    """Tests the put quote operation."""
    random_id = secrets.token_hex(12)

    # Test 404 error
    quote_url = url_for("api.quote", quote_id=random_id)
    res = client.put(quote_url, headers=admin_headers)
    assert res.status_code == HttpStatus.NOT_FOUND_404.value

    # Test put quote
    data = {
        "quote_text": "New quote text.",
        "author_name": "New quote author",
        "author_image": "https://www.goodreads.com/quotes/tag/books",
        "tags": ["put-test-tag"],
    }
    quote_url = url_for("api.quote", quote_id=new_quote.id)
    res = client.put(quote_url, headers=admin_headers, json=data)
    assert res.status_code == HttpStatus.NO_CONTENT_204.value


def test_patch_quote(client, admin_headers, new_quote):
    """Tests the patch quote operation."""
    random_id = secrets.token_hex(12)

    # Test 404 error
    quote_url = url_for("api.quote", quote_id=random_id)
    res = client.patch(quote_url, headers=admin_headers)
    assert res.status_code == HttpStatus.NOT_FOUND_404.value

    # Test patch quote
    data = {"quote_text": "Patch quote."}
    quote_url = url_for("api.quote", quote_id=new_quote.id)
    res = client.patch(quote_url, headers=admin_headers, json=data)
    assert res.status_code == HttpStatus.NO_CONTENT_204.value


def test_delete_quote(client, admin_headers, new_quote, quote):
    """Tests the delete quote operation."""
    random_id = secrets.token_hex(12)

    # Test 404 error
    quote_url = url_for("api.quote", quote_id=random_id)
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


def test_get_all_quotes(client, user_headers, new_quote):
    """Tests the get all quotes operation."""
    # Test get all quotes
    quotes_url = url_for("api.quotes")
    query_parameters = {"page": "1", "per_page": "5"}

    res = client.get(quotes_url, headers=user_headers, query_string=query_parameters)
    assert res.status_code == HttpStatus.OK_200.value

    data = res.get_json()
    quotes = data["records"]
    meta = data["meta"]

    assert meta["page_number"] == 1
    assert meta["page_size"] == 5
    assert meta["total_pages"] == 1
    assert meta["total_records"] == 1

    for quote in quotes:
        assert quote["id"] == str(new_quote.id)


def test_create_quote(client, admin_headers, quote):
    """Tests the create quote operation."""

    # Test 400 (Bad request)
    quotes_url = url_for("api.quotes")
    data = {"quote_text": "Post quote."}
    res = client.post(quotes_url, headers=admin_headers, json=data)
    assert res.status_code == HttpStatus.BAD_REQUEST_400.value

    # Tests create quote
    data["author_name"] = "Post Author"
    data["author_image"] = "https://www.goodreads.com/quotes/tag/books"
    data["tags"] = ["post-test-tag"]

    res = client.post(quotes_url, headers=admin_headers, json=data)
    assert res.status_code == HttpStatus.CREATED_201.value

    # Test quote is on the database
    response_body = res.get_json()
    Quote = quote  # pylint: disable=invalid-name
    quote = Quote.objects.get(id=response_body["id"])

    assert str(quote.id) == response_body["id"]
    assert quote.quote_text == data["quote_text"]
    assert quote.author_image == data["author_image"]
    assert quote.tags == data["tags"]


def test_get_random_quote(client, user_headers, new_quote):
    """Tests the get random quote operation."""

    random_quote_url = url_for("api.random_quote")
    res = client.get(random_quote_url, headers=user_headers)
    data = res.get_json()

    assert res.status_code == HttpStatus.OK_200.value
    assert data["id"] == str(new_quote.id)
    assert data["quote_text"] == new_quote.quote_text
    assert data["author_name"] == new_quote.author_name
    assert data["tags"] == new_quote.tags
