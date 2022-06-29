from flask import Flask, render_template, session, request, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import os
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = '?'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Kanade123@localhost:3306/blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class NameForm(FlaskForm):
    name = StringField("name?")
    submit = SubmitField('submit')


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    content = db.Column(db.Text())


db.drop_all()
db.create_all()
a1 = Article(title='test1', content=Config.content1)
a2 = Article(title='another test', content=Config.content2)
db.session.add_all([a1, a2])
db.session.commit()


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
    href = []
    for a in article_list:
        href.append('/article/{0}'.format(a.id))
    return render_template('main_page.html', zip_list=zip(article_list, href))


@app.route('/main')
def main_page():
    article_list = Article.query.all()
    # title_list = [i.title for i in article_list]
    href = []
    for a in article_list:
        href.append('<a href="/article/{0}">{1}</a>'.format(a.id, a.title))
    return render_template('template.html', main_page=True, href=href)


@app.route('/article/<id>')
def route_to_article(id):
    print(id)
    a = Article.query.filter_by(id=id).first()
    print(a)
    print(a.content)
    return render_template('template.html', article=a)
@app.route('/<name>')
def index2(name):
    return render_template('template.html', name=name)



