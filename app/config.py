import markdown
import os
from flask import current_app
from bs4 import BeautifulSoup
from math import ceil

basedir = os.path.abspath(os.path.dirname(__file__))

base_url = ''
def abstract(content):
    soup = BeautifulSoup(content)
    mytag = soup.mytag
    s = mytag.get_text()
    return s


def monthOfYear(year):
    return list(set([article.month for article in current_app.article_all if article.year == year]))


def articleOfMonthYear(month, year):
    return [article for article in current_app.article_all if article.year == year and article.month == month]

class Config:
    with open('Devlog.md', 'r') as fp:
        content1 = fp.read()
    content1 = markdown.markdown(content1)
    content1 = '<mytag>' + content1
    content1 = content1 + '</mytag>'
    content2 = '<mytag>Flask-SQLAlchemy provides a base class for models as\
well as a set of helper classes and functions that are used</mytag>'


    @staticmethod
    def init_app(app):
        app.config['SECRET_KEY'] = '?'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        app.jinja_env.globals['str'] = str
        app.jinja_env.globals['zip'] = zip
        app.jinja_env.globals['len'] = len
        app.jinja_env.globals['list'] = list
        app.jinja_env.globals['range'] = range
        app.jinja_env.globals['ceil'] = ceil
        app.jinja_env.globals['base_url'] = base_url
        app.jinja_env.globals['monthOfYear'] = monthOfYear
        app.jinja_env.globals['articleOfMonthYear'] = articleOfMonthYear
        app.jinja_env.globals['abstract'] = abstract
