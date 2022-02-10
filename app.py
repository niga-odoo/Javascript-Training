from itertools import product
import os
from re import template
import re
from sqlite3 import adapters
from urllib import request, response
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.routing import Map, Rule
from werkzeug.utils import redirect
from werkzeug.wrappers import Request, Response
from jinja2 import Environment, FileSystemLoader
from redis import StrictRedis


class Product_App:
    def __init__(self):
        template_path = os.path.join(os.path.dirname(__file__), 'templates')
        self.jinja_env = Environment(loader=FileSystemLoader(template_path), autoescape=True)

        self.url_map = Map([
            Rule('/', endpoint='index'),
            Rule('/products', endpoint='products'),
            Rule('/product_info', endpoint='product_info'),
        ])

    def dispatch_request(self, req):
        # return Response('Hello World!!')
        # return self.render_template('index.html')
        adapter = self.url_map.bind_to_environ(req.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self,endpoint)(req, **values)
        except HTTPException as e:
            return e
    def index(self, req):
        return self.render_template('index.html')

    def products(self,req):
        return self.render_template('products.html')
    
    def product_info(self,req):
        return self.render_template('product_info.html')

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def render_template(self, template_name, **context):
        template = self.jinja_env.get_template(template_name)
        return Response(template.render(context), mimetype='text/html')

def create_App():
    app = Product_App()
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/static' : os.path.join(os.path.dirname(__file__), 'static')
    })
    return app


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app = create_App()
    run_simple('127.0.0.1', 5003, app, use_debugger=True, use_reloader=True)
