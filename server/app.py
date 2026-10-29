#!/usr/bin/env python3

from flask import request, session, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

import os
from config import create_app, db, api
from models import Book, BookSchema

env = os.getenv("FLASK_ENV", "dev")
app = create_app(env)

# Pagination defaults and limits
DEFAULT_PAGE = 1
DEFAULT_PER_PAGE = 5
MAX_PER_PAGE = 100


class Books(Resource):
    def get(self):
        """Return a paginated list of books.

        Query params:
            page     (int, default 1)  - which page of results to return
            per_page (int, default 5)  - how many books per page (max 100)
        """
        # Step 1: read query params; fall back to defaults if missing/invalid
        page = request.args.get("page", DEFAULT_PAGE, type=int)
        per_page = request.args.get("per_page", DEFAULT_PER_PAGE, type=int)

        # Guard against zero/negative values and oversized pages
        if page < 1:
            page = DEFAULT_PAGE
        if per_page < 1:
            per_page = DEFAULT_PER_PAGE
        per_page = min(per_page, MAX_PER_PAGE)

        # Step 2: paginate. Order by id so pages are stable between requests.
        # error_out=False -> an out-of-range page returns an empty list
        # instead of raising a 404.
        pagination = Book.query.order_by(Book.id).paginate(
            page=page, per_page=per_page, error_out=False
        )

        # Step 3: structured response with metadata
        return {
            "page": page,
            "per_page": per_page,
            "total": pagination.total,
            # always at least 1, even when there are no books
            "total_pages": max(pagination.pages, 1),
            "items": BookSchema(many=True).dump(pagination.items),
        }, 200


api.add_resource(Books, '/books', endpoint='books')


if __name__ == '__main__':
    app.run(port=5555, debug=True)