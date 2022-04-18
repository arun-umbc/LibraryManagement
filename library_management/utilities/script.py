import os
import random
import time
from hashlib import md5

import pandas as pd

from library_app.models import Book

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


def load_books():
    try:
        books = pd.read_csv(BASE_DIR + "/data/books.csv")
        for index, row in books.iterrows():
            if row['Author']:
                book = Book()
                book.book_id = md5(f"{time.time()}".encode('utf-8')).hexdigest()
                book.name = row['Title']
                book.author = row['Author']
                book.total_copies = random.choice(range(5, 25))
                book.copies_available_rent = random.choice(range(1, book.total_copies))
                book.copies_available_sale = book.total_copies - book.copies_available_rent
                book.fine = round(random.uniform(1, 10), 2)
                book.price = round(random.uniform(30, 200), 2)
                book.save()
    except Exception as e:
        print(e)
