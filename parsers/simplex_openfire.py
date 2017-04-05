from logger import LOG
import settings
from base_parser import BaseParser 
from lxml import etree
import datetime
#import xml.etree.ElementTree as ElementTree

#imv_

class simplex_openfire(BaseParser):

	def __init__(self):
		pass

	def fill_conversations(self):	
		tree = etree.parse(self.file_path)
		conversation_ids2communications = {}
		for communication_node in tree.iterfind('./database/table_data/row'):
			communication_node.find('./field[@name="toJID"]').text
			communication = self.create_communication(
				from_ = {
					'name' : communication_node.find('./field[@name="fromJID"]').text,
				},
				to = [
					{				
						'name' : communication_node.find('./field[@name="toJID"]').text,
					}
				],
				message = communication_node.find('./field[@name="body"]').text,
				message_time = get_datetime_from_unix_string(communication_node.find('./field[@name="sentDate"]').text)
			)
			try:			
				communications = conversation_ids2communications[communication_node.find('./field[@name="conversationID"]').text]
			except:
				communications = []
				conversation_ids2communications[communication_node.find('./field[@name="conversationID"]').text] = communications
			communications.append(communication)
		self.conversations = conversation_ids2communications.values()

def get_datetime_from_unix_string(
	unix_string
):
	unix_string = unix_string[:10] + '.' + unix_string[10:]
	try:
		return datetime.datetime.utcfromtimestamp(float(unix_string))
	except:
		LOG.error('unix_string=' + unix_string)
		#LOG.exception(sys.exc_info()[0])
		raise
		return unix_string	
