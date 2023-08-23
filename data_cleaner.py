from datetime import datetime
from peewee import *
import os
import json

# # TODO: test again once the cron env variables issue is fixed
# env_db_host = os.environ.get('DB_HOST')
# env_db_pass = os.environ.get('DB_PASS')
# env_logger_output = os.environ.get('LOGGER_OUTPUT')

# # Check if an environment variable exists and get its value
# if not env_db_host or not env_db_pass or not env_logger_output:
#     print(f'ERROR: One or more environment variables are missing. ({env_db_host}|{env_db_pass}|{env_logger_output})')
#     exit(code=1)

# db = SqliteDatabase(":memory:")
db = PostgresqlDatabase('postgres', user='postgres', password='oCSM7dqa2nrR',
                           host='db', port=5432)

class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = db

class Log(BaseModel):
    id = AutoField(primary_key=True)
    download = IntegerField()
    upload = IntegerField()
    ping = IntegerField()
    created_on = DateTimeField(default=datetime.now)

# Creates log table if nonexistent
if 'log' not in db.get_tables():
    print("Creating table log")
    db.create_tables([Log])

# Scanning for new logger outputs
folder_path = '/home/logger_output'
target_extension = '.json'

log_data = []

print("Looking for new files")
# Iterate over files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(target_extension):
        file_path = os.path.join(folder_path, filename)
        print(f"Handling file {file_path}")
        with open(file_path, 'r') as json_file:
            try:
                json_data = json.load(json_file)
                log = Log(
                        download = json_data['download'] / 1000000,
                        upload = json_data['upload'] / 1000000,
                        ping = json_data['ping']
                    )
                log.save()
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
            
            try:
                os.remove(file_path)
                print(f"File '{file_path}' removed successfully.")
            except OSError as e:
                print(f"Error deleting '{file_path}': {e}")
