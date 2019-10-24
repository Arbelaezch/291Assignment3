import os
import time
import getpass
import sqlite3

connection = None
cursor = None

def close_connection():
	global connection
	connection.close()

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
	cursor.execute('SELECT utype FROM users WHERE uid=? AND pwd=?;', user)
	usr_login = cursor.fetchone()
	
	if usr_login == None:
		print('You fucked up!')
	else:
		return usr_login[0]


def login_screen():	
	while True:
		print("Welcome! Please (L)ogin or (E)xit.")
		action = input("Action: ")
		action = action.upper()
		if action == 'L':
			os.system('cls' if os.name=='nt' else 'clear')
			print("Please Log In")
			uid = input("User ID: ")
			password = getpass.getpass('Password: ')
			user = login(uid,password)
			if user == 'a':
				agent_menu(uid,password)
			elif user == 'o':
				officer_menu(uid,password)
		elif action == 'E':
			break
		else:
			print('Unknown action :(')
			os.system('cls' if os.name=='nt' else 'clear')
	return
	
	
def agent_menu(uid, password):
	while True:
		print("Welcome, Agent "+ uid +" "+ password +"!")
		print("What would you like to do?")
		print("1 - Register a birth\n2 - Register a marriage\n3 - Renew a vehicle registration\n4 - Process a bill of sale\n5 - Process a payment\n6 - Get a driver abstract")
		print("L - Logout")
		action = input("Action: ")
		if action == '1':
			register_birth()
		elif action == '2':
			register_marriage()
		elif action == '3':
			renew_registration()
		elif action == '4':
			process_BOS()
		elif action == '5':
			process_payment()
		elif action == '6':
			get_driver()
		elif (action == 'L') or (action == 'l'):
			print("Good byeeee")
			time.sleep(1)
			break
		else:
			print("Invalid entry!\n Please try again.")
			os.system('cls' if os.name=='nt' else 'clear')

def officer_menu(uid,pwd):
	while True:
		print("Welcome, Officer "+ uid +" "+ pwd +"!")
		print("What would you like to do?")
		print("1 - Issue a ticket\n2 - Find a car owner\nL - Logout")
		action = input("Action: ")
		if action == '1':
			issue_ticket()
		elif action == '2':
			find_owner()
		elif action == 'l' or action == 'L':
			print("Have a good day officer!")
			time.sleep(2)
			break

def register_birth():
	pass
def register_marriage():
	pass
def renew_registration():
	pass
def process_BOS():
	pass
def process_payment():
	pass
def get_driver():
	pass



def main():
	
	path = "./a3.db"
	defaultPath = path

	connect(path)

	login_screen()
	close_connection()

	return


if __name__ == "__main__":
    main()
