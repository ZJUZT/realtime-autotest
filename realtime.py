import resource
import user
import time

__author__ = 'Jason-Zhang'

if __name__ == "__main__":
	# create send share link for each folder
	target_user = [8420, 42]
	user1 = {
		"email": "3131@qq.com",
		"password": "1994zt87",
		"remember_login": 0,
		"folder_created": 0,
		"file_created": 0,
		"group_created": 0
	}

	user2 = {
		"email": "3232@qq.com",
		"password": "1994][Wqy",
		"remember_login": 0,
		"folder_created": 2,
		"file_created": 2,
		"group_created": 1
	}

	action1 = {
		"method": resource.PUT,
		"target": resource.FOLDER,
		"type": resource.CREATE_SHARE_LINK,
		"params": {
			"access": "public",
			"disable_download": "0",
			"due_time": time.strftime("%Y-%m-%d", time.localtime()),
			"password_protected": False,
		}
	}

	# send share link
	action2 = {
		"method": resource.PUT,
		"target": resource.FOLDER,
		"type": resource.SEND_SHARE_LINK,
		"params": {
			"receiver_ids": target_user,
			"group_ids": [],
			"message_description": "123"
		}
	}

	action3 = {
		"method": resource.PUT,
		"target": resource.FILE,
		"type": resource.CREATE_SHARE_LINK,
		"params": {
			"access": "public",
			"disable_download": "0",
			"due_time": time.strftime("%Y-%m-%d", time.localtime()),
			"password_protected": False,
		}
	}

	# send share link
	action4 = {
		"method": resource.PUT,
		"target": resource.FILE,
		"type": resource.SEND_SHARE_LINK,
		"params": {
			"receiver_ids": target_user,
			"group_ids": [],
			"message_description": "123"
		}
	}

	# collabs invitation
	invited_users = ""
	for u in target_user:
		invited_users += "%d:editor;" % u
	action5 = {
		"method": resource.PUT,
		"target": resource.FOLDER,
		"type": resource.COLLABS,
		"params": {
			"invited_users": "8420:editor",
			"invited_groups": "",
			"invitation_message": "123"
		}
	}

	# comments
	content = ""
	for u in target_user:
		content += "@[%d] " % u
	content += "123"

	action6 = {
		"method": resource.POST,
		"target": resource.FILE,
		"type": resource.COMMENTS,
		"params": {
			# "content": "@[8420:zt] 123",
			"content": content
		}
	}

	# review invitation
	action7 = {
		"method": resource.PUT,
		"target": resource.FILE,
		"type": resource.REVIEW_INVITATION,
		"params": {
			"invited_users": target_user,
			"title": "123",
			"description": "1234",
			"due_time": time.strftime("%Y-%m-%d", time.localtime())
		}
	}

	# group invitation
	action8 = {
		"method": resource.PUT,
		"target": resource.GROUP,
		"type": resource.GROUP_INVITATION,
		"params": {
			"added_user_ids": target_user,
			"deleted_user_ids": [],
		}
	}

	# review comment
	action = [
		action1,
		action2,
		action3,
		action4,
		action5,
		action6,
		action7,
		action8
	]

	user1["action"] = None
	user2["action"] = action

	users = [user1, user2]

	for u in users:
		user.User(
			u['email'],
			u['password'],
			u['remember_login'],
			u['folder_created'],
			u['file_created'],
			u['group_created'],
			u['action']
		).start()
