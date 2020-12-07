from quotes_api.extensions import ma


class QuoteSchema(ma.Schema):
    id = ma.String(dump_only=True)
    quoteText = ma.String()
    authorName = ma.String()
    authorImage = ma.URL()
    tags = ma.List(ma.String())
