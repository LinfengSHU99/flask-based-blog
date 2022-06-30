import datetime

from flask import Flask, render_template, session, request, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import os
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
bootstrap = Bootstrap(app)
# app.config['SECRET_KEY'] = '?'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Kanade123@localhost:3306/blog'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
from Database import Database
Database()
db = SQLAlchemy(app)


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
    catagory = db.Column(db.String(64))
    content = db.Column(db.Text())
    tags = db.relationship('Tag', secondary=article_tag, backref=db.backref('tag', lazy='dynamic'), lazy='dynamic')
print(Tag.__name__)
db.drop_all()
db.create_all()
a1 = Article(title='test1', content=Config.content1, post_time=datetime.time(), subtitle='test1',  catagory='cata1')
a2 = Article(title='another test', content=Config.content2, post_time=datetime.time(), subtitle='another test',  catagory='cata2')
a3 = Article(title='another another test', content=Config.content2, post_time=datetime.time(), subtitle='another another test',  catagory='cata2')
t1 = Tag(name='tag1', url='/tag/' + 'tag1')
t2 = Tag(name='tag2', url='/tag/' + 'tag2')
a1.tags.append(t1)
a2.tags.append(t2)
a3.tags.append(t1)
a3.tags.append(t2)
db.session.add_all([a1, a2])
db.session.commit()


def abstract(content):
    if len(content) < 300:
        return content
    else:
        return content[:300] + '......'

@app.route('/', methods=['GET', 'POST'])
def index():  # put application's code here
    # name = ''
    # form = NameForm()
    # if request.method == 'POST':
        # print(request.get_data())
        # print(request.form[1])
        # name = request.get_data()
    # if form.validate_on_submit():
    #     name = form.name.data
    #     form.name.data = ''
    #     redirect('/' + name)
    # return render_template('template.html', name=name, form=form)
    article_list = Article.query.all()
    # title_list = [i.title for i in article_list]
    url_list = []
    for a in article_list:
        url_list.append('/article/{0}'.format(a.id))
    # return render_template('main_page.html', zip_list=zip(article_list, href))
    return render_template('home.html', article_list=article_list,
                           url_list=url_list, zip=zip, abstract=abstract)


@app.route('/article/<id>')
def route_to_article(id):
    print(id)
    a = Article.query.filter_by(id=id).first()
    return render_template('post.html', article=a)


@app.route('/tag/<tagname>')
def articles_of_tag(tagname):
    article_all = Article.query.all()
    # search for articles whose tags have the tag named <tagname>
    article_list = [article for article in article_all if tagname in [tag.name for tag in article.tags]]
    return render_template('catalog.html', article_list=article_list)




