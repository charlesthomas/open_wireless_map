from add import AddHandler
from index import IndexHandler
from list import ListHandler

url_map = []

url_map.append(('/', IndexHandler))
url_map.append((r'/add/?', AddHandler))
url_map.append((r'/api/add/?', AddHandler))
url_map.append((r'/api/list/?', ListHandler))
