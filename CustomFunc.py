from flask import current_app
from bs4 import BeautifulSoup
def abstract(content):
    soup = BeautifulSoup(content)
    mytag = soup.mytag
    s = mytag.get_text()
    return s

class custom_func:
    def str(self, x):
        return str(x)

    def zip(self, x):
        return zip(x)


class CustomFunc(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if not hasattr(app, 'extensions'):  # pragma: no cover
            app.extensions = {}
        app.extensions['custom_func'] = custom_func
        app.context_processor(self.context_processor)
    @staticmethod
    def context_processor():
        return {
            'custom_func': current_app.extensions['custom_func']
        }



