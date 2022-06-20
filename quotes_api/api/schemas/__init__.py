"""Schemas initialization file."""

from quotes_api.api.schemas.quote import QuoteSchema
from quotes_api.api.schemas.author import AuthorSchema
from quotes_api.api.schemas.tag import TagSchema
from quotes_api.api.schemas.meta import MetadataSchema, LinksSchema

__all__ = [
    "QuoteSchema",
    "AuthorSchema",
    "TagSchema",
    "MetadataSchema",
    "LinksSchema",
]
