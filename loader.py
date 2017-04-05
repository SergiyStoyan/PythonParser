#by Sergey Stoyan: sergey.stoyan@gmail.com, stoyan@cliversoft.com
from logger import LOG
import settings
import os
import paramiko
import db 

print("""
USAGE:
>loader.py [<load_source>] [<reload_state>]
where:
load_source - CommunicationLogs.source to be loaded or one of the following: ['*', '.', '%'] as everything
reload_state - CommunicationLogs.state to be reloaded
""")

def Execute(load_source, reload_state):
	def __download_communication_logs(source):	
		try:	
			LOG.info('Checking: ' + source['Name'])
			transport = paramiko.Transport(source['Host'], source['Port'])
			transport.connect(username = source['User'], password = source['Password'])
			sftp = paramiko.SFTPClient.from_transport(transport)
			sftp.chdir(source['RemoteDir'])
			files = sftp.listdir('.')
			for file in files:
				try:
					#lstat = sftp.lstat(file)
					#LOG.debug(file, lstat)	
					#communication_log = db.CommunicationLogs.GetByKey(source['Name'], file, lstat.st_mtime)	
					communication_log = db.CommunicationLogs.GetByKey(source['Name'], file)	
					
					if not reload_state:#production mode: only loading new logs, not reloading old ones
						if communication_log:
							continue
					else:#testing mode: only reloading old logs, not loading new ones
						if not communication_log:
							continue
						if communication_log['state'] != reload_state:
							continue					
						db.CommunicationLogs.DeleteById(communication_log['_id'])
						db.Conversations.DeleteByCommunicationLogId(communication_log['_id'])
						db.Communications.DeleteByCommunicationLogId(communication_log['_id'])
						
					unique_file_name = file #+ '.' + str(lstat.st_mtime)
					LOG.info('Loading: %s/%s', source['Name'], unique_file_name)
					directory = settings.DOWNLOAD_DIR + '/' + source['Name']
					if not os.path.exists(directory):
						os.makedirs(directory)
					sftp.get(file, directory + '/' + unique_file_name)
					db.CommunicationLogs.Add(
						source = source['Name'],
						remote_file_name = file,
						#remote_file_modified_time = lstat.st_mtime,
						file_name = unique_file_name,
						enterprise_id = source['EnterpriseId'],
					)
				except:
					LOG.exception(sys.exc_info()[0])
		except:
			LOG.exception(sys.exc_info()[0])

	LOG.info('STARTED: ' + os.path.basename(__file__))
	LOG.info('load_source: \'' + str(load_source) + '\'')
	LOG.info('reload_state: \'' + str(reload_state) + '\'')
	
	for source_name in settings.COMMUNICATION_LOG_SOURCES:
		if load_source and source_name != load_source:
			continue	
		source = settings.COMMUNICATION_LOG_SOURCES[source_name]
		source['Name'] = source_name
		__download_communication_logs(source)		
			
	LOG.info('COMPLETED')
	
if __name__ == '__main__':#not to run when this module is being imported
	import sys
	load_source = None
	reload_state = None#production mode: loading new logs
	if len(sys.argv) > 1:
		load_source = sys.argv[1]
		if load_source in ['*', '.', '%']:
			load_source = None
		if len(sys.argv) > 2:#testing mode: re-loading old logs
			reload_state = sys.argv[2]
	Execute(load_source, reload_state)