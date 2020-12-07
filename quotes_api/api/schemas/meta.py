from quotes_api.extensions import ma


class LinksSchema(ma.Schema):
    self_link = ma.URL()
    next_link = ma.URL(allow_none=True)
    previous_link = ma.URL(allow_none=True)


class MetadataSchema(ma.Schema):
    page_number = ma.Integer()
    page_size = ma.Integer()
    total_pages = ma.Integer()
    total_records = ma.Integer()
    links = ma.Nested(LinksSchema)

