#by Sergey Stoyan: sergey.stoyan@gmail.com, stoyan@cliversoft.com
from logger import LOG
import settings
import db 
import os
import imp

print("""
USAGE:
>parser.py [<parse_source>] [<parse_state>]
where:
parse_source - CommunicationLogs.source to be parsed or one of the following: ['*', '.', '%'] as everything
parse_state - CommunicationLogs.state to be parsed
""")

def Execute(parse_source, parse_state):
	LOG.info('STARTED: ' + os.path.basename(__file__))
	LOG.info('parse_source: \'' + str(parse_source) + '\'')
	if not parse_state:
		parse_state = db.CommunicationLogs.States.DOWNLOADED#production mode: parsing newly downloaded logs
	LOG.info('parse_state: \'' + str(parse_state) + '\'')

	communication_logs = db.CommunicationLogs.GetByStateSource(
		state = parse_state,
		source = parse_source,
	)
	LOG.debug(communication_logs)	
	for communication_log in communication_logs:
		try:	
			file_path = settings.DOWNLOAD_DIR + '/' + communication_log['source'] + '/' + communication_log['file_name']
			if not os.path.exists(file_path):
				LOG.error('Does not exists: ' + file_path)
				continue
			LOG.info('Parsing: ' + file_path)
			parsers = imp.load_source('parsers', 'parsers/' + communication_log['source'] + '.py')
			#class_ = getattr(parsers, settings.COMMUNICATION_LOG_SOURCES[communication_log['source']]['ParserClass'])
			parser_class = getattr(parsers, communication_log['source'])
			parser = parser_class()
			parser.Parse(communication_log)
		except:
			LOG.exception(sys.exc_info()[0])

	LOG.info('COMPLETED')

if __name__ == '__main__':#not to run when this module is being imported
	import sys
	parse_source = None
	parse_state = None#production mode: parsing newly downloaded logs
	if len(sys.argv) > 1:
		parse_source = sys.argv[1]
		if parse_source in ['*', '.', '%']:
			parse_source = None
		if len(sys.argv) > 2:#testing mode: re-parsing old logs
			parse_state = sys.argv[2]
	Execute(parse_source, parse_state)