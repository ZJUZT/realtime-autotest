__author__ = 'Jason-Zhang'
'''
defines basic uri and other resources
'''
protocol = "http://"
host = "zhangteng.yifangyun.com"

# action target
FILE = "file"
FOLDER = "folder"
REVIEW = "review"
GROUP = "group"
# login uri
LOGIN = "login"
login_uri = "/auth/login"
# logout
LOGOUT = "logout"
logout_uri = "/auth/logout"
# 1.share
# create share link
CREATE_SHARE_LINK = "create_share_link"
create_share_link__uri = "/apps/files/share"
# send share link
SEND_SHARE_LINK = "send_share_link"
send_share_link_uri = "/apps/files/send_share_link"

# 2.collabs
# collabs
COLLABS = "collabs"
collabs_uri = "/apps/collabs/invite"

# 3. group
# create_group_uri
CREATE_GROUP = "create_group"
create_group_uri = "/groups/create"
# group_invitation_uri
GROUP_INVITATION = "group_invitation"
group_invitation_uri = "/groups/edit_users"

# delete_group
DELETE_GROUP = "delete_group"
delete_group_uri = "/groups/delete"

# 4. comments
COMMENTS = "comments"
comments_uri = "/apps/comments/create"

# 5. review
# invitation
REVIEW_INVITATION = "review_invitation"
review_invitation_uri = "/apps/files/review"
# review comments
REVIEW_COMMENTS = "review_comments"
review_comments_uri = "/apps/review_comments/create"
# get review list
REVIEW_LIST = "/apps/messages/get_list"

# file list
file_list_uri = "/apps/files/file_list"

# create folder
CREATE_FOLDER = "create_folder"
create_folder_uri = "/apps/files/new_folder"

# create file
CREATE_FILE = "create_file"
create_file_uri = "/apps/files/new_file"

# delete folder
DELETE_item = "delete_item"
delete_item_uri = "/apps/files/delete"

action_uri_map = {
	LOGIN: login_uri,
	LOGOUT: logout_uri,
	CREATE_SHARE_LINK: create_share_link__uri,
	SEND_SHARE_LINK: send_share_link_uri,
	COLLABS: collabs_uri,
	CREATE_GROUP: create_group_uri,
	GROUP_INVITATION: group_invitation_uri,
	COMMENTS: comments_uri,
	REVIEW_INVITATION: review_invitation_uri,
	REVIEW_COMMENTS: review_comments_uri,
	CREATE_FOLDER: create_folder_uri,
	CREATE_FILE: create_file_uri,
	DELETE_item: delete_item_uri,
	DELETE_GROUP: delete_group_uri
}

action_attribute_map = {
	SEND_SHARE_LINK: "item_typed_id",
	CREATE_SHARE_LINK: "item_typed_id",
	COMMENTS: "item_typed_id",
	COLLABS: "folder_id",
	REVIEW_INVITATION: "items",
	GROUP_INVITATION: "group_id"
}

PUT = "PUT"
POST = "POST"
GET = "GET"

generate_value = {
	SEND_SHARE_LINK: lambda item_type, item: "%s%s%d" % (item_type, "_", item),
	CREATE_SHARE_LINK: lambda item_type, item: "%s%s%d" % (item_type, "_", item),
	COLLABS: lambda item_type, item: item,
	COMMENTS: lambda item_type, item: "%s%s%d" % (item_type, "_", item),
	REVIEW_INVITATION: lambda item_type, item: ["%s%d" % ("file_", item)],
	GROUP_INVITATION: lambda item_type, item: item
}
