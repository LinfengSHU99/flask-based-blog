import os
from app import create_app
from flask_migrate import Migrate, upgrade
from app import db
from app.database import Article, Tag, Password, Category

blog = create_app()
# migrate = Migrate(blog, db)
if os.getenv('PRODUCTION', 0) != '1':
    from app.config import Config
    import datetime
    from werkzeug.security import generate_password_hash
    db.drop_all()
    db.create_all()
    a1 = Article(title='test1', content=Config.content1, post_time=datetime.datetime.utcnow(), subtitle='test1', year='2020',
                 month='Jan')
    a2 = Article(title='another test', content=Config.content2, post_time=datetime.datetime.utcnow(), subtitle='another test',
                 year='2020', month='Feb')
    a3 = Article(title='another another test', content=Config.content2, post_time=datetime.datetime.utcnow(),
                 subtitle='another another test', year='2020', month='Jan')
    a4 = Article(title='test1', content=Config.content1, post_time=datetime.datetime.utcnow(), subtitle='test1', year='2021',
                 month='Feb')
    a5 = Article(title='test1', content=Config.content1, post_time=datetime.datetime.utcnow(), subtitle='test1', )
    a6 = Article(title='test1', content=Config.content1, post_time=datetime.datetime.utcnow(), subtitle='test1', )
    a7 = Article(title='test1', content=Config.content1, post_time=datetime.datetime.utcnow(), subtitle='test1', )
    a8 = Article(title='test1', content=Config.content1, post_time=datetime.datetime.utcnow(), subtitle='test1', )
    a9 = Article(title='test1', content=Config.content1, post_time=datetime.datetime.utcnow(), subtitle='test1', )
    a10 = Article(title='test1', content=Config.content1, post_time=datetime.datetime.utcnow(), subtitle='test1', )
    a11 = Article(title='test1', content=Config.content1, post_time=datetime.datetime.utcnow(), subtitle='test1', )
    a12 = Article(title='test1', content=Config.content1, post_time=datetime.datetime.utcnow(), subtitle='test1', )
    a13 = Article(title='test1', content=Config.content1, post_time=datetime.datetime.utcnow(), subtitle='test1', )
    a14 = Article(title='test1', content=Config.content1, post_time=datetime.datetime.utcnow(), subtitle='test1', )
    t1 = Tag(name='tag1', )
    t2 = Tag(name='tag2', )
    c1 = Category(name='category1')
    c2 = Category(name='category2')
    p1 = Password(password='123', password_hash=generate_password_hash('123'))
    a1.category = c1
    a2.category = c1
    a3.category = c2
    a5.category = c1
    a1.tags.append(t1)
    a2.tags.append(t2)
    a3.tags.append(t1)
    a3.tags.append(t2)
    db.session.add_all([a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, p1, c1, c2, t1, t2])
    for a in Article.query.all():
        a.year = a.post_time.year
        a.month = a.post_time.month
    db.session.commit()


# @blog.shell_context_processor
# def make_shell_context():
#     return dict(db=db, Tag=Tag, Article=Article, Category=Category,
#                 Password=Password)