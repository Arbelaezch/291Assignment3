import os
import time
import getpass
import sqlite3
import random

connection = None
cursor = None

# I like keeping table names in string variables to minimize errors
# region Table Constants
# region Persons
TABLE_PERSONS = "persons"
PERSONS_FNAME = "fname"
PERSONS_LNAME = "lname"
PERSONS_BDATE = "bdate"
PERSONS_BPLACE = "bplace"
PERSONS_ADDRESS = "address"
PERSONS_PHONE = "phone"
# endregion

# region
TABLE_VEHICLES = "vehicles"
VEHICLES_VIN = "vin"
VEHICLES_MAKE = "make"
VEHICLES_MODEL = "model"
VEHICLES_YEAR = "year"
VEHICLES_COLOR = "color"
# endregion

# region Registrations
TABLE_REGISTRATIONS = "registrations"
REGISTRATION_REGNO = "regno"
REGISTRATION_REGDATE = "regdate"
REGISTRATION_EXPIRY = "expiry"
REGISTRATION_PLATE = "plate"
REGISTRATION_VIN = "vin"
REGISTRATION_FNAME = "fname"
REGISTRATION_LNAME = "lname"
# endregion

# region Tickets
TABLE_TICKETS = "tickets"
TICKETS_TNO = "tno"
TICKETS_REGNO = "regno"
TICKETS_FINE = "fine"
TICKETS_VIOLATION = "violation"
TICKETS_VDATE = "vdate"
# endregion

# region DemeritNotices
TABLE_DEMERITS = "demeritNotices"
DEMERITS_DDATE = "ddate"
DEMERITS_FNAME = "fname"
DEMERITS_LNAME = "lname"
DEMERITS_POINTS = "points"
DEMERITS_DESC = "desc"
# endregion

# region Payments
TABLE_PAYMENTS = "payments"
PAYMENTS_TNO = "tno"
PAYMENTS_PDATE = "pdate"
PAYMENTS_AMOUNT = "amount"
# endregion
# endregion

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
	# Need to check if empty strings appear as null in SQL
	global cursor

	p1fname = input("Enter the first name of partner 1: ")
	p1lname = input("Enter the last name of partner 1: ")
	p2fname = input("Enter the first name of partner 2: ")
	p2lname = input("Enter the last name of partner 2: ")
	reg_number = random.randint(100, 999)
	current_date = time.strftime("%Y-%m-%d")
	reg_place = "Edmonton"
	try:
		cursor.execute("insert into marriages values (?, ?, ?, ?, ?, ?, ?);", [str(reg_number), current_date, reg_place, p1fname, p1lname, 
		p2fname, p2lname])
	except sqlite3.IntegrityError:
		pass
	cursor.execute("select fname, lname from persons where fname=? and lname=?;", [p1fname, p1lname])
	if cursor.fetchone() == None:
		print("Partner 1 is not in our database. Please provide additional information:")
		valid_chars = 0
		while True:
			bday = input("Enter date of birth YYYY-MM-DD (optional): ")
			if bday == '':
				break
			if len(bday) != 10:
				print("Birth date must be entered as YYYY-MM-DD")
				continue
			for i in range(10):
				try:
					int_bday = int(bday[i])
				except:
					if bday[i] != '-':
						print("Birth date must be entered as YYYY-MM-DD")
						break
				if bday[i] == '-' and i != 4 and i != 7:
					print("Birth date must be entered as YYYY-MM-DD")
					break
				else:
					valid_chars += 1
			if valid_chars == 10:
				break
		place = input("Enter place of birth (optional): ")
		addr = input("Enter your current address (optional): ")
		phone_no = input("Enter your phone number (optional): ")
		cursor.execute("insert into persons values (?, ?, ?, ?, ?, ?);", [p1fname, p1lname, bday, place, addr, phone_no])
		
	cursor.execute("select fname, lname from persons where fname=? and lname=?;", [p2fname, p2lname])
	if cursor.fetchone() == None:
		print("Partner 2 is not in our database. Please provide additional information:")
		valid_chars = 0
		while True:
			bday = input("Enter date of birth YYYY-MM-DD (optional): ")
			if bday == '':
				break
			if len(bday) != 10:
				print("Birth date must be entered as YYYY-MM-DD")
				continue
			for i in range(10):
				try:
					int_bday = int(bday[i])
				except:
					if bday[i] != '-':
						print("Birth date must be entered as YYYY-MM-DD")
						break
				if bday[i] == '-' and i != 4 and i != 7:
					print("Birth date must be entered as YYYY-MM-DD")
					break
				else:
					valid_chars += 1
			if valid_chars == 10:
				break
		place = input("Enter place of birth (optional): ")
		addr = input("Enter your current address (optional): ")
		phone_no = input("Enter your phone number (optional): ")
		cursor.execute("insert into persons values (?, ?, ?, ?, ?, ?);", [p2fname, p2lname, bday, place, addr, phone_no])
	return

