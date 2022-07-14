import datetime
import time
from flask import Flask, render_template, session, request, redirect, current_app, g
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, InputRequired
from flask_pagedown import PageDown
from flask_pagedown.fields import PageDownField
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from . import main
from form import MarkDownForm
from ..database import Article, Tag, Category, Password, db
from ..config import base_url

def numOfArticle():
    pass




def articleOfTag(tagname) -> list:
    return [article for article in current_app.article_all if tagname in [tag.name for tag in article.tags]]


def articleOfCategory(name) -> list:
    return list([category.article for category in current_app.category_list if category.name == name][0])


@main.before_first_request
def init_tag_category_archive():
    current_app.tag_list = Tag.query.all()
    current_app.article_all = Article.query.order_by(Article.id).all()
    current_app.category_list = Category.query.all()
    year_list_t = list(set([article.year for article in current_app.article_all if article.year is not None]))

    # [[year,[month,num_of_article], [month, num_of_article]], [year, [month, num_of_article]]]
    current_app.year_month_list = [[year] for year in year_list_t]
    for year_month_list in current_app.year_month_list:
        year_month_list.extend(monthOfYear(year_month_list[0]))
    for year_month in current_app.year_month_list:
        for i in range(1, len(year_month)):
            year_month[i] = [year_month[i]]
            year_month[i].append(len(articleOfMonthYear(year_month[i][0], year_month[0])))


@main.route(base_url + '/page/<n>')
@main.route(base_url + '/', methods=['GET', 'POST'])
def index(n=1):
    n = int(n)
    session['index_page'] = n
    article_list_t = current_app.article_all
    session['max_page'] = len(article_list_t) / 5
    article_list_page = article_list_t[5 * n - 5: n * 5]

    url_list = []
    # tag_list = Tag.query.all()
    # category_list = Category.query.all()G
    # for a in article_list:
    #     url_list.append('/article/{0}'.format(a.id))
    # print(current_app.year_month_list)
    return render_template('home.html', article_list=article_list_page,
                            tag_list=current_app.tag_list, category_list=current_app.category_list,
                           year_month_list=current_app.year_month_list)


# @main.route(base_url + '/page/' + '<n>')
# def index
@main.route(base_url + '/article/<id>')
def route_to_article(id):
    print(id)
    a = Article.query.filter_by(id=id).first()
    return render_template('article.html', article=a)


@main.route(base_url + '/archive/<year>/<month>')
@main.route(base_url + '/category/<category_name>')
@main.route(base_url + '/tag/<tagname>')
def articles_of_tag(tagname=None, category_name=None, year=None, month=None):
    # search for articles whose tags have the tag named <tagname>
    article_list = []
    # category_list = Category.query.all()
    category = Category.query.filter_by(name=category_name).first()
    if tagname is not None:
        article_list = articleOfTag(tagname)
    elif category_name is not None:
        # article_list = list(category.article)
        article_list = articleOfCategory(category_name)
    elif year is not None and month is not None:
        article_list = articleOfMonthYear(month, year)
    # tag_list = Tag.query.all()
    return render_template('catalog.html', article_list=article_list, tag_list=current_app.tag_list,
                           category_list=current_app.category_list, year_month_list=current_app.year_month_list)


@main.route(base_url + '/post', methods=['GET', 'POST'])
def route_to_post():
    data = None
    form = MarkDownForm()
    category_name = [c.name for c in Category.query.all()]
    tag_name = [tag.name for tag in Tag.query.all()]
    # print(category_name)
    # print([tag.name for tag in Tag.query.all()])
    # print(current_app.tag_list)
    if form.validate_on_submit():
        print('here')
        password = form.password.data
        content = form.pagedown.data
        content  = '<mytag>' + content + '</mytag>'
        title = form.title.data
        subtitle = form.subtitle.data
        tag = form.tag.data
        category = form.category.data
        if check_password_hash(Password.query.all()[0].password_hash, password):
            print('correct')
            a = Article(title=title, content=content, post_time=datetime.datetime.now(), subtitle=subtitle, )
            if tag not in [t.name for t in current_app.tag_list]:
                t = Tag(name=tag)
            else:
                t = [tag_ for tag_ in current_app.tag_list if tag_.name == tag][0]
            if category not in [c.name for c in current_app.category_list]:
                c = Category(name=category)
            else:
                c = [c for c in current_app.category_list if c.name == category][0]
            a.category = c
            a.tags.append(t)
            db.session.add_all([a,t,c])
            db.session.commit()
        init_tag_category_archive()
        print('success')
        return "success"
    return render_template('post.html', form=form, category_name=category_name, tag_name=tag_name)


@main.route(base_url + '/about')
def about():
    pass