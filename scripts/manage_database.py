import sqlite3
import os
from pathlib import Path

current_path = Path(os.getcwd())
DB_FILE = str(current_path.parent) + "/db/db.sqlite3"

''' connection to sqlite3 database, OperationalError is raised when the database in not reachable '''
def connect_to_database():
	try:
		connection = sqlite3.connect(DB_FILE)
	except sqlite3.OperationalError as e:
		raise e
	return connection

''' create a database with 2 tables, the SQL statements are in this function '''
''' the created database is in the db folder'''
def create_database():
	try:
		connection = connect_to_database()
	except sqlite3.OperationalError as e:
		raise e

	cursor = connection.cursor()

	cursor.executescript(
	'''CREATE TABLE IF NOT EXISTS statuses (
		id integer PRIMARY KEY,
		name text NOT NULL);

	INSERT INTO statuses(id, name) VALUES
		(-1, \'FAILED\'),
   		(1, \'CREATED\'),
   		(2, \'COMPLETED\');

	CREATE TABLE IF NOT EXISTS payments (
    	id integer PRIMARY KEY,
    	value text NOT NULL,
    	currency text NOT NULL,
    	transaction_id integer NOT NULL,
    	created_at datetime NOT NULL,
    	status integer NOT NULL,
    	FOREIGN KEY(status) REFERENCES statuses (id) );''')

	connection.commit()
	connection.close()

'''deleting the database, do not use this just when you need to delete the database'''
def delete_database():
	try:
		connection = connect_to_database()
	except sqlite3.OperationalError as e:
		raise e

	cursor = connection.cursor()
	cursor.executescript("DROP TABLE payments; DROP TABLE statuses;")
	connection.commit()
	connection.close()

create_database()