def renew_registration():
	pass

def process_BOS(): 
	# todo: double check what they mean by cars not having owners
	# does this mean that it is registered but the owners are null
	# or that vin does not exist anywhere in registrations
	# what happens if the registration from transfer is already expired???
	"""
	The user should be able to record a bill of sale by providing the vin of a 
	car, the name of the current owner, the name of the new owner, and a 
	plate number for the new registration. If the name of the current owner 
	(that is provided) does not match the name of the most recent owner of the 
	car in the system, the transfer cannot be made.
	"""
	global connection, cursor

	vin = input("Enter vin: ")
	current_owner = input("Enter current owner name: ")
	new_owner = input("Enter new owner name: ")
	plate = input("Enter a plate number: ")
	
	# validate person
	q_person = """SELECT {p_fname}, {p_lname}
	FROM {p}
	WHERE {p_fname} || " " || {p_lname} LIKE :new_owner;
	""".format(p=TABLE_PERSONS, p_fname=PERSONS_FNAME, p_lname=PERSONS_LNAME)
	cursor.execute(q_person, {"new_owner" : new_owner})
	person_name = cursor.fetchone()

	if person_name == None:
		print("New owner is not in database. Transaction cannot be made")
		return
	
	fname = person_name[0]
	lname = person_name[1]

	# check which case of process BOS to take
	q_case = """SELECT * FROM
	(
		SELECT {v_vin}
		FROM {v}
		WHERE {v_vin} LIKE :vin
	) A
	LEFT OUTER JOIN
	(
		SELECT {r_vin}
		FROM {r}
		WHERE {r_vin} LIKE :vin
	) B
	ON A.{v_vin}=B.{r_vin};
	""".format(v=TABLE_VEHICLES, v_vin=VEHICLES_VIN, r=TABLE_REGISTRATIONS,
	r_vin=REGISTRATION_VIN)
	cursor.execute(q_case, {"vin" : vin})
	car_details = cursor.fetchone()

	if car_details == None:
		print("Car with vin {0} does not exist. Transfer failed.".format(vin))
		return
	
	is_car_new = car_details[1] == None

	if is_car_new:
		print("Car with vin {0} has no owner yet.".format(vin))
	else:
		q_validation = """SELECT {r_regno}
			FROM {r}
			WHERE {r_vin} LIKE :c_vin AND {r_fname} || " " || {r_lname} LIKE :c_owner
			ORDER BY {r_regdate} DESC
			LIMIT 1;
		""".format(r=TABLE_REGISTRATIONS, r_vin=REGISTRATION_VIN,
			r_fname=REGISTRATION_FNAME, r_lname=REGISTRATION_LNAME,
			r_regno=REGISTRATION_REGNO, r_regdate=REGISTRATION_REGDATE)
		cursor.execute(q_validation, {"c_vin" : vin, "c_owner" : current_owner})
		reg_no = cursor.fetchone()

		if reg_no == None:
			# In finding the owner of a car, if a car is not registered, 
			# you will indicate in your output that the car has no owner.
			# Check if car is owned, if not, register the car as new
			print("Transfer cannot be made. Some details are invalid.")
			return
		reg_no = reg_no[0]

		# update expiry date if car has already been registered with an owner
		q_update = """UPDATE {r} 
		SET {r_exp} = date('now')
		WHERE {r_regno} = :c_regno;
		""".format(r=TABLE_REGISTRATIONS, r_exp=REGISTRATION_EXPIRY, 
		r_regno=REGISTRATION_REGNO)
		cursor.execute(q_update, {"c_regno" : reg_no})
	
	"""
	When the transfer can be made, the expiry date of the current 
	registration is set to today's date 
	and a new registration under the new owner's name is recorded with the 
	registration date and the expiry date set by the system to today's date 
	and a year after today's date respectively. Also a unique registration 
	number should be assigned by the system to the new registration. The vin 
	will be copied from the current registration to the new one.
	"""

	# create new registration
	new_regno = find_available_id(TABLE_REGISTRATIONS, REGISTRATION_REGNO)
	q_insert = """INSERT INTO {r}
	VALUES(:new_regno, date('now'), date('now', '1 year'),
			:plate, :vin, :fname, :lname);
	""".format(r=TABLE_REGISTRATIONS)
	cursor.execute(q_insert, {"new_regno" : new_regno, 
		"plate" : plate, "vin" : vin, "fname" : fname, "lname" : lname})

	connection.commit()
	if is_car_new:
		print("Registration successful!")
	else:
		print("Transfer successful!")



