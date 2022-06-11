from flask import url_for


def generate_links(pagination, endpoint, **kwargs):

    self_link = url_for(
        endpoint=endpoint,
        page=pagination.page,
        per_page=pagination.per_page,
        _external=True,
        **kwargs
    )

    next_link = (
        url_for(
            endpoint=endpoint,
            page=pagination.next_num,
            per_page=pagination.per_page,
            _external=True,
            **kwargs
        )
        if pagination.has_next
        else None
    )

    previous_link = (
        url_for(
            endpoint=endpoint,
            page=pagination.prev_num,
            per_page=pagination.per_page,
            _external=True,
            **kwargs
        )
        if pagination.has_prev
        else None
    )

    return {"self": self_link, "prev": previous_link, "next": next_link}


def paginator(pagination, endpoint, schema, **kwargs):
    """Paginator for supported models."""

    # Create schemas
    schema = schema(many=True)

    # Creating list of items
    items = [item for item in pagination.items]
    links = generate_links(pagination, endpoint, **kwargs)

    response_body = {
        "meta": {
            "page_number": pagination.page,
            "page_size": pagination.per_page,
            "total_pages": pagination.pages,
            "total_records": pagination.total,
            "links": links,
        },
        "records": schema.dump(items),
    }

    return response_body


def author_paginator(pagination, endpoint, schema, **kwargs):
    """Paginator for list of authors."""

    authors = []
    for item in pagination.items:
        author_name = item.author_name

        if author_name not in authors:
            authors.append(author_name)
    links = generate_links(pagination, endpoint, **kwargs)

    response_body = {
        "meta": {
            "page_number": pagination.page,
            "page_size": len(authors),
            "total_pages": pagination.pages,
            "links": links,
        },
        "records": authors,
    }

    return response_body
