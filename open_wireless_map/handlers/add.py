import logging
from pprint import pformat

from bson.json_util import dumps, loads
from tornado.gen import coroutine
from tornado.web import authenticated

from base import BaseHandler

class AddHandler(BaseHandler):
    def get(self):
        self.render('add.html')

    @authenticated
    @coroutine
    def post(self):
        if self.request.uri.startswith('/api/'):
            payload = loads(self.request.body)
            lat = payload['latitude']
            lon = payload['longitude']
        else:
            lat = self.get_argument('latitude')
            lon = self.get_argument('longitude')

        result = yield self.settings['mongo']['locations'].insert(
            dict(location=self.make_point(latitude=lat, longitude=lon))
        )

        if self.request.uri.startswith('/api/'):
            self.write(dumps(dict(status='ok')))
            self.finish()
        else:
            self.redirect('/')
