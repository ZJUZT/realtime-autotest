import resource
import user

__author__ = 'Jason-Zhang'

if __name__ == "__main__":
	# create send share link for each folder
	action1 = {
		"method": resource.PUT,
		"target": resource.FOLDER,
		"type": resource.CREATE_SHARE_LINK,
		"params": {
			"access": "public",
			"disable_download": "0",
			"due_time": "2015-09-07",
			"password_protected": False,
		}
	}

	# send share link
	action2 = {
		"method": resource.PUT,
		"target": resource.FOLDER,
		"type": resource.SEND_SHARE_LINK,
		"params": {
			"receiver_ids": [8420],
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
			"due_time": "2015-09-07",
			"password_protected": False,
		}
	}

	# send share link
	action4 = {
		"method": resource.PUT,
		"target": resource.FILE,
		"type": resource.SEND_SHARE_LINK,
		"params": {
			"receiver_ids": [8420],
			"group_ids": [],
			"message_description": "123"
		}
	}

	# collabs invitation
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
	action6 = {
		"method": resource.POST,
		"target": resource.FILE,
		"type": resource.COMMENTS,
		"params": {
			"content": "@[8420:zt] 123",
		}
	}

	# review invitation
	action7 = {
		"method": resource.PUT,
		"target": resource.FILE,
		"type": resource.REVIEW_INVITATION,
		"params": {
			"invited_users": [8420],
			"title": "123",
			"description": "1234",
			"due_time": "2015-09-30"
		}
	}

	# group invitation
	action8 = {
		"method": resource.PUT,
		"target": resource.GROUP,
		"type": resource.GROUP_INVITATION,
		"params": {
			"added_user_ids": ["8420"],
			"deleted_user_ids": [],
		}
	}

	# review comment
	actions = [
		action1,
		action2,
		action3,
		action4,
		action5,
		action6,
		action7,
		action8
	]
	zt = user.User("3131@qq.com", "1994zt87", 0, 1, 1, 0)
	wqy = user.User("3232@qq.com", "1994][Wqy", 0, 2, 2, 1, actions)
	zt.start()
	wqy.start()
