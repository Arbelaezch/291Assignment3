import os
import time
import getpass
import sqlite3

connection = None
cursor = None

def close_connection():
	con.close()

def connect(path):
	global connection, cursor

	connection = sqlite3.connect(path)
	cursor = connection.cursor()
	cursor.execute(' PRAGMA foreign_keys = ON; ')
	connection.commit()
	return

def login(uid,pwd):
	global connection, cursor

	user = (uid,pwd)
	cursor.execute('SELECT * FROM members WHERE uid=? AND pwd=?;', user)
	usr_login = cursor.fetchone()
	
	return usr_login



def login_screen():
	print("Welcome! Please (L)ogin or (E)xit.")
	action = input("Action: ")
	action = action.upper()
	if action == 'L':
		#os.system('cls' if os.name=='nt' else 'clear')
		print("Log In: ")
		uid = input("User ID: ")
		password = getpass.getpass('Password: ')
		user = login(uid,password)
		if user != None:
			user_menu(user)
		else:
			print("Invalid email or password!")


def main():
	
	path = "./a3.db"
	defaultPath = path

	connect(path)

	login_screen()
	close_connection()

	return


if __name__ == "__main__":
    main()
