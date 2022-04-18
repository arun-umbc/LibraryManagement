import datetime
import os
import random
import time
from hashlib import md5

import pandas as pd
import rstr
from faker import Faker

from library_app.models import Book, User, Request, Reserve
from utilities.constants import ROLE_TYPES, DEPARTMENTS, STUDY_LEVEL, REQUEST_STATUS, REQUEST_FOR, RESERVE_STATUS

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


def load_students():
    try:
        departments = [a for a, b in DEPARTMENTS.choices()]
        study_level = [a for a, b in STUDY_LEVEL.choices()]
        for i in range(1, 1000):
            student = User()
            student.user_id = rstr.xeger(r'[A-Z][A-Z]\d\d\d\d\d')
            student.role = ROLE_TYPES.student
            student.department = random.choice(departments)
            student.study_level = random.choice(study_level)
            student.set_password('password')
            student.save()
    except Exception as e:
        print(e)


def load_librarians():
    try:
        for i in range(1, 3):
            librarian = User()
            librarian.user_id = rstr.xeger(r'[A-Z][A-Z]\d\d\d\d\d')
            librarian.role = ROLE_TYPES.librarian
            librarian.set_password('password')
            librarian.save()
    except Exception as e:
        print(e)


def load_request():
    try:
        students = User.objects.filter(role=ROLE_TYPES.student)
        books = Book.objects.all()
        user_count = len(students)
        book_count = len(books)
        request_status = [a for a, b in REQUEST_STATUS.choices()]
        request_for = [a for a, b in REQUEST_FOR.choices()]

        for i in range(1, 10000):
            request = Request()
            request.request_id = md5(f"{time.time()}".encode('utf-8')).hexdigest()
            request.user = students[random.randint(0, user_count-1)]
            request.book = books[random.randint(0, book_count-1)]
            request.request_status = random.choice(request_status)
            request.request_for = random.choice(request_for)
            request.save()
    except Exception as e:
        print(e)


def load_reserve():
    try:
        fake = Faker()
        reserve_status = [a for a, b in RESERVE_STATUS.choices()]
        requests = Request.objects.filter(request_status=REQUEST_STATUS.approved)
        for request in requests:
            reserve = Reserve()
            reserve.reserve_id = md5(f"{time.time()}".encode('utf-8')).hexdigest()
            reserve.request = request
            if request.request_for == REQUEST_FOR.rent:
                reserve.reserve_status = random.choice(reserve_status)
                reserve.rented_date = fake.date_time_between(start_date='-2y', end_date='now')
                reserve.return_date = reserve.rented_date + datetime.timedelta(days=15)
                if reserve.reserve_status == RESERVE_STATUS.overdue:
                    reserve.fine = request.book.fine
                if reserve.reserve_status == RESERVE_STATUS.close:
                    reserve.returned_date = reserve.rented_date + datetime.timedelta(days=random.randint(5, 14))
            else:
                reserve.purchase_date = datetime.datetime.now()
                reserve.reserve_status = RESERVE_STATUS.close
            reserve.save()
    except Exception as e:
        print(e)
