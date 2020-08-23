import tornado.ioloop
import tornado.httpserver
from tornado.web import RequestHandler, Application, StaticFileHandler
from tornado_http_auth import DigestAuthMixin, BasicAuthMixin, auth_required
import base64
import os

#import web.tracks as ewsxml
import web.db as db
import web.creds as creds
import web.logs as logs
import web.sokol as sokol
DBG = logs.DBG

import web.config as config
cfg = config.read()
server_type = cfg.get('server_type', 'http')
server_syte = cfg.get('server_syte', 'localhost:85')

class BaseHandler(RequestHandler):
    #dbw = db.SQLite3Wrapper()
    def prepare(self):
        #self.get_authenticated_user(check_credentials_func=creds.credentials.get, realm='Protected')
        #print('prep /')
        pass

    def get(self):
        self.write('Hello %s' % 'self._current_user')
        #send_xml(self)

class MainHandler(BaseHandler):
    def get(self):
        print("main")
        self.write('<html><body>main<body/><html/>')

class StartHandler(BaseHandler):
    def get(self):
        self.write('<html><body>start<body/><html/>')

class SoHandler(BaseHandler):
    def get(self):
        self.write('<html><body>SO<body/><html/>')

class DebugHandler(BaseHandler):
    pass

class DbHandler(BaseHandler):
    def sql(self):
        return self.dbw.get_shipments(count, offset)
    def get(self):
        f = self.sql() #self.dbw.fetchall(self.sql())
        s = ''
        for line in f:
            s += str(line) + '<br>'
        self.write(s)

class SoHandler(BaseHandler):
    def initialize(self, func):
        self.func = func
    def get(self):
        funcs = {
            'main':sokol.main,
            'init':sokol.init,
            'iter':sokol.iter,
            'manu':sokol.manu,
            'auto':sokol.auto,
        }
        print(self.func)
        if funcs.get(self.func, None) is None:
            self.write(' unknown function')
        else:
            funcs[self.func](self.write)

def main():
    root = './'
    urls = [
        (r'/', DebugHandler),
        (r'/main', MainHandler),
        (r'/start', StartHandler),
        (r'/so', SoHandler, {'func':'main'}),
        (r'/init', SoHandler, {'func':'init'}),
        (r'/iter', SoHandler, {'func':'iter'}),
        (r'/manu', SoHandler, {'func':'manu'}),
        (r'/auto', SoHandler, {'func':'auto'}),
        (r'/(.*)', StaticFileHandler, {'path':'./'}),
    ]
    def get(self):
        s = '<!DOCTYPE HTML><html><body>'
        s += 'Hello %s, updated! <br>' % '' #  self._current_user
        for url in urls:
            if url[0] != r'/' and url[0] != r"/(.*)":
                s += '<a href="http://' + server_syte + url[0] + '">' + url[0] + '<a/><br>'
        s += '<body/><html/>'
        self.write(s)
    urls[0][1].get = get
    urls.append( (r"/(.*)", StaticFileHandler, {"path": r'.\htm', "default_filename": "index.html"}) )
    app = Application(urls)

    if server_type == 'http':
        app.listen(85)
    else:
        # https works, but testing bad
        http_server = tornado.httpserver.HTTPServer(app, ssl_options={
            "certfile": "../https/cert.pem",
            "keyfile": "../https/private.key",
        })
        http_server.listen(85) 

    print('start server')
    DBG.info('start_server')
    db0 = db.SQLite3Wrapper()
    db0.createTables()
    DBG.debug('tables_created')
    db0.load_credentails(creds.credentials)
    tornado.ioloop.IOLoop.current().start()

