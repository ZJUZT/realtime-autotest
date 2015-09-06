import json
import ws_realtime
import threading
import logging
import logging.config
import resource
import time
import requests

__author__ = 'Jason-Zhang'
'''
Auto test for real-time server
User class defines the basic action
including:
create a share link for a file/folder
send a share link to user(s)/group(s)
invite user(s)/group(s) to collaborate with folder(s)
make comments for a file (@ specific user(s))
send review invitation to user(s)
make review comments under a review (@ specific user(s))
invite user(s) to join a group
'''

logging.config.fileConfig("logger.config")
logger = logging.getLogger("user")


class User(threading.Thread):
	def __init__(self, email, password, remember_login, file_num, folder_num, group_num, action_list=None):
		threading.Thread.__init__(self, name=email)
		self.email = email
		self.password = password
		self.remember_login = remember_login
		self.action_list = action_list
		self.file = []
		self.folder = []
		self.group = []
		self.review = []

		self.test_folder = None
		self.realtime_token = None
		self.request_token = None
		self.file_num = file_num
		self.folder_num = folder_num
		self.group_num = group_num
		self.review_num = self.file_num
		self.session = requests.Session()
		self.user_id = None

	# log user in
	def login(self):
		params = {
			'email': self.email,
			'password': self.password,
			'remember_login': self.remember_login
		}
		session = self.session
		response = session.put(resource.protocol + resource.host + resource.login_uri, json.dumps(params))
		if response.json()["success"] is True:
			self.user_id = response.json()["user"]['id']
			logger.info("login success")
		else:
			logger.error("login fail")
			raise Exception
		# get realtime token
		if 'realtime_token' in response.cookies.keys() and 'csrf_cookie_name' in response.cookies.keys():
			self.realtime_token = response.cookies['realtime_token']
			self.request_token = response.cookies['csrf_cookie_name']
		else:
			logger.error("login realtime server fail")
			raise Exception
		ws_thread = ws_realtime.WsRealTime(self.realtime_token, email=self.email)
		ws_thread.setDaemon(True)
		ws_thread.start()

	def do_action(self, action, method):
		action_uri_map = resource.action_uri_map
		uri = action_uri_map[action["type"]]
		params = action["params"]
		session = self.session
		if method == resource.PUT:
			response = session.put(url=resource.protocol + resource.host + uri, data=json.dumps(params))
		elif method == resource.POST:
			headers = {
				'requesttoken': self.request_token
			}
			response = session.post(url=resource.protocol + resource.host + uri, data=params, headers=headers)
		else:
			response = session.get(url=resource.protocol + resource.host + uri, params=params)

		response = response.json()
		if 'success' in response.keys() and response['success'] is True:
			logger.info(action["type"] + " success")
			return response
		else:
			raise Exception

	def logout(self):
		self.session.close()
		logger.info("logout success")
		# wait for websocket thread to handle all the notifications
		time.sleep(2)

	def create_group(self, number):
		for i in range(1, number + 1):
			action = {
				"type": resource.CREATE_GROUP,
				"params": {
					"added_user_ids": [self.user_id],
					"name": "%s%d" % ('real_time', i),
					"description": "test_for_realtime",
					"collab_auto_accepted": True,
					"visiable": True,
				}
			}
			response = self.do_action(action, resource.PUT)
			if 'success' in response.keys() and response['success'] is True:
				self.group.append(response['group']['id'])
			else:
				raise Exception

	def create_item(self, item_type, number):
		for i in range(1, number + 1):
			action = {
				"type": item_type,
				"params": {
					"name": "%s" % i,
					"parent_folder_id": self.test_folder
				}
			}
			if item_type == resource.CREATE_FILE:
				action["params"]["type"] = 1
			response = self.do_action(action, resource.PUT)
			if 'success' in response.keys() and response['success'] is True:
				if item_type == resource.CREATE_FILE:
					self.file.append(response["new_file"]["id"])
				elif item_type == resource.CREATE_FOLDER:
					self.folder.append(response["new_folder"]["id"])
				time.sleep(0.1)
			else:
				raise Exception

	def delete_item(self):
		action = {
			"type": resource.DELETE_item,
			"params": {
				"item_typed_ids[]": "%s%d" % ("folder_", self.test_folder)
			}
		}
		res = self.do_action(action, resource.POST)

	def delete_group(self):

		for group in self.group:
			action = {
				"type": resource.DELETE_GROUP,
				"params": {
					"group_id": group
				}
			}
			self.do_action(action, resource.PUT)

	def do_action_list(self):
		for action in self.action_list:
			action_type = action['type']
			if action['target'] == resource.FOLDER:
				for item in self.folder:
					action["params"][resource.action_attribute_map[action_type]] = resource.generate_value[action_type](
						resource.FOLDER, item)
					self.do_action(action, action['method'])
			elif action['target'] == resource.FILE:
				for item in self.file:
					action["params"][resource.action_attribute_map[action_type]] = resource.generate_value[action_type](
						resource.FILE, item)
					self.do_action(action, action['method'])
			elif action['target'] == resource.GROUP:
				action['admin_user_id'] = self.user_id
				for group in self.group:
					action["params"][resource.action_attribute_map[action_type]] = resource.generate_value[action_type](
						resource.GROUP, group)
					self.do_action(action, action['method'])

	def run(self):
		try:
			self.login()
		except Exception, e:
			logger.error("login fail")
			exit(1)
		if self.action_list is None:
			return
		try:
			# create a test folder at root directory
			action = {
				"type": resource.CREATE_FOLDER,
				"params": {
					"name": "test",
					"parent_folder_id": "own"
				}
			}
			res = self.do_action(action, resource.PUT)

			# get test folder id
			self.test_folder = res['new_folder']['id']
			self.create_item(resource.CREATE_FILE, self.file_num)
			self.create_item(resource.CREATE_FOLDER, self.folder_num)
			self.create_group(self.group_num)
			self.folder.append(self.test_folder)
			self.do_action_list()
			# logout
			self.logout()

		except Exception, e:
			logger.error(e)
		finally:
			# delete all the file created for test anyway
			try:
				self.delete_item()
				self.delete_group()
			except Exception, e:
				logger.error("Can't delete resource created for test")
			finally:
				exit(1)
