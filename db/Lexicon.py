from logger import LOG
import settings
import pymongo
import mongo
import datetime

#db.Lexicon.find().forEach(function(d){ db.getSiblingDB('parser1')['Lexicon'].insert(d); });

class States:
	ARCHIVED = 'archived'
	#ERROR = 'error'

try:
	collection
except:	
	collection = mongo.Db['Lexicon']
	
def GetByEnterprise(
	enterprise_id,
):
	LOG.debug('Lexicon:GetByEnterprise:', enterprise_id)
	r = collection.find(
		{
			'enterprise_id': enterprise_id,
		}
	)
	LOG.debug(r)
	return r
	