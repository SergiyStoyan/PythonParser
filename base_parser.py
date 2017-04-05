from logger import LOG
import settings
import sys
import db 
import datetime
import re

class BaseParser(object):

	def __init__(self):		
		pass
	
	def Parse(self, 
		communication_log,
	):
		try:
			self.communication_log = communication_log
			
			lexicon = db.Lexicon.GetByEnterprise(self.communication_log['enterprise_id'])
			keywords = {}
			for l in lexicon:
				for k in l['keywords']:
					if k and not k.isspace():
						keywords[k.strip()] = 1
			if len(keywords) > 0:
				self.keywords_regex = re.compile('|'.join(keywords.keys()), re.IGNORECASE)
			else:
				self.keywords_regex = re.compile('---', re.IGNORECASE)
				LOG.warning('Lexicon is empty for enterprise_id=' + self.communication_log['enterprise_id'])
			
			db.Conversations.DeleteByCommunicationLogId(self.communication_log['_id'])
			db.Communications.DeleteByCommunicationLogId(self.communication_log['_id'])
						
			self.file_path = db.CommunicationLogs.GetFilePath(communication_log)
			self.conversations = []
			self.fill_conversations()	
			for communications in self.conversations:	
				self.__save_conversation(communications)
			db.CommunicationLogs.SetParsed(communication_log['_id'])
		except:
			LOG.exception(sys.exc_info()[0])
			db.CommunicationLogs.SetParsed(communication_log['_id'], sys.exc_info()[0])
		
	def fill_conversations(self):
		raise NotImplementedError('The method is not implemented!')
	
	#helper	
	def create_communication(self,	
		from_,
		to,
		message,
		message_time,		
	):
		matched_keywords = {}
		for m in self.keywords_regex.finditer(message):
			matched_keywords[m.group(0)] = 1
		return {
			'from': from_,
			'to': to,
			'message': message,
			'message_time': message_time,		
			'matched_keywords': matched_keywords.keys(),
		}	
			
	def __save_conversation(self,
		communications
	):
		LOG.info('conversation: communications: ' + str(len(communications)))
		communication_ids = []
		conversation_participants = {}
		last_message_time = datetime.datetime.min
		conversation_matched_keywords = {}
		for c in communications:
			r = db.Communications.Add(			
				communication_log_id = str(self.communication_log['_id']),
				from_ = c['from'],
				to = c['to'],
				message = c['message'],
				message_time = c['message_time'],
				matched_keywords = c['matched_keywords'],
				source = self.communication_log['source'],
				enterprise_id = self.communication_log['enterprise_id'],
			)
			for k in c['matched_keywords']:
				conversation_matched_keywords[k] = 1
			communication_ids.append(str(r.inserted_id))
			conversation_participants[c['from']['name']] = 1;
			for p in c['to']:
				conversation_participants[p['name']] = 1;
			if last_message_time < c['message_time']:
				last_message_time = c['message_time']
		
		db.Conversations.Add(
			communication_log_id = str(self.communication_log['_id']),
			communication_ids = communication_ids,
			matched_keywords = conversation_matched_keywords.keys(),
			participants = list(conversation_participants.keys()),
			last_message_time = last_message_time,
			source = self.communication_log['source'],
			enterprise_id = self.communication_log['enterprise_id'],			
		)