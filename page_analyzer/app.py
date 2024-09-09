import os
import requests
from requests.exceptions import ReadTimeout, ConnectionError
from page_analyzer.data_validator import validate_url, normalize_url
from dotenv import load_dotenv
from page_analyzer.html_parser import parser
from flask import (
    Flask,
    render_template,
    request,
    flash,
    url_for,
    redirect,
    abort
)
from page_analyzer.db import (
    add_given_url,
    get_urls_list,
    get_url_by_id,
    get_url_by_name,
    add_url_check,
    get_url_check,
    get_all_last_checks,
    delete_url
)

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
DATABASE_URL = os.environ.get('DATABASE_URL')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/not_found.html'), 404


@app.route('/')
def index():
    return render_template(
        'pages/index.html'
    )


@app.post('/urls')
def add_url():
    given_url = request.form.get('url')
    if not validate_url(given_url):
        flash('Некорректный URL', 'danger')
        return render_template('pages/index.html'), 422
    else:
        given_url = normalize_url(given_url)
    if get_url_by_name(DATABASE_URL, given_url):
        url = get_url_by_name(DATABASE_URL, given_url)
        flash('Страница уже существует', 'info')
        return redirect(url_for('url', id=url.id))
    new_id = add_given_url(DATABASE_URL, given_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(
        url_for('url', id=new_id.id)
    )


@app.get('/urls')
def all_urls():
    url_checks = get_all_last_checks(DATABASE_URL)
    return render_template(
        'pages/urls.html',
        urls=get_urls_list(DATABASE_URL),
        url_checks=url_checks
    )


@app.get('/urls/<int:id>')
def url(id):
    url = get_url_by_id(DATABASE_URL, id)
    if not url:
        return abort(404)
    check_results = get_url_check(DATABASE_URL, id)
    return render_template(
        'pages/url.html',
        url=url,
        check_results=check_results
    )


@app.post('/urls/<int:id>/delete')
def url_delete(id):
    delete_url(DATABASE_URL, id)
    flash('Страница удалена успешно', 'success')
    return redirect(url_for('index'))


@app.post('/urls/<int:id>/checks')
def url_check(id):
    url = get_url_by_id(DATABASE_URL, id)[1]
    try:
        response = requests.get(url, timeout=5)
        html_values = parser(response.text)
        response.raise_for_status()
        status = response.status_code
        add_url_check(DATABASE_URL, id, status, html_values)
        flash('Страница успешно проверена', 'success')
    except ReadTimeout:
        flash('Ресурс не отвечает', 'warning')
    except ConnectionError:
        flash('Ресурса не существует, советуем удалить его из базы',
              'warning')
    except Exception:
        flash('Произошла ошибка при проверке', 'danger')
    finally:
        return redirect(url_for('url', id=id))
