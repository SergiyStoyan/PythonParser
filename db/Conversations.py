from logger import LOG
import settings
import pymongo
import mongo
import datetime
#from bson import ObjectId

class States:
	ARCHIVED = 'archived'
	#ERROR = 'error'

try:
	collection
except:	
	collection = mongo.Db['Conversations']
		
def Add(
	communication_log_id,
	communication_ids,
	#source,
	#enterprise_id,
	matched_keywords,
	participants,
	last_message_time,
	source,
	enterprise_id,
	state = None,
	error = None,
):
	LOG.debug('Conversations:Add:', communication_log_id, communication_ids)
	r = collection.insert_one(
		{ 
			'communication_log_id': communication_log_id,
			'communication_ids': communication_ids,
			#'source': source,
			#'enterprise_id': enterprise_id,
			'matched_keywords': matched_keywords,
			'participants': participants,
			'last_message_time': last_message_time,
			'source': source,
			'enterprise_id': enterprise_id,
			'state': state,
			'error': error,
		}
	)
	LOG.debug(r)
	return r
	
def DeleteByCommunicationLogId(
	communication_log_id,
):
	LOG.debug('Conversations:DeleteByCommunicationLogId:{0}'.format(communication_log_id))
	r = collection.remove(
		{
			'communication_log_id': str(communication_log_id),
		}
	)
	LOG.debug(r)
	return r	
		
def DeleteBySource(
	source,
):
	LOG.debug('Conversations:DeleteBySource:{0}'.format(source))
	r = collection.remove(
		{
			'source': source,
		}
	)
	LOG.debug(r)
	return r
	
