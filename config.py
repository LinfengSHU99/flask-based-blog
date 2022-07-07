base_url = ''
import markdown

class Config:
    with open('Devlog.md', 'r') as fp:
        content1 = fp.read()
    content1 = markdown.markdown(content1)
    content1 = '<mytag>' + content1
    content1 = content1 + '</mytag>'
    content2 = '<mytag>Flask-SQLAlchemy provides a base class for models as\
well as a set of helper classes and functions that are used</mytag>'
