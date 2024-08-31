import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import NamedTupleCursor

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

db = psycopg2.connect(DATABASE_URL)


def add_given_url(given_url):
    with db.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute("INSERT INTO urls (name) VALUES (%s) RETURNING id;",
                            (given_url,))
        id = cursor.fetchone()
    return id


def get_urls_list():
    with db.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute('SELECT * FROM urls ORDER BY id DESC;')
        urls = cursor.fetchall()
    return urls


def get_url_by_id(id):
    with db.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute('SELECT * FROM urls WHERE id=(%s)', (id,))
        url = cursor.fetchone()
    return url


def get_url_by_name(name):
    with db.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute('SELECT * FROM urls WHERE name=(%s)', (name,))
        url = cursor.fetchone()
    return True if url else False