def process_payment():
	# based on payment's schema, you can't pay more than once a day for single tno
	# i'm not sure if that was their intention
	# todo: validate if already paid today (???)
	"""
	The user should be able to record a payment by entering a valid
	ticket number and an amount. The payment date is automatically set to
	the day of the payment (today's date). A ticket can be paid in
	multiple payments but the sum of those payments cannot exceed the
	fine amount of the ticket.
	"""
	global connection, cursor

	# region validate ticket existence
	ticket_number = input("Enter a valid ticket number: ")
	# todo: check if ticket_number is only a number???

	q_ticket_validation = """SELECT {t_fine} FROM {t} WHERE {t_tno} = :c_tno;
		""".format(t=TABLE_TICKETS, t_fine=TICKETS_FINE, t_tno=TICKETS_TNO)
	cursor.execute(q_ticket_validation, {"c_tno": ticket_number})
	r_fine = cursor.fetchone()

	if r_fine is None:
		# todo: improve warning
		# there is no such ticket
		print("No such ticket")
		return
	else:
		print("Ticket exists! Yay! Remove this please!!!")
		fine = r_fine[0]
	# endregion

	# region validate amount is not over
	amount_input = input("Enter payment amount: ")

	try:
		amount = int(amount_input)
	except ValueError:
		# todo improve message
		print("That's not a number!!!")
		return

	if amount <= 0:
		# todo: improve message
		print("Invalid amount")
		return

	q_fine_validation = """SELECT SUM({p_amount})
	FROM {p}
	WHERE {p_tno} = :c_tno;
	""".format(p=TABLE_PAYMENTS, p_amount=PAYMENTS_AMOUNT, p_tno=PAYMENTS_TNO)
	cursor.execute(q_fine_validation, {"c_tno": ticket_number})
	old_payments = cursor.fetchone()[0]

	if old_payments is not None and (old_payments + amount) > fine:
		# todo: improve message
		print("Over paid. Cancelling")
		return
	else:
		#todo: remove
		print("Not overpaid")

	# endregion

	# region insert payment
	q_insert = """INSERT INTO {p} VALUES(?, date('now'), ?);
	""".format(p=TABLE_PAYMENTS)
	cursor.execute(q_insert, (ticket_number, amount_input))
	connection.commit()
	print("Payment successful")
	# endregion
	

