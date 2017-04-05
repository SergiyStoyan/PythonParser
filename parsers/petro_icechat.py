from logger import LOG
import settings
from base_parser import BaseParser 
from lxml import etree
import datetime
#import xml.etree.ElementTree as ElementTree

#imv_

class petro_icechat(BaseParser):

	def __init__(self):
		pass

	def fill_conversations(self):	
		tree = etree.parse(self.file_path)
		side1_names2side2_names2dates2conversation = {}
		for communication_node in tree.iterfind('./messageLogs/message'):
			from_name = communication_node.find('./senderIMID').text
			to_name = communication_node.find('./recipientIMID').text
			message_time = get_datetime_from_string(communication_node.find('./datetime').text)
			communication = self.create_communication(
				from_ = {
					'name' : from_name,
					'email': communication_node.find('./senderEmail').text,
				},
				to = [
					{				
						'name' : to_name,
						'email': communication_node.find('./recipientEmail').text,
					}
				],
				message = communication_node.find('./content').text,
				message_time = message_time
			)
			
			if from_name in side1_names2side2_names2dates2conversation:
				side2_names2dates2conversation = side1_names2side2_names2dates2conversation[from_name]
				if to_name in side2_names2dates2conversation:
					dates2conversation = side2_names2dates2conversation[to_name]
				else:
					dates2conversation = {}
					side2_names2dates2conversation[to_name] = dates2conversation
			else:
				if to_name in side1_names2side2_names2dates2conversation:
					side2_names2dates2conversation = side1_names2side2_names2dates2conversation[to_name]
					if from_name in side2_names2dates2conversation:
						dates2conversation = side2_names2dates2conversation[from_name]
					else:
						dates2conversation = {}
						side2_names2dates2conversation[from_name] = dates2conversation
				else:
					side2_names2dates2conversation = {}
					side1_names2side2_names2dates2conversation[from_name] = side2_names2dates2conversation
					dates2conversation = {}
					side2_names2dates2conversation[to_name] = dates2conversation
							
			message_date = message_time.date()			
			if message_date in dates2conversation:
				conversation = dates2conversation[message_date]
			else:
				conversation = []
				dates2conversation[message_date] = conversation
				self.conversations.append(conversation)
				
			conversation.append(communication)

def get_datetime_from_string(
	string
):
	try:
		#import dateutil
		#return dateutil.parser.parse(string)
		return datetime.datetime.strptime(string, '%Y-%m-%dT%H:%M:%S')
	except:
		LOG.error('string=' + string)
		#LOG.exception(sys.exc_info()[0])
		raise
		return string	
	