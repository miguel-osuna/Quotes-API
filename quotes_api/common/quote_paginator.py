from flask import url_for


def quote_paginator(pagination, endpoint, **kwargs):

    # Creating list of quotes

    quote_items = []
    for quote in pagination.items:
        quote_object = {
            "id": str(quote.id),
            "quoteText": quote.quoteText,
            "authorName": quote.authorName,
            "authorImage": quote.authorImage,
            "tags": quote.tags,
        }
        quote_items.append(quote_object)

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

    body_response = {
        "meta": {
            "page_number": pagination.page,
            "page_size": pagination.per_page,
            "total_pages": pagination.pages,
            "total_records": pagination.total,
            "links": {"self": self_link, "prev": previous_link, "next": next_link},
        },
        "records": quote_items,
    }

    return body_response

