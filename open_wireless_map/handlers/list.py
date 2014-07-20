from bson.json_util import dumps
from tornado.gen import coroutine

from base import BaseHandler

class ListHandler(BaseHandler):
    @coroutine
    def get(self):
        data = []
        north = float(self.get_argument('north'))
        south = float(self.get_argument('south'))
        east = float(self.get_argument('east'))
        west = float(self.get_argument('west'))
        criteria = dict(location=self.make_geo_query(north=north, south=south,
                                                     east=east, west=west))
        cursor = self.settings['mongo'].locations.find(criteria)
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            data.append(doc)
        self.write(dumps(data))
