import psycopg2
from psycopg2.extras import NamedTupleCursor, DictCursor


def open_connection(db_url):
    conn = psycopg2.connect(db_url)
    return conn


def add_given_url(db_url, given_url):
    with open_connection(db_url) as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                "INSERT INTO urls (name) VALUES (%s) RETURNING id;",
                (given_url,))
            id = cursor.fetchone()
            conn.commit()
        return id


def get_urls_list(db_url):
    with open_connection(db_url) as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute('SELECT * FROM urls ORDER BY id DESC;')
            urls = cursor.fetchall()
            conn.commit()
        return urls


def get_url_by_id(db_url, id):
    with open_connection(db_url) as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute('SELECT * FROM urls WHERE id=(%s)', (id,))
            url = cursor.fetchone()
            conn.commit()
        return url


def get_url_by_name(db_url, name):
    with open_connection(db_url) as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute('SELECT * FROM urls WHERE name=(%s)', (name,))
            url = cursor.fetchone()
            conn.commit()
        return url


def add_url_check(db_url, url_id, status):
    with open_connection(db_url) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                'INSERT INTO url_checks (url_id, status_code) \
                VALUES (%s, %s)', (url_id, status,))
            conn.commit()


def get_url_check(db_url, url_id):
    with open_connection(db_url) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                'SELECT * FROM url_checks WHERE url_id=(%s) \
                ORDER BY created_at DESC', (url_id, ))
            check_results = cursor.fetchall()
            conn.commit()
        return check_results


def get_all_last_checks(db_url):
    with open_connection(db_url) as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                'SELECT * FROM url_checks \
                INNER JOIN \
                (SELECT MAX(id) AS upd_id FROM url_checks GROUP BY url_id) \
                AS last_updates \
                ON last_updates.upd_id = url_checks.id')
            all_checks = cursor.fetchall()
            conn.commit()
        return all_checks
