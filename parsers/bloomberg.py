from logger import LOG
import settings
from base_parser import BaseParser 
from lxml import etree
import datetime
#import xml.etree.ElementTree as ElementTree

#imv_

class bloomberg(BaseParser):

	def __init__(self):
		pass

	def fill_conversations(self):	
		tree = etree.parse(self.file_path)
		for communication_node in tree.iterfind('./Message'):
			Sender_UserInfo_node = communication_node.find('./Sender/UserInfo')
			from_name, from_emails = get_name_emails(Sender_UserInfo_node)
			
			to = []
			for Recipient_UserInfo_node in communication_node.iterfind('./Recipient/UserInfo'):
				to_name, to_emails = get_name_emails(Recipient_UserInfo_node)
				to.append(
					{
						'name' : to_name,
						'email': to_emails,
					}
				)
			
			message_parts = []
			n = communication_node.find('./Subject')
			if n is not None and n.text:
				message_parts.append(n.text)
			n = communication_node.find('./MsgBody')
			if n is not None and n.text:
				message_parts.append(n.text)
			n = communication_node.find('./Greeting')
			if n is not None and n.text:
				message_parts.append(n.text)
			message = '\r\n\r\n'.join(message_parts)
			
			message_time = get_datetime_from_unix_string(communication_node.find('./MsgTimeUTC').text)
			
			communication = self.create_communication(
				from_ = {
					'name' : from_name,
					'email': from_emails,
				},
				to = to,
				message = message,
				message_time = message_time
			)
			
			conversation = []
			conversation.append(communication)
			self.conversations.append(conversation)				

def get_name_emails(
	UserInfo_node,
):
	name_parts = []
	n = UserInfo_node.find('./FirstName')	
	if n is not None and n.text:
		name_parts.append(n.text)
	n = UserInfo_node.find('./LastName')
	if n is not None and n.text:
		name_parts.append(n.text)
	name = ' '.join(name_parts)
	
	emails = []
	for node in UserInfo_node.iterfind('./'):
		if node.tag.find('Email') >= 0 and node.text:
			emails.append(node.text)
			
	if len(name) < 1:
		name = emails[0]
	
	return name, emails
			
def get_datetime_from_unix_string(
	unix_string
):
	try:
		return datetime.datetime.utcfromtimestamp(float(unix_string))
	except:
		LOG.error('unix_string=' + unix_string)
		#LOG.exception(sys.exc_info()[0])
		raise
		return unix_string	