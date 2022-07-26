from .. import db

article_tag = db.Table('article_tag', db.Column('article_id', db.Integer, db.ForeignKey('article.id')),
                       db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    # url = db.Column(db.String(64))
    # article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    articles = db.relationship('Article', secondary=article_tag, back_populates='tags', lazy='dynamic', cascade='all, delete')

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    subtitle = db.Column(db.String(64))
    post_time = db.Column(db.DateTime())
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='articles', lazy='immediate', )
    content = db.Column(db.Text())
    # tags = db.relationship('Tag', secondary=article_tag, backref=db.backref('tag', ), lazy='immediate')
    tags = db.relationship('Tag', secondary=article_tag, back_populates='articles', lazy='immediate')
    year = db.Column(db.String(10))
    month = db.Column(db.String(10))


# article_category = db.Table('article_category', db.Column('article_id', db.Integer, db.ForeignKey('article.id')),
#                             db.Column('category_id', db.Integer, db.ForeignKey('category.id')))


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    articles = db.relationship('Article', back_populates='category', lazy='immediate', )
    name = db.Column(db.String(64), unique=True)

class Password(db.Model):
    __tablename__ = 'password'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(64))
    password_hash = db.Column(db.String(300))