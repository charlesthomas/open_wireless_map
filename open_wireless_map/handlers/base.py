from bcrypt import hashpw
from bson.json_util import loads
from tornado.web import RequestHandler

class BaseHandler(RequestHandler):
    def get_current_user(self):
        if not self.request.uri.startswith('/api/'):
            return True
        payload = loads(self.request.body)
        token = payload.get('token', None)
        if token is None or token == '':
            return False
        stored_hash = self.settings['api_password_hash']
        if hashpw(token, stored_hash) != stored_hash:
            return False
        return True

    def make_point(self, latitude, longitude):
        latitude = float(latitude)
        longitude = float(longitude)
        return dict(type='Point', coordinates=[longitude, latitude])
    
    def make_geo_query(self, north, south, east, west):
        north = float(north)
        south = float(south)
        east = float(east)
        west = float(west)

        return  {'$geoWithin':
                    {'$geometry':
                        {'type': 'Polygon',
                         'coordinates': [[[west, south],
                                          [west, north],
                                          [east, north],
                                          [east, south],
                                          [west, south]]]}}}