def get_driver():
	"""
	Get a driver abstract. The user should be able to enter a first name and a 
	last name and get a driver abstract, which includes the number of tickets, 
	the number of demerit notices, the total number of demerit points received 
	both within the past two years and within the lifetime.
	"""
	global connection, cursor
	clear_screen()
	first_name = input("Enter a first name: ")
	last_name = input("Enter a last name: ")

	# Validate that the person in our system
	query = """SELECT * FROM {r}
	WHERE {r_fname} LIKE :fname AND {r_lname} LIKE :lname;
	""".format(r=TABLE_REGISTRATIONS, r_fname=REGISTRATION_FNAME, 
		r_lname=REGISTRATION_LNAME)
	cursor.execute(query, {"fname" : first_name, "lname" : last_name})
	result = cursor.fetchone()

	if result == None:
		print("{0} {1} is not registered in the database.".format(first_name, last_name))
		print("Unable to get driver abstract.")
		return
	
	ticket_count = 0
	demerit_count = 0
	latest_points = 0
	lifetime_points = 0

	query = """SELECT COUNT(*) FROM {r}, {t}
	WHERE {r}.{r_fname} LIKE :fname AND {r}.{r_lname} LIKE :lname AND 
		{t}.{t_regno} = {r}.{r_regno};
	""".format(r=TABLE_REGISTRATIONS, t=TABLE_TICKETS, r_fname=REGISTRATION_FNAME,
		r_lname=REGISTRATION_LNAME, t_regno=TICKETS_REGNO, r_regno=REGISTRATION_REGNO)
	cursor.execute(query, {"fname" : first_name, "lname" : last_name})
	result = cursor.fetchone()

	if result != None:
		print("We got the result: " + str(result[0]))
		ticket_count = result[0]
	else:
		print("We are here!")

	query = """SELECT COUNT(*), SUM({d_points}) FROM {d}
	WHERE {d_fname} LIKE :fname AND {d_lname} LIKE :lname;
	""".format(d=TABLE_DEMERITS, d_fname=DEMERITS_FNAME, d_lname=DEMERITS_LNAME,
		d_points=DEMERITS_POINTS)
	cursor.execute(query, {"fname" : first_name, "lname" : last_name})
	result = cursor.fetchone()

	if result != None:
		demerit_count = result[0]
		lifetime_points = result[1]
		if lifetime_points == None:
			lifetime_points = 0

	# todo: decide if < or <=, just think about that later
	query = """SELECT SUM({d_points}) FROM {d}
	WHERE {d_fname} LIKE :fname AND {d_lname} LIKE :lname 
		AND {d_ddate} >= date('now', '-2 year');
	""".format(d=TABLE_DEMERITS, d_fname=DEMERITS_FNAME, d_lname=DEMERITS_LNAME,
		d_points=DEMERITS_POINTS, d_ddate=DEMERITS_DDATE)
	cursor.execute(query, {"fname" : first_name, "lname" : last_name})
	result = cursor.fetchone()

	if result != None and result[0] != None:
		latest_points = result[0]
	
	messages = ("Driver abstract for {0} {1}".format(first_name, last_name),
		"Number of tickets: {0}".format(ticket_count),
		"Number of demerit notices: {0}".format(demerit_count),
		"Demerit points within the past two years: {0}".format(latest_points),
		"Lifetime demerits points: {0}".format(lifetime_points))
	display_messages(messages)

	"""
	The user should be given the option to see 
	the tickets ordered from the latest to the oldest. 
	For each ticket, you will report the ticket number, the violation date, 
	the violation description, the fine, the registration number and the make 
	and model of the car for which the ticket is issued. If there are more than 
	5 tickets, at most 5 tickets will be shown at a time, and the user can 
	select to see more.
	"""
	message_list = ("Do you want to see the tickets that {0} has received?"
			.format(first_name + " " + last_name),
		"Enter y or Y only to see the tickets.",
		"Any other input would send you back to the main menu.")
	display_messages(message_list)
	should_see_ticket = input("Input: ")

	clear_screen()
	if not (should_see_ticket.lower() == "y"):
		return
	
	query = """SELECT {t}.{t_tno}, {t}.{t_vdate}, {t}.{t_violation}, 
		{t}.{t_fine}, {t}.{t_regno}, {v}.{v_make}, {v}.{v_model}
	FROM {t}, {r}, {v}
	WHERE {r}.{r_fname} LIKE :fname AND {r}.{r_lname} LIKE :lname AND 
		{r}.{r_regno} = {t}.{t_regno} AND {v}.{v_vin} = {r}.{r_vin}
	ORDER BY {t}.{t_vdate} DESC;
	""".format(t=TABLE_TICKETS, r=TABLE_REGISTRATIONS, v=TABLE_VEHICLES,
		t_tno=TICKETS_TNO, t_vdate=TICKETS_VDATE, t_violation=TICKETS_VIOLATION,
		t_fine=TICKETS_FINE, t_regno=TICKETS_REGNO, v_make=VEHICLES_MAKE,
		v_model=VEHICLES_MODEL, r_fname=REGISTRATION_FNAME,
		r_lname=REGISTRATION_LNAME, v_vin=VEHICLES_VIN, r_regno=REGISTRATION_REGNO,
		r_vin=REGISTRATION_VIN)
	cursor.execute(query, {"fname" : first_name, "lname" : last_name})
	result = cursor.fetchall()
	
	if result == None:
		print("{0} {1} has no tickets in the record".format(first_name, last_name))
		return

	MAX_TICKET_VIEW = 5
	ind = 0

	print("Ticket details: ")
	while ind < len(result):
		if ind != 0 and ind % MAX_TICKET_VIEW == 0:
			should_see_ticket = input("Enter ""Y"" to see more: ")

			clear_screen()
			if not (should_see_ticket.lower() == "y"):
				return
			print("Ticket details: ")
		else:
			row = result[ind]
			messages = ("-"*20,
				"Ticket number: {0}".format(row[0]),
				"-"*20,
				"Violation date: {0}".format(row[1]),
				"Violation description: {0}".format(row[2]),
				"Fine: {0}".format(row[3]),
				"Registration number: {0}".format(row[4]),
				"Vehicle make: {0}".format(row[5]),
				"Vehicle model: {0}".format(row[6]),
				"-"*20,
				"")
			display_messages(messages)
			ind += 1
	
	input("Press enter to go back to the menu.")
	clear_screen()


def find_available_id(table, column):
	"""
	Finds the next appropriate integer id for a column in a given table
	It does this by finding the max and incrementing it by one
	"""
	global connection, cursor

	query = """
	SELECT MAX({c}) FROM {t};
	""".format(t=table, c=column)

	cursor.execute(query)
	max_id = cursor.fetchone()
	available_id = 1

	if max_id is not None:
		available_id = max_id[0] + 1

	return available_id

def clear_screen():
	os.system('cls' if os.name=='nt' else 'clear')

def display_messages(list_of_messages):
	for item in list_of_messages:
		print(item)

def main():
	
	path = "./a3.db"
	defaultPath = path

	connect(path)

	login_screen()
	close_connection()

	return


if __name__ == "__main__":
	main()
