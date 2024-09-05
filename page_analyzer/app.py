import os
from page_analyzer.data_validator import validate_url
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    flash,
    url_for,
    redirect
    )
from page_analyzer.sql import (
    add_given_url,
    get_urls_list,
    get_url_by_id,
    get_url_by_name
)

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
DATABASE_URL = os.environ.get('DATABASE_URL')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def index():
    return render_template(
        'index.html'
    )


@app.post('/urls')
def add_url():
    given_url = validate_url(request.form.get('url'))
    if not given_url:
        flash('Введен некорректный URL!', 'danger')
        return redirect(url_for('index'))
    if get_url_by_name(DATABASE_URL, given_url):
        url = get_url_by_name(DATABASE_URL, given_url)
        flash('URL уже есть в базе!', 'info')
        return redirect(url_for('url', id=url.id))
    new_id = add_given_url(DATABASE_URL, given_url)
    flash('URL успешно добавлен!', 'success')
    return redirect(
        url_for('url', id=new_id.id)
    )


@app.get('/urls')
def all_urls():
    return render_template(
        'urls.html',
        urls=get_urls_list(DATABASE_URL)
    )


@app.get('/urls/<int:id>')
def url(id):
    url = get_url_by_id(DATABASE_URL, id)
    return render_template(
        'url.html',
        url=url
    )


@app.post('/urls/<int:id>/checks')
def url_check(id):
    pass
