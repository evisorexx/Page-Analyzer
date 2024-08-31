import os
from page_analyzer.data_validator import validate_url
from dotenv import load_dotenv
from page_analyzer.sql import (
    add_given_url,
    get_urls_list,
    get_url_by_id,
    get_url_by_name
)
from flask import (
    Flask,
    render_template,
    request,
    flash,
    url_for,
    redirect
    )



load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template(
        'index.html'
    )


@app.post('/urls')
def add_url():
    given_url = request.form.get('url').rstrip('/')
    if not validate_url(given_url):
        flash('Введен некорректный URL!', 'error')
        return redirect(url_for('index'))
    if get_url_by_name(given_url):
        flash('URL уже есть в базе!', 'info')
        return redirect(url_for('index'))
    new_id = add_given_url(given_url)
    flash('URL успешно добавлен!', 'success')
    return redirect(
        url_for('url', id=new_id.id)
    )


@app.get('/urls')
def all_urls():
    return render_template(
        'urls.html',
        urls=get_urls_list()
    )


@app.get('/urls/<int:id>')
def url(id):
    url = get_url_by_id(id)
    return render_template(
        'url.html',
        url=url
    )
