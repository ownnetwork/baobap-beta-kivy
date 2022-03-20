# MIT License -> LISCENCE.mit

from os import path
import json

"""
Delete chat content
"""
class DeleteChatContent(object):
	
	def __init__(self, chat_id: str):

		file_path = f'db/chat/{chat_id}.json'

		path.exists(file_path)
		with open(file_path, 'w+') as f:
			json.dump({}, f)