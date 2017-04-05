from logger import LOG
import settings
from base_parser import BaseParser 
from lxml import etree
import datetime
#import xml.etree.ElementTree as ElementTree

#imv_

class reuters(BaseParser):

	def __init__(self):
		pass

	def fill_conversations(self):
		try:
			tree = etree.parse(self.file_path)
		except:
			with open(self.file_path) as f:
				xml = f.read()
			xml = '<root>' + xml + '</root>'
			#print '|' + xml + '|'
			tree = etree.fromstring(xml)
	
		names2dates2conversation = {}
		for communication_node in tree.iterfind('./Message'):
			from_name = communication_node.find('./User').text
			message_time = get_datetime_from_string(communication_node.find('./UTCTime').text)
			communication = self.create_communication(
				from_ = {
					'name' : from_name,
					#'email': None,
				},
				to = [],
				message = communication_node.find('./Content').text,
				message_time = message_time
			)
			
			if from_name in names2dates2conversation:
				dates2conversation = names2dates2conversation[from_name]
			else:
				dates2conversation = {}
				names2dates2conversation[from_name] = dates2conversation
							
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
		return datetime.datetime.strptime(string, '%Y-%m-%dT%H:%M:%S.%fZ')
	except:
		LOG.error('string=' + string)
		#LOG.exception(sys.exc_info()[0])
		raise
		return string	
	