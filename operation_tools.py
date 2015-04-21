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


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler), (r'/domain', ApplyDomainPageHandler),(r'/ApplyDomainResult',DomainPageHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "pages")
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()