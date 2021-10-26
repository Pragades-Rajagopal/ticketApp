from gevent import monkey
from gevent.pywsgi import WSGIServer
from index import app

monkey.patch_all()

http_server = WSGIServer(('localhost', 5000), app)
http_server.serve_forever()

