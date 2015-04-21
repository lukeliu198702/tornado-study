__author__ = 'luke'
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import parse_command_line
from tornado.web import *

import psycopg2
import momoko


class BaseHandler(RequestHandler):
    @property
    def db(self):
        return self.application.db


class TutorialHandler(BaseHandler):
    @asynchronous
    def get(self):
        query_string='SELECT "LookUp"."Description","LookUp"."Id" FROM public."LookUp";'
        self.db.execute(query_string,callback=self._done)
        #self.write('Some text here!')
        #self.finish()
    def _done(self,cursor,error):
        self.write('Results: %r'%(cursor.fetchall(),))
        self.finish()

if __name__ == '__main__':
    parse_command_line()
    application = Application([
        (r'/', TutorialHandler)
    ], debug=True)

    application.db = momoko.Pool(
        dsn='dbname=cmdbuild user=postgres password=000000 '
            'host=10.200.200.233 port=5432',
        size=1
    )

    http_server = HTTPServer(application)
    http_server.listen(8888, 'localhost')
    IOLoop.instance().start()
