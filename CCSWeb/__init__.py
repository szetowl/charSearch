from flask import Flask

def create_web ():
    app=Flask(__name__)
    app.config['SECRET_KEY']='szeto'

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    return app