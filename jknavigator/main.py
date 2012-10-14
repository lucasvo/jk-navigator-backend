import os
import re
from flask import Flask, url_for, render_template
import flask.ext.assets
from flask.ext.mongoengine import MongoEngine
from flask.ext.mongorest import MongoRest
from flask.ext.admin import Admin
from flask.ext.mail import Mail, Message
#from flask.ext.sslify import SSLify
from pymongo.uri_parser import parse_uri 

from werkzeug.exceptions import BadRequest
class Application(Flask):
    def __init__(self, *args, **kwargs): 
      if os.environ.get('ST_SETTINGS', None):
          config = os.environ.get('ST_SETTINGS', None)
      else:
          config = kwargs.pop('config', 'jknavigator.config.defaults')

      testing = kwargs.pop('testing', False) 

      super(Application, self).__init__('jknavigator', *args, **kwargs)

      if config != None:
          cf_obj = __import__(config, fromlist=['*'])#[config.rpartition('.')[2]])
          self.config.from_object(cf_obj)
 
      # Set the mongohq url from the heroku plugin
      if os.environ.get('MONGOLAB_URI', False):
          m_uri = os.environ.get('MONGOLAB_URI')
          self.config.MONGODB_SETTINGS = {}
          self.config.MONGODB_SETTINGS['host'] = m_uri
          m_dict = parse_uri(m_uri)
          MONGODB_SETTINGS = {
            'DB':m_dict['database'],
#            'USER':m_dict['username'],
#            'PASSWORD':m_dict['password'],
            'host':m_uri
          }
          self.config.update(MONGODB_SETTINGS=MONGODB_SETTINGS)

      # Overwrite db for testing and prepare some other things
      self.config.TESTING = False
      if testing:
          self.config['MONGODB_SETTINGS']['DB'] = self.config['MONGODB_SETTINGS']['DB']+'_test'
          self.config.TESTING = True


      self.db = MongoEngine(self)


#   def url_for(self, endpoint, **kwargs):
#       return self.config.get('APPLICATION_BASE_URL') + url_for(endpoint, **kwargs)


def setup_app(**kwargs):
    global app, api, admin, assets

    app = Application(**kwargs)
    app.debug = True

    #TODO: Set secret dynamically
    app.secret_key = '29adsnlzh0e20asdf289'

# Flask-Assets
    assets = flask.ext.assets.Environment(app)

    assets.manifest = 'json:.webassets-manifest.json'
    
    if 'STATIC_HOST' in app.config:
        assets.config['url'] = app.config['STATIC_HOST']
    if app.debug:
        assets.cache = False

# TODO: Get rid of this hacked less compiler
#    import sendtask.bootstrap_less

# TOOD add new jquery version
    js_files = [
        'lib/jquery/jquery-1.8.1.min.js',
        'lib/ddslick/jquery.ddslick.min.js', 
        'lib/jquery/jquery.validate.js',
        'js/core.js',
        'lib/retina/retina.js',
        ]

    if app.config.get('LESSC_AVAILABLE', False) and not app.config.TESTING:
        assets.register('all_css', 'style/style.less', filters=['bootstrap_less', 'yui_css'], output='style/style.css')
    else:
         assets.register('all_css', 'style/style_compiled.css', filters=['yui_css'], output='style/style.css')
       
    assets.register('all_js', *js_files, filters=['yui_js'], output='js/all.js') 
    app.assets = assets

# Override the template context {{ url_for }} function.
#    @app.context_processor
#    def override_url_for():
#        return dict(url_for=cdn_url_for)


    # MongoRest
    api = MongoRest(app, url_prefix='/api/v1')

    # Admin
    admin = Admin(app=app, url='/admin')

    # Error emails
#   if not app.debug:
#       import logging
#       #from logging.handlers import SMTPHandler
#
#       mail_handler = SMTPHandler((config['MAIL_SERVER'], config['MAIL_PORT']),
#                                  config['SERVER_EMAIL'],
#                                  config['ADMINS'],
#                                  'Server error',
#                                  (config['MAIL_USERNAME'], config['MAIL_PASSWORD']),
#                                  secure=config['MAIL_USE_TLS'] and ())
#       mail_handler.setLevel(logging.ERROR)
#       app.logger.addHandler(mail_handler)

#       mail_handler.setFormatter(logging.Formatter('''\
#           Message type:       %(levelname)s
#           Location:           %(pathname)s:%(lineno)d
#           Module:             %(module)s
#           Function:           %(funcName)s
#           Time:               %(asctime)s
#
#           Message:
#
#           %(message)s
#       '''))


    from jknavigator import resources
    @app.route('/')
    def homepage():
        context = {}
        return render_template('base.html', **context)



    return app
