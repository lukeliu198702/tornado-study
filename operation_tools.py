__author__ = 'luke'
'''
运维工具网站
'''
import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

from tornado.options import parse_command_line
from tornado.web import *

import psycopg2
import momoko

define("port", default=8888, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class ApplyDomainPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('domain.html')

class DomainPageHandler(tornado.web.RequestHandler):
    def post(self):
        RootDomain = self.get_argument('RootDomain')
        HostRecord = self.get_argument('HostRecord')
        RecordType = self.get_argument('RecordType')
        IP = self.get_argument('IP')
        self.render('ApplyDomainResult.html', RootDomain=RootDomain, HostRecord=HostRecord, RecordType=RecordType,
                    IP=IP)

class BaseHandler(RequestHandler):
    @property
    def db(self):
        return self.application.db

class IPHandler(BaseHandler):
    @asynchronous
    def get(self):
        query_string='SELECT "LookUp"."Description","LookUp"."Id" FROM public."LookUp";'
        self.db.execute(query_string,callback=self._done)
        #self.write('Some text here!')
        #self.finish()
    def _done(self,cursor,error):
        self.write('Results: %r'%(cursor.fetchall(),))
        self.finish()
class PhysicalServerHandler(BaseHandler):
    @asynchronous
    def get(self, *args, **kwargs):
        query_string='''
        select distinct "PhysicalServeer"."Code" as "计算机名","PhysicalServeer"."Description" as "其他ip","PhysicalServeer"."IntranetIP" as "内网ip","PhysicalServeer"."ExtranetIP" as "公网ip",
"PhysicalServeer"."Hdinfo" as "硬盘总大小","Map_Server_ProductUse"."IdClass2" as "所属产品","ServerUse"."Description" as "服务器描述","ServerUse"."Owner" as "负责人"
from "PhysicalServeer"
inner join "Map_Server_ProductUse"
on "PhysicalServeer"."Id"="Map_Server_ProductUse"."IdObj1" and "PhysicalServeer"."Status"='A' and "Map_Server_ProductUse"."Status"='A'
inner join "ServerUse"
on "ServerUse"."Id"="Map_Server_ProductUse"."IdObj2"
order by "Map_Server_ProductUse"."IdClass2"
'''
        self.db.execute(query_string,callback=self._done)

    def _done(self,cursor,error):
        self.write('Results: %r'%(cursor.fetchall(),))

        self.finish()

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
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler),
                  (r'/domain', ApplyDomainPageHandler),
                  (r'/applydomainresult',DomainPageHandler),
                  (r'/ip',IPHandler),
                  (r'/pys',PhysicalServerHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "pages")
    )
    app.db= momoko.Pool(
        dsn='dbname=cmdbuild user=postgres password=abcd123! '
            'host=10.200.200.201 port=5432',
        size=1
    )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()