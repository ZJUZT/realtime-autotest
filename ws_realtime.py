import websocket
import json
import threading
import logging

__author__ = 'Jason-Zhang'
'''
establish websocket connection with realtime server
'''

logger = logging.getLogger("websocket")
realtime_server_uri = "ws://121.40.237.99:9999/websocket"


class WsRealTime(threading.Thread):
	ws = None

	def __init__(self, token, email):
		threading.Thread.__init__(self, name=email)
		self.token = token
		login_info = {
			"action": "login",
			"action_info": {
				"auth_token": self.token
			},
		}

		logout_info = {
			"action": "logout"
		}

		def on_message(ws, message):
			logger.info(message.decode('utf-8').encode('gbk'))

		def on_error(ws, error):
			logger.error(error.decode('utf-8').encode('gbk'))

		def on_close(ws):
			ws.send(json.dumps(logout_info))
			logger.info("websocket connection closed")

		websocket.enableTrace(False)
		self.ws = websocket.WebSocketApp(
			realtime_server_uri,
			on_message=on_message,
			on_error=on_error,
			on_close=on_close)

		def on_open(ws_):
			ws_.on_open = ws_.send(json.dumps(login_info))

		self.ws.on_open = on_open

	def run(self):
		self.ws.run_forever()

	def stop(self):
		self.ws.close()
