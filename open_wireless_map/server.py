#!/usr/bin/env python
from os import path
from sys import argv

from motor import MotorClient
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_config_file
from tornado.web import Application

from handlers import url_map

def get_mongo(db_name, host, port, user=None, password=None):
    if user is not None and password is not None:
        connection_string = 'mongodb://{user}:{password}@{host}:{port}'.format(
            user=user, password=password, host=host, port=port
        )
    else:
        connection_string = 'mongodb://{host}:{port}'.format(
            host=host, port=port
        )
    return MotorClient(connection_string)[db_name]

def make_server(config_path):
    root = path.dirname(__file__)
    static_path = path.join(root, 'static')
    template_path = path.join(root, 'template')

    define('port', default=7777, type=int)
    define('production', default=False, type=bool)
    define('mongo_db_name', default='open_wireless_map', type=str)
    define('mongo_host', default='localhost', type=str)
    define('mongo_port', default=27017, type=int)
    define('mongo_user', default=None, type=str)
    define('mongo_password', default=None, type=str)
    define('api_password_hash', default=None, type=str)

    parse_config_file(config_path)

    app_config = dict(static_path=static_path,
                      template_path=template_path)
    if not options.production:
        app_config.update(debug=True)

    server = Application(url_map, **app_config)
    server.settings['api_password_hash'] = options.api_password_hash
    server.settings['mongo'] = get_mongo(db_name=options.mongo_db_name,
                                         host=options.mongo_host,
                                         port=options.mongo_port,
                                         user=options.mongo_user,
                                         password=options.mongo_password)
    return server

def main(config_path='/etc/open_wireless_map.conf'):
    server = make_server(config_path)
    server.listen(options.port, 'localhost')
    IOLoop.instance().start()

if __name__ == '__main__':
    if len(argv) == 1:
        main()
    else:
        main(argv[1])
