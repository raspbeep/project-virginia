import sqlite3
import os
from pathlib import Path

current_path = Path(os.getcwd())
DB_FILE = str(current_path.parent) + "/db/db.sqlite3"

def connect_to_database():
	conn = None
	try:
		conn = sqlite3.connect(DB_FILE)
	except sqlite3.OperationalError as e:
		print("Cound not connect to database")
		raise sqlite3.OperationalError
	return conn

def create_database():
	try:
		conn = connect_to_database()
	except sqlite3.OperationalError as e:
		print("Could not create the database")
		exit(-1)

	cur = conn.cursor()

	cur.executescript(
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


def delete_database():
	try:
		conn = connect_to_database()
	except sqlite3.OperationalError as e:
		print("Could not delete the database")
		exit(-1)

	cur = conn.cursor()
	cur.executescript("DROP TABLE payments; DROP TABLE statuses;")