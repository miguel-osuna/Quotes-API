from datetime import datetime

from quotes_api.models import Quote, User, TokenBlacklist


def test_new_quote(quote):
    """ Test the creation of a new quote. """

    assert quote.quote_text == "Quote."
    assert quote.author_name == "Author"
    assert quote.author_image == "URL"
    assert "test-tag" in quote.tags


def test_new_user(user):
    """ Test the creation of a new user. """

    assert user.username == "user"
    assert user.email == "user@email.com"
    assert user.password != "user"
    assert user.active == True
    assert "basic" in user.roles


def test_new_token(user, access_token):
    """ Test the creation of a new token. """

    assert access_token.jti == "jti_example"
    assert access_token.token_type == "access"
    assert access_token.user == user
    assert access_token.revoked == False
    assert access_token.expires == datetime.timestamp(1608057500)
