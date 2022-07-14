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
from config import Config, base_url
import markdown
from CustomFunc import abstract


def numOfArticle():
    pass


def monthOfYear(year):
    return list(set([article.month for article in current_app.article_all if article.year == year]))


def articleOfMonthYear(month, year):
    return [article for article in current_app.article_all if article.year == year and article.month == month]


def articleOfTag(tagname) -> list:
    return [article for article in current_app.article_all if tagname in [tag.name for tag in article.tags]]


def articleOfCategory(name) -> list:
    return list([category.article for category in current_app.category_list if category.name == name][0])


app = Flask(__name__)
# session['page'] = 1
bootstrap = Bootstrap(app)
pagedown = PageDown(app)
app.jinja_env.globals['str'] = str
app.jinja_env.globals['zip'] = zip
app.jinja_env.globals['len'] = len
app.jinja_env.globals['list'] = list
app.jinja_env.globals['base_url'] = base_url
app.jinja_env.globals['monthOfYear'] = monthOfYear
app.jinja_env.globals['articleOfMonthYear'] = articleOfMonthYear
app.jinja_env.globals['abstract'] = abstract
# app.jinja_env.globals['page'] = page
# CustomFunc(app)
# app.config['SECRET_KEY'] = '?'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Kanade123@localhost:3306/blog'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
from Database import Database

Database(app)
db = SQLAlchemy(app)


@app.before_first_request
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


class MarkDownForm(FlaskForm):
    title = StringField('Title of the article', validators=[DataRequired()])
    subtitle = StringField('Subtitle of the article')
    category = StringField('Chose the category', validators=[DataRequired()])
    tag = StringField('Chose the tag', validators=[DataRequired()])
    password = PasswordField('Input the token', validators=[DataRequired()])
    pagedown = PageDownField('Enter your markdown', validators=[DataRequired()])
    submit = SubmitField('Submit')

class NameForm(FlaskForm):
    name = StringField("name?")
    submit = SubmitField('submit')


article_tag = db.Table('article_tag', db.Column('article_id', db.Integer, db.ForeignKey('article.id')),
                       db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    url = db.Column(db.String(64))


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    subtitle = db.Column(db.String(64))
    post_time = db.Column(db.DateTime())
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    content = db.Column(db.Text())
    tags = db.relationship('Tag', secondary=article_tag, backref=db.backref('tag', ), lazy='immediate')
    year = db.Column(db.String(10))
    month = db.Column(db.String(10))


# article_category = db.Table('article_category', db.Column('article_id', db.Integer, db.ForeignKey('article.id')),
#                             db.Column('category_id', db.Integer, db.ForeignKey('category.id')))


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    article = db.relationship('Article', backref='category', lazy='immediate')
    name = db.Column(db.String(64))

class Password(db.Model):
    __tablename__ = 'password'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(64))
    password_hash = db.Column(db.String(300))

db.drop_all()
db.create_all()
a1 = Article(title='test1', content=Config.content1, post_time=datetime.datetime.now(), subtitle='test1', year='2020',
             month='Jan')
a2 = Article(title='another test', content=Config.content2, post_time=datetime.datetime.now(), subtitle='another test',
             year='2020', month='Feb')
a3 = Article(title='another another test', content=Config.content2, post_time=datetime.datetime.now(),
             subtitle='another another test', year='2020', month='Jan')
a4 = Article(title='test1', content=Config.content1, post_time=datetime.datetime.now(), subtitle='test1', year='2021',
             month='Feb')
a5 = Article(title='test1', content=Config.content1, post_time=datetime.datetime.now(), subtitle='test1', )
a6 = Article(title='test1', content=Config.content1, post_time=datetime.datetime.now(), subtitle='test1', )
a7 = Article(title='test1', content=Config.content1, post_time=datetime.datetime.now(), subtitle='test1', )
a8 = Article(title='test1', content=Config.content1, post_time=datetime.datetime.now(), subtitle='test1', )
a9 = Article(title='test1', content=Config.content1, post_time=datetime.datetime.now(), subtitle='test1', )
a10 = Article(title='test1', content=Config.content1, post_time=datetime.datetime.now(), subtitle='test1', )
a11 = Article(title='test1', content=Config.content1, post_time=datetime.datetime.now(), subtitle='test1', )
a12 = Article(title='test1', content=Config.content1, post_time=datetime.datetime.now(), subtitle='test1', )
a13 = Article(title='test1', content=Config.content1, post_time=datetime.datetime.now(), subtitle='test1', )
a14 = Article(title='test1', content=Config.content1, post_time=datetime.datetime.now(), subtitle='test1', )
t1 = Tag(name='tag1', url='/tag/' + 'tag1')
t2 = Tag(name='tag2', url='/tag/' + 'tag2')
c1 = Category(name='category1')
c2 = Category(name='category2')
p1 = Password(password='Kanade123', password_hash=generate_password_hash('Kanade123'))
a1.category = c1
a2.category = c1
a3.category = c2
a5.category = c1
print(list(c1.article))
a1.tags.append(t1)
a2.tags.append(t2)
a3.tags.append(t1)
a3.tags.append(t2)
db.session.add_all([a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, p1, c1, c2, t1, t2])
for a in Article.query.all():
    a.year = a.post_time.year
    a.month = a.post_time.month
db.session.commit()
# db.session.close()


@app.route(base_url + '/page/<n>')
@app.route(base_url + '/', methods=['GET', 'POST'])
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


# @app.route(base_url + '/page/' + '<n>')
# def index
@app.route(base_url + '/article/<id>')
def route_to_article(id):
    print(id)
    a = Article.query.filter_by(id=id).first()
    return render_template('article.html', article=a)


@app.route(base_url + '/archive/<year>/<month>')
@app.route(base_url + '/category/<category_name>')
@app.route(base_url + '/tag/<tagname>')
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


@app.route(base_url + '/post', methods=['GET', 'POST'])
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


@app.route(base_url + '/about')
def about():
    pass