import datetime

from flask import Flask, render_template, session, request, redirect, current_app, g
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import os
from flask_sqlalchemy import SQLAlchemy
from config import Config, base_url

# from CustomFunc import CustomFunc
def numOfArticle():
    pass
app = Flask(__name__)
# session['page'] = 1
bootstrap = Bootstrap(app)
app.jinja_env.globals['str'] = str
app.jinja_env.globals['zip'] = zip
app.jinja_env.globals['len'] = len
app.jinja_env.globals['list'] = list
app.jinja_env.globals['base_url'] = base_url
# app.jinja_env.globals['page'] = page
# CustomFunc(app)
# app.config['SECRET_KEY'] = '?'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Kanade123@localhost:3306/blog'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
from Database import Database
Database()
db = SQLAlchemy(app)
@app.before_first_request
def init_tag_category_archive():
    g.tag_list = tag_list = Tag.query.all()

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
    post_time = db.Column(db.Time())
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    content = db.Column(db.Text())
    tags = db.relationship('Tag', secondary=article_tag, backref=db.backref('tag', lazy='dynamic'), lazy='dynamic')
    year = db.Column(db.String(10))
    month = db.Column(db.String(10))


# article_category = db.Table('article_category', db.Column('article_id', db.Integer, db.ForeignKey('article.id')),
#                             db.Column('category_id', db.Integer, db.ForeignKey('category.id')))


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    article = db.relationship('Article', backref='category')
    name = db.Column(db.String(64))


db.drop_all()
db.create_all()
a1 = Article(title='test1', content=Config.content1, post_time=datetime.time(), subtitle='test1',year='2020', month='Jan' )
a2 = Article(title='another test', content=Config.content2, post_time=datetime.time(), subtitle='another test', year='2020',month='Feb' )
a3 = Article(title='another another test', content=Config.content2, post_time=datetime.time(), subtitle='another another test', year='2020',month='Jan')
a4 = Article(title='test1', content=Config.content1, post_time=datetime.time(), subtitle='test1', year='2021', month='Feb')
a5 = Article(title='test1', content=Config.content1, post_time=datetime.time(), subtitle='test1',  )
a6 = Article(title='test1', content=Config.content1, post_time=datetime.time(), subtitle='test1',  )
a7 = Article(title='test1', content=Config.content1, post_time=datetime.time(), subtitle='test1',  )
a8 = Article(title='test1', content=Config.content1, post_time=datetime.time(), subtitle='test1',  )
a9 = Article(title='test1', content=Config.content1, post_time=datetime.time(), subtitle='test1',  )
a10 = Article(title='test1', content=Config.content1, post_time=datetime.time(), subtitle='test1',  )
a11 = Article(title='test1', content=Config.content1, post_time=datetime.time(), subtitle='test1',  )
a12 = Article(title='test1', content=Config.content1, post_time=datetime.time(), subtitle='test1',  )
a13 = Article(title='test1', content=Config.content1, post_time=datetime.time(), subtitle='test1',  )
a14 = Article(title='test1', content=Config.content1, post_time=datetime.time(), subtitle='test1',  )
t1 = Tag(name='tag1', url='/tag/' + 'tag1')
t2 = Tag(name='tag2', url='/tag/' + 'tag2')
c1 = Category(name='category1')
c2 = Category(name='category2')
a1.category = c1
a2.category = c1
a3.category = c2
a5.category = c1
print(list(c1.article))
a1.tags.append(t1)
a2.tags.append(t2)
a3.tags.append(t1)
a3.tags.append(t2)
db.session.add_all([a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14])
db.session.commit()

def abstract(content):
    if len(content) < 300:
        return content
    else:
        return content[:300] + '......'



@app.route(base_url + '/page/<n>')
@app.route(base_url + '/', methods=['GET', 'POST'])
def index(n=1):
    n = int(n)
    session['index_page'] = n
    article_list_t = Article.query.order_by(Article.id).all()
    session['max_page'] = len(article_list_t) // 5
    article_list = article_list_t[5 * n - 5: n * 5]

    url_list = []
    tag_list = Tag.query.all()
    category_list = Category.query.all()
    for a in article_list:
        url_list.append('/article/{0}'.format(a.id))

    return render_template('home.html', article_list=article_list,
                           abstract=abstract, tag_list=tag_list, category_list=category_list)


# @app.route(base_url + '/page/' + '<n>')
# def index
@app.route(base_url + '/article/<id>')
def route_to_article(id):
    print(id)
    a = Article.query.filter_by(id=id).first()
    return render_template('post.html', article=a)


@app.route(base_url + '/category/<category_name>')
@app.route(base_url + '/tag/<tagname>')
def articles_of_tag(tagname=None, category_name=None):
    article_all = Article.query.all()
    # search for articles whose tags have the tag named <tagname>
    article_list = []
    category_list = Category.query.all()
    category = Category.query.filter_by(name = category_name).first()
    if tagname is not None:
        article_list = [article for article in article_all if tagname in [tag.name for tag in article.tags]]
    elif category_name is not None:
        article_list = list(category.article)
    tag_list = Tag.query.all()
    return render_template('catalog.html', article_list=article_list, tag_list=tag_list, category_list=category_list)




