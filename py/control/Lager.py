import falcon
from wsgiref import simple_server
import threading
import json


class LagerThread(threading.Thread):

    def __init__(self, brumulus):
        threading.Thread.__init__(self)
        super(LagerThread, self).__init__()
        self.brumulus = brumulus

        self.api = falcon.API(middleware=[JSONTranslator()])
        self.api.add_route('/action/{action}', self)
        self.api.add_route('/', Resource())

    def run(self):
        self.httpd = simple_server.make_server('', 8000, self.api)
        self.httpd.serve_forever()

    def stop(self):
        self.httpd.shutdown()

    def on_get(self, req, resp, action):
        try:
            result = self.brumulus.action(action)
            print "sending result", result
            req.context['result'] = result
            # resp.set_header =
            resp.status = falcon.HTTP_200

        except Exception as e:
            print "action failed: ", action, str(e)


class Resource(object):

    def __init__(self):
        self.page = open('www/kiosk.html').read()

    def on_get(self, req, resp):
        resp.body = self.page
        resp.status = falcon.HTTP_200


class JSONTranslator(object):

    def process_request(self, req, resp):
        # req.stream corresponds to the WSGI wsgi.input environ variable,
        # and allows you to read bytes from the request body.
        #
        # See also: PEP 3333
        if req.content_length in (None, 0):
            # Nothing to do
            return

        body = req.stream.read()
        if not body:
            raise falcon.HTTPBadRequest('Empty request body',
                                        'A valid JSON document is required.')

        try:
            req.context['doc'] = json.loads(body.decode('utf-8'))

        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPError(falcon.HTTP_753,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect or not encoded as '
                                   'UTF-8.')

    def process_response(self, req, resp, resource):
        if 'result' not in req.context:
            return

        resp.body = json.dumps({'data': req.context['result']})
