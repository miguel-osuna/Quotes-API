from datetime import datetime

from quotes_api.models import Quote, User, TokenBlacklist


def test_new_quote(new_quote):
    """ Test the creation of a new quote. 
    
    GIVEN a Quote model
    WHEN a new Quote is created
    THEN check the quote_text, author_name, author_image and tags fields are defined correctly
    """

    assert new_quote.quote_text == "Quote."
    assert new_quote.author_name == "Author"
    assert new_quote.author_image == "URL"
    assert "test-tag" in new_quote.tags


def test_new_user(new_user):
    """ Test the creation of a new user. 
    
    GIVEN a User model
    WHEN a new User is created
    THEN check the username, email, password, active and roles fields are defined correctly
    """

    assert new_user.username == "user"
    assert new_user.email == "user@email.com"
    assert new_user.password != "user"
    assert new_user.active == True
    assert "basic" in new_user.roles


def test_new_token(new_user, new_access_token):
    """ Test the creation of a new token. 
    
    GIVEN a TokenBlacklist model
    WHEN a new access token is created 
    THEN check the jti, token_type, user, revoked and expires fields are defined correctly
    """

    assert new_access_token.jti == "jti_example"
    assert new_access_token.token_type == "access"
    assert new_access_token.user.id == new_user.id
    assert new_access_token.revoked == False
    assert new_access_token.expires == datetime.fromtimestamp(1608057500)
