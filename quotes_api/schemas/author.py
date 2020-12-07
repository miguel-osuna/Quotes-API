from quotes_api.extensions import ma 

class AuthorSchema(ma.Schema):
    authorName = ma.String()
    authorImage = ma.URL()
