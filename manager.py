from logger import LOG
import sys

print("""
USAGE:
To run subsequently loader and parser:
>manager.py [<source>]
where:
source - CommunicationLogs.source to be processed or one of the following: ['*', '.', '%'] as everything
To delete all the data for a certain source: 
>manager.py drop <source>
""")

# LOG.info('STARTED')
#print sys.argv
if len(sys.argv) <= 2:
	source = None
	if len(sys.argv) > 1:
		source = sys.argv[1]
		if source in ['*', '.', '%']:
			source = None

	LOG.info('EXECUTING: loader')
	import loader	
	loader.Execute(source, None)

	LOG.info('EXECUTING: parser')	
	import parser
	parser.Execute(source, None)
	
else:
	command = sys.argv[1]
	if command == 'drop':
		source = sys.argv[2]
		if source in ['*', '.', '%']:
			source = None
		
		import db 
		import settings
		for source_name in settings.COMMUNICATION_LOG_SOURCES:
			if source and source_name != source:
				continue	
			answer = raw_input('ATTENTION! Dropping all the data for source: ' + source_name + '. Proceed? [y/n]').lower()
			if answer != 'y':
				print 'Canceled'
				continue	
			LOG.warning('Dropping Conversations for source: ' + source_name)
			db.Conversations.DeleteBySource(source_name)
			LOG.warning('Dropping Communications for source: ' + source_name)
			db.Communications.DeleteBySource(source_name)
			LOG.warning('Dropping CommunicationLogs for source: ' + source_name)
			db.CommunicationLogs.DeleteBySource(source_name)
			import os
			directory = settings.DOWNLOAD_DIR + '/' + source_name
			LOG.warning('Deleting: ' + directory)					
			if os.path.exists(directory):
				import shutil
				shutil.rmtree(directory)				
	else:
		print('Unknown command: ' + sys.argv[1])
			
# LOG.info('COMPLETED')