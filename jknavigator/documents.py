from base64 import b64decode, b64encode
from mongoengine import * 
from flask.ext.mail import Message
import datetime

class Site(Document):
    author_email = EmailField()
    author_full_name = StringField()
    
    date_submitted = DateTimeField(default=datetime.datetime.now)

    site = StringField()
    opts = DictField()


