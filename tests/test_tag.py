""" Test tag. """
from flask import url_for

from quotes_api.common import HttpStatus


def test_get_all_tags(client, user_headers):
    tags_url = url_for("api.tags")
    res = client.get(tags_url, headers=user_headers)

    assert res.status_code == HttpStatus.OK_200.value
