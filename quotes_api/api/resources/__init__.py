from quotes_api.api.resources.quote import (
    QuoteResource,
    QuoteList,
    QuoteRandom,
    QuoteSearch,
)
from quotes_api.api.resources.author import (
    AuthorList,
    AuthorQuoteRandom,
)
from quotes_api.api.resources.category import (
    CategoryList,
    CategoryQuoteRandom,
)

__all__ = [
    "QuoteResource",
    "QuoteList",
    "QuoteRandom",
    "QuoteSearch",
    "AuthorList",
    "AuthorQuoteRandom",
    "CategoryList",
    "CategoryQuoteRandom",
]
