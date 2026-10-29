#!/usr/bin/env python3

from random import randint, choice as rc

from faker import Faker
import os
from app import create_app
from models import db, Book

fake = Faker()

env = os.getenv("FLASK_ENV", "dev")
app = create_app(env)

with app.app_context():

    print("Deleting all books...")
    Book.query.delete()

    fake = Faker()

    print("Creating books...")
    books = []
    for i in range(500):
        title = fake.sentence(nb_words=4)
        author = fake.name()
        description = fake.paragraph(nb_sentences=5)
        
        book = Book(
            title=title,
            author=author,
            description=description
        )

        books.append(book)

    db.session.add_all(books)
    
    db.session.commit()
    print("Complete.")
