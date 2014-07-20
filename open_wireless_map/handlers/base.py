from tornado.web import RequestHandler

class BaseHandler(RequestHandler):

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
