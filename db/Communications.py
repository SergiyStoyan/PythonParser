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
	collection = mongo.Db['Communications']
	
def Add(
	communication_log_id,
	#conversation_id,
	from_,
	to,
	message,
	message_time,
	matched_keywords,
	source,
	enterprise_id,
	#message_index,
	#thread_index,
	state = None,
	#error = None,
):
	LOG.debug('Communications:Add:', communication_log_id, from_, to)
	
	try:
		r = collection.insert_one(
			{ 		
				'communication_log_id': communication_log_id,
				#'conversation_id': conversation_id,
				'from': from_,
				'to': to,
				'message': message,
				'message_time': message_time,
				#'matched_keywords': matched_keywords,
				'state': state,
				#'error': error,
				'created_time': datetime.datetime.now(),
				#'updated_time': ,
				'matched_keywords': matched_keywords,
				'type': 'IM',
				'source': source,
				'enterprise_id': enterprise_id,
			}
		)
	except pymongo.errors.WriteError as we:
		LOG.error('{0}, {1}, {2}, {3}, {4}'.format(communication_log_id,from_,to,message,message_time))
		raise	
	LOG.debug(r)
	return r
	
def DeleteByCommunicationLogId(
	communication_log_id,
):
	LOG.debug('Communications:DeleteByCommunicationLogId:{0}'.format(communication_log_id))
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
	LOG.debug('Communications:DeleteBySource:{0}'.format(source))
	r = collection.remove(
		{
			'source': source,
		}
	)
	LOG.debug(r)
	return r
	
