from flask.ext.mongorest.views import ResourceView
from flask.ext.mongorest.resources import Resource
from flask.ext.mongorest import operators as ops
from flask.ext.mongorest import methods
from flask.ext.mongorest.authentication import AuthenticationBase
from jknavigator.main import app, api
from flask import session
from jknavigator.documents import Site
from jknavigator.crossdomain import CrossDomainResourceView, Options

class SiteResource(Resource):
    document = Site
    fields = ['author_full_name', 'site', 'opts']

class UserResourceAuthentication(AuthenticationBase):
    def authorized(self):
        # TODO: Find out if resource == current_user
        return current_user.is_authenticated()
 
@api.register(name='sites', url='/site/')
class SiteResourceView(CrossDomainResourceView):
    resource = SiteResource
#    authentication_methods = [UserResourceAuthentication]
    methods = [methods.Create, methods.Update, methods.List, methods.Fetch, methods.Delete, Options]

