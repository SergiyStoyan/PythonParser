from logger import LOG
import settings
from base_parser import BaseParser 
from lxml import etree
import datetime

#imv_

class noble_icechat(BaseParser):

	def __init__(self):
		pass

	def fill_conversations(self):	
		tree = etree.parse(self.file_path)
		for conversation_node in tree.iterfind('./Conversation'):			
			self.conversations.append(self.__get_communications_from_conversation_node(conversation_node))
			#LOG.debug(conversation_node)

	def __get_communications_from_conversation_node(self,
		conversation_node
	):		
		communications = []
		participants = {}
		for participantEntered_node in conversation_node.findall('./ParticipantEntered'):
			participant = {
				'name': participantEntered_node.find('./LoginName').text,
				'login_time': datetime.datetime.utcfromtimestamp(float(participantEntered_node.find('./DateTimeUTC').text)),
			}
			participants[participant['name']] = participant
		for participantLeft_node in conversation_node.findall('./ParticipantLeft'):
			try:
				participants[participantLeft_node.find('./LoginName').text]['logout_time'] = datetime.datetime.utcfromtimestamp(float(participantLeft_node.find('./DateTimeUTC').text))
			except:
				LOG.exception(sys.exc_info()[0])
				#LOG.info(participants)
				#LOG.info(stringify_children(conversation_node))				
				raise
		for message_node in conversation_node.findall('./Message'):	
			message_time = get_datetime_from_unix_string(message_node.find('./DateTimeUTC').text)
			name = message_node.find('./LoginName').text
			tos = []
			for participant_name in participants:
				try:
					if participant_name != name and participants[participant_name]['login_time'] <= message_time and participants[participant_name]['logout_time'] >= message_time:
						tos.append(
							{
								'name': participant_name
							}
						)
				except:
					LOG.exception(participant_name)
					#LOG.info(participants)
					#LOG.info(tos)
					raise
			communication = self.create_communication(
				from_ = {
					'name' : name,
				},
				to = tos,
				message = message_node.find('./Content').text,
				message_time = message_time,		
			)			
			communications.append(communication)
			#LOG.debug(communication)
		return communications

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
			
def stringify_children(node):
	from lxml.etree import tostring
	from itertools import chain
	parts = ([node.text]
		+ list(chain(*([tostring(c, with_tail=False), c.tail] for c in node.getchildren())))
		+ [node.tail]
	)
	# filter removes possible Nones in texts and tails
	return ''.join(filter(None, parts))
