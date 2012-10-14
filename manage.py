#!/usr/bin/env python

import os
import sys
import datetime
from flask.ext.script import Manager, Server, Command
from jknavigator.main import setup_app

app = setup_app()
manager = Manager(app)

server = Server(host="0.0.0.0", port=5002, use_debugger=app.debug)
manager.add_command('runserver', server)

# Add Flask-Assets/webassets management comments
from flask.ext.assets import ManageAssets
manager.add_command('assets', ManageAssets(app.assets))


#@manager.command
#def createuser():
#    from closeio.app.documents import User
#    from getpass import getpass
#    email = raw_input('Email: ')
#    password = getpass('Password: ')
#    user = User(email=email)
#    user.first_name = raw_input('First Name: ')
#    user.last_name = raw_input('Last Name: ')
#    user.set_password(password)
#    user.save()

@manager.command
def mongo():
    os.system('mongo %s' % app.config['MONGODB_SETTINGS']['DB'])

@manager.command
def routes():
    print app.url_map

@manager.command
def runasync():
    os.system('gunicorn -c config/gunicorn/local.py sendtask.gunicorn:app')


class DnsLookup(Command):
    capture_all_args = True
    def run(self, args):
        from sendtask.jobs.dnslookup import LookupTask
        for arg in args:
            LookupTask.delay(arg)

manager.add_command('lookup', DnsLookup())


class Celery(Command):
    capture_all_args = True

    def run(self, args):
        app.celery.start(['celery']+args)

manager.add_command('celery', Celery())


if __name__ == "__main__":
    manager.run()
