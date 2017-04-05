from logger import LOG
import settings
import pymongo

try:
	Db
except:
	client = pymongo.MongoClient(settings.DB_HOST, settings.DB_PORT)
	Db = client[settings.DB_NAME]	
	#LOG.info('# Db open #')