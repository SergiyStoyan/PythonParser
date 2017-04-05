from logger import LOG
import settings
import pymongo
import mongo
import datetime

class States:
	DOWNLOADED = 'downloaded'
	PARSED = 'parsed'
	PARSING_ERROR = 'parsing_error'

try:
	collection
except:
	collection = mongo.Db['CommunicationLogs']	
	collection.create_index( 
		[
			('source', pymongo.ASCENDING), 
			('remote_file_name', pymongo.ASCENDING), 
			#('remote_file_modified_time', pymongo.ASCENDING)
		],
		unique = True
	)
			
def Add(
	source,
	remote_file_name,
	#remote_file_modified_time,
	file_name,
	enterprise_id,
):
	LOG.debug('CommunicationLogs:Add:', source, remote_file_name)
	r = collection.insert_one(
		{ 
			'source': source,
			'remote_file_name': remote_file_name,
			#'remote_file_modified_time': remote_file_modified_time,
			'file_name': file_name,
			'enterprise_id': enterprise_id,
			'state': States.DOWNLOADED,
			'created_time': datetime.datetime.now(),
			'parsed_time': None,
			#'error': None
		}
	)
	LOG.debug(r)
	return r
		
def DeleteById(
	_id,
):
	LOG.debug('CommunicationLogs:DeleteById:{0}'.format(_id))
	r = collection.remove(
		{
			'_id': _id,
		}
	)
	LOG.debug(r)
	return r
	
def GetByKey(
	source,
	remote_file_name,
	#remote_file_modified_time,
):
	LOG.debug('CommunicationLogs:GetByKey:', source, remote_file_name)
	r = collection.find_one(
		{
			'source': source,
			'remote_file_name': remote_file_name,
			#'remote_file_modified_time': remote_file_modified_time,
		}
	)
	LOG.debug(r)
	return r

def GetByStateSource(
	state,
	source
):
	set = {
		'state': state
	}
	if source:
		set['source'] = source
	r = collection.find(set)
	LOG.debug('CommunicationLogs:GetByStateSource:', r)
	return r

def SetParsed(
	communication_log_id,
	error = None
):
	LOG.debug('CommunicationLogs:Save:', communication_log_id, error)
	set = {
		'parsed_time': datetime.datetime.now(),
	}
	if error:
		set['error'] = 'PARSING: ' + str(error)
		set['state'] = States.PARSING_ERROR
	else:
		set['error'] = None
		set['state'] = States.PARSED
	r = collection.update_one(
		{ 
			'_id': communication_log_id,
		},
		{ 
			'$set': set,
		},
		upsert = False 
	)
	LOG.debug(r)
	return r
	
def GetFilePath(
	communication_log,
):
	return settings.DOWNLOAD_DIR + '/' + communication_log['source'] + '/' + communication_log['file_name']
		
def DeleteBySource(
	source,
):
	LOG.debug('CommunicationLogs:DeleteBySource:{0}'.format(source))
	r = collection.remove(
		{
			'source': source,
		}
	)
	LOG.debug(r)
	return r
