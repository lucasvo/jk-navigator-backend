from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
from flask.ext.mongorest import methods
from flask.ext.mongorest.views import ResourceView, render_json
import mimerender

ORIGIN = []

def crossdomain(origin=ORIGIN, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
# The following is not used:
    #if headers is not None and not isinstance(headers, basestring):
    #    headers = ', '.join(x.upper() for x in headers)
    if isinstance(origin, basestring):
        origin = [origin]
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            print 'AAA'
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            if 'origin' in request.headers:
                print 'b'
                print request
                requestedOrigin = request.headers['origin']
                if True: # Disabled
                    # Origin whitelisted, show CORS headers. 
                    h = resp.headers

                    h['Access-Control-Allow-Origin'] = '*' 
                    h['Access-Control-Allow-Methods'] = get_methods()
                    h['Access-Control-Max-Age'] = str(max_age)
                    if 'Access-Control-Request-Headers' in request.headers:
                        h['Access-Control-Allow-Headers'] = request.headers['Access-Control-Request-Headers']

            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator
   
class Options:
    method = 'OPTIONS'

mimerender = mimerender.FlaskMimeRender()
class CrossDomainResourceView(ResourceView):
    hosts = ORIGIN
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List, methods.Delete, Options] 

    
    @crossdomain(hosts)
    def dispatch_request(self, *args, **kwargs):
        return super(CrossDomainResourceView, self).dispatch_request(*args, **kwargs)

