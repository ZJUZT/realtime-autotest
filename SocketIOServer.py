import json
import threading
import logging
from socketIO_client import SocketIO, LoggingNamespace

__author__ = 'Jason-Zhang'
'''
establish websocket connection with realtime server
'''

logger = logging.getLogger("websocket")
# realtime_server_uri = "ws://121.40.237.99:9999/websocket"
socketio_host = "http://121.40.237.99"
socketio_port = 8080


class SocketIOServer(threading.Thread):
	def __init__(self, token, email):
		threading.Thread.__init__(self, name=email)
		self.token = token
		self.login_info = {
			"action": "login",
			"action_info": {
				"auth_token": self.token
			},
		}

		self.logout_info = {
			"action": "logout"
		}
		self.socketIO = SocketIO(socketio_host, socketio_port)

	def on_realtime(*args):
		logger.debug(args[1])

	def run(self):
		self.socketIO.emit('realtime', json.dumps(self.login_info))
		self.socketIO.on('realtime', self.on_realtime)
		self.socketIO.wait()

