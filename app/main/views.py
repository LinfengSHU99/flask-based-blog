import datetime
from flask import Flask, render_template, session, request, redirect, current_app, g, make_response, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import markdown
from . import main
from .form import MarkDownForm, TestFrom
from ..database import Article, Tag, Category, Password, db
from ..config import base_url


def numOfArticle():
    pass


def articleOfMonthYear(month, year):
    return [article for article in current_app.article_all if article.year == year and article.month == month]


def monthOfYear(year):
    return list(set([article.month for article in current_app.article_all if article.year == year]))


def articleOfTag(tagname) -> list:
    return [article for article in current_app.article_all if tagname in [tag.name for tag in article.tags]]


def articleOfCategory(name) -> list:
    return list([category.articles for category in current_app.category_list if category.name == name][0])


@main.before_app_first_request
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
    article_list_t = list(current_app.article_all)
    # ordered by modification time?
    article_list_t.reverse()
    session['max_page'] = len(article_list_t) / 5
    article_list_page = article_list_t[5 * n - 5: n * 5]

    return render_template('home.html', article_list=article_list_page,
                           tag_list=current_app.tag_list, category_list=current_app.category_list,
                           year_month_list=current_app.year_month_list)


@main.route(base_url + '/article/<id>')
def route_to_article(id):
    a = Article.query.filter_by(id=id).first()
    return render_template('article.html', article=a)


@main.route(base_url + '/archive/<year>/<month>')
@main.route(base_url + '/category/<category_name>')
@main.route(base_url + '/tag/<tagname>')
def articles_of_tag(tagname=None, category_name=None, year=None, month=None):
    # search for articles whose tags have the tag named <tagname>
    article_list = []
    category = Category.query.filter_by(name=category_name).first()
    if tagname is not None:
        article_list = articleOfTag(tagname)
    elif category_name is not None:
        article_list = articleOfCategory(category_name)
    elif year is not None and month is not None:
        article_list = articleOfMonthYear(month, year)
    return render_template('catalog.html', article_list=article_list, tag_list=current_app.tag_list,
                           category_list=current_app.category_list, year_month_list=current_app.year_month_list)


@main.route(base_url + '/admin', methods=['GET', 'POST'])
def route_to_admin():
    if session.get('state') != 'registered':
        return redirect(url_for('main.route_to_login'))
    else:
        if request.form.get('action') is not None:
            action = request.form.get('action').split(' ')[0]
            article_id = request.form.get('action').split(' ')[1]
            if action == 'delete':
                article = Article.query.filter_by(id=article_id).first()
                db.session.delete(article)
                db.session.query(Tag).filter(~Tag.articles.any()).delete(synchronize_session=False)
                db.session.query(Category).filter(~Category.articles.any()).delete(synchronize_session=False)
                db.session.commit()
                init_tag_category_archive()
            elif action == 'modify':
                return redirect(url_for('main.modify', id=article_id))
        return render_template('admin.html', article_list=current_app.article_all)


@main.route(base_url + '/admin/modify<id>', methods=['POST', 'GET'])
def modify(id):
    if session.get('state') != 'registered':
        return redirect(url_for('main.route_to_login'))
    form = MarkDownForm()
    if id is not None:
        article = Article.query.filter_by(id=id).first()
        tag_list = []
        for tag in article.tags:
            tag_list.append(tag.name)
        tags = ','.join(tag_list)
        # each element in the list is a line of content.
        content_list = article.content.split('\n')
        return render_template('post.html', form=form, title=article.title, subtitle=article.subtitle,
                               category=article.category.name,
                               content_list=content_list, tags=tags)


@main.route(base_url + '/admin/post', methods=['POST', 'GET'])
def post():
    if session.get('state') != 'registered':
        return redirect(url_for('main.route_to_login'))
    data = None
    form = MarkDownForm()
    category_name = [c.name for c in Category.query.all()]
    tag_name = [tag.name for tag in Tag.query.all()]
    if form.validate_on_submit():
        content = form.pagedown.data
        # content = markdown.markdown(content)
        title = form.title.data
        subtitle = form.subtitle.data
        tags = form.tag.data
        tags = tags.split(',')
        category = form.category.data
        a = Article(title=title, content=content, post_time=datetime.datetime.now(), subtitle=subtitle, )
        for tag in tags:
            if tag not in [t.name for t in current_app.tag_list]:
                t = Tag(name=tag)
            else:
                t = [tag_ for tag_ in current_app.tag_list if tag_.name == tag][0]
            a.tags.append(t)
            db.session.add(t)
        if category not in [c.name for c in current_app.category_list]:
            c = Category(name=category)
        else:
            c = [c for c in current_app.category_list if c.name == category][0]
        a.category = c
        a.year = a.post_time.year
        a.month = a.post_time.month
        db.session.add_all([a, c])
        db.session.commit()
        init_tag_category_archive()
        return redirect(url_for('main.route_to_admin'))
    return render_template('post.html', form=form, category_name=category_name, tag_name=tag_name)


@main.route(base_url + '/about')
def about():
    return render_template('about.html')


@main.route(base_url + '/login', methods=['GET', 'POST'])
def route_to_login():
    form = TestFrom()
    if form.validate_on_submit():
        pw = form.title.data
        if pw == '123':
            # flask session is based on cookies. The info of session is encrypted using
            # SECRET_KEY, and stored in the browser.
            # By default, the cookies are cleared when the browser is closed. And that's the time
            # during which the session is maintained.
            session['state'] = 'registered'
            return redirect(url_for('main.index'))
        flash('Wrong Password!')
    return render_template('login.html', form=form)


@main.route('/in')
def in_():
    print(session.get('pw'))
    if request.cookies.get('state') == 'login':

        return 'you are in!'
    elif session.get('pw') == '666':
        return '666！'
    else:
        return 'fail!'
