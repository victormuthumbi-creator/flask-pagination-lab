# Lab: Flask Pagination

## Introduction

In this lab, you'll add server-side pagination to an existing Flask API endpoint. Right now, your API returns all books when a client makes a request to /books. That’s fine with 10 entries, but in production systems, this approach can slow down your app and flood the frontend with too much data.

Your goal is to refactor the endpoint to:

* Accept `?page` and `?per_page` query parameters
* Return only a subset of records
* Include metadata (like total, page, total_pages) in the response

This mirrors the structure used by APIs across the web from Shopify to Reddit to GitHub.

## Tools & Resources

- [GitHub Repo](https://github.com/learn-co-curriculum/flask-pagination-lab)
- [Flask SQLAlchemy Docs - paginate](https://flask-sqlalchemy.readthedocs.io/en/stable/pagination/)

## Set Up

The starter code includes a Flask app and seed data for books.

To get started:

```bash
pipenv install && pipenv shell
cd server
flask db init
flask db migrate -m "initial migration"
flask db upgrade head
python seed.py
python app.py
```

You can view the API in your browser or using Postman. Test pagination by visiting
http://localhost:5555/books?page=1&per_page=5.

## Instructions

### Task 1: Define the Problem

Your current /books endpoint returns every book in the database. The frontend team wants this replaced with a paginated response that:

* Uses page and per_page query parameters
* Returns only the requested chunk of data
* Includes metadata like the total number of pages

### Task 2: Determine the Design

Backend Requirements:
* Accept `?page=<int>` and `?per_page=<int>` via `request.args`
* Use `.paginate()` on your SQLAlchemy query
* Return a structured JSON response like:

```json
{
  "page": 1,
  "per_page": 5,
  "total": 30,
  "total_pages": 6,
  "items": [
    { "id": 1, "title": "Apple Pie" },
    // ...
  ]
}
```

### Task 3: Develop, Test, and Refine the Code

#### Step 1: Accept Query Parameters

* page
* per_page

#### Step 2: Use .paginate() in Your Query

Use the SQLAlchemy `.paginate()` method to get the correct books by the query params.

#### Step 3: Return a Structured Response

Format response with the proper metadata:
* page
* per_page
* total
* total_pages
* items

#### Step 4: Test the Pagination Logic

Test routes in browser or Postman. Run the test suite with:
```bash
pytest
```

#### Step 5: Commit and Push Git History

* Commit and push your code:

```bash
git add .
git commit -m "final solution"
git push
```

* If you created a separate feature branch, remember to open a PR on main and merge.

### Task 4: Document and Maintain

Optional Best Practice documentation steps:
* Add comments to the code to explain purpose and logic, clarifying intent and functionality of your code to other developers.
* Update README text to reflect the functionality of the application following https://makeareadme.com. 
  * Add screenshot of completed work included in Markdown in README.
* Delete any stale branches on GitHub
* Remove unnecessary/commented out code
* If needed, update git ignore to remove sensitive data

## Submit Solution

CodeGrade will use the same test suite as the test suite included.

Once all tests are passing, commit and push your work using `git` to submit to CodeGrade through Canvas.

---

## Solution: Paginated `/books` Endpoint

`GET /books` now returns one page of books at a time instead of every record.

### Query parameters

| Param      | Default | Notes                                              |
|------------|---------|----------------------------------------------------|
| `page`     | `1`     | Page number (values below 1 fall back to 1)        |
| `per_page` | `5`     | Items per page (values below 1 fall back to 5, capped at 100) |

### Example

```
GET http://localhost:5555/books?page=2&per_page=3
```

```json
{
  "page": 2,
  "per_page": 3,
  "total": 500,
  "total_pages": 167,
  "items": [
    { "id": 4, "title": "...", "author": "...", "description": "..." }
  ]
}
```

### How it works

- `request.args.get(..., type=int)` reads and validates the query params.
- `Book.query.order_by(Book.id).paginate(page=..., per_page=..., error_out=False)` fetches only the requested slice. Ordering by `id` keeps pages consistent between requests.
- `error_out=False` means a page past the end returns `"items": []` with a 200 instead of a 404.
- The response includes `page`, `per_page`, `total`, `total_pages` and `items`.

### Run the tests

```bash
pytest
```

### Screenshot

![Paginated response](screenshots/pagination.png)
