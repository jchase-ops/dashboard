import os
from flask import Flask
from .config import *
from sqlalchemy.sql import text
from .db import *
from .models import *

def create_app(test_config=None):
    app = Flask(__name__)
    
    if test_config is None:
        app.config.from_object(DevelopmentConfig)
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    else:
        app.config.from_mapping(test_config)

    url = app.config.get('SQLALCHEMY_DATABASE_URL')
    if url.startswith('sqlite') and 'instance' in url:
        app.config['SQLALCHEMY_DATABASE_URL'] = url.replace('instance', app.instance_path)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    @app.route('/testdb')
    def test_db():
        try:
            db.query(text('1')).from_statement(text('SELECT 1')).all()
            return '<h1>It works.</h1>'
        except Exception as e:
            error_text = "<p>The error:<br>" + str(e) + "</p>"
            hed = '<h1>Something is broken.</h1>'
            return hed + error_text
        
    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    from . import calendar
    app.register_blueprint(calendar.bp)
        
    return app
