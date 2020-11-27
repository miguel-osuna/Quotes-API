from quotes_api.api.resources.quote import (
    QuoteResource,
    QuoteList,
    QuoteRandom,
    QuoteSearch,
)
from quotes_api.api.resources.author import AuthorQuoteList, AuthorQuoteRandom
from quotes_api.api.resources.category import (
    CategoryList,
    CategoryQuoteList,
    CategoryQuoteRandom,
)

__all__ = [
    "QuoteResource",
    "QuoteList",
    "QuoteRandom",
    "QuoteSearch",
    "AuthorQuoteList",
    "AuthorQuoteRandom",
    "CategoryList",
    "CategoryQuoteList",
    "CategoryQuoteRandom",
]
