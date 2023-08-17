from datetime import datetime
from peewee import *
import os
import json

# define a conexão com o banco de dados
db = SqliteDatabase(":memory:")
# db = PostgresqlDatabase('postgres', user='postgres', password='oCSM7dqa2nrR',
#                            host='127.0.0.1', port=5432)

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
folder_path = 'logger_output'
target_extension = '.json'

log_data = []

print("Looking for new files")
# Iterate over files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(target_extension):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as json_file:
            json_data = json.load(json_file)
            log = Log(
                    download = json_data['download'] / 1000000,
                    upload = json_data['upload'] / 1000000,
                    ping = json_data['ping']
                )
            log.save()
        try:
            os.remove(file_path)
            print(f"File '{file_path}' removed successfully.")
        except OSError as e:
            print(f"Error deleting '{file_path}': {e}")
