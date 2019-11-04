import os
import time
import getpass
import sqlite3

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
	global cursor

	cursor.execute("select city from users where uid=?;", [uid])
	city = cursor.fetchone()[0]
	while True:
		print("Welcome, Agent "+ uid +" "+ password +"!")
		print("What would you like to do?")
		print("1 - Register a birth\n2 - Register a marriage\n3 - Renew a vehicle registration\n4 - Process a bill of sale\n5 - Process a payment\n6 - Get a driver abstract")
		print("L - Logout")
		action = input("Action: ")
		if action == '1':
			register_birth(city)
		elif action == '2':
			register_marriage(city)
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

def register_birth(reg_place):
	global cursor, connection

	while True:
		fname = input("Enter the first name of the child: ")
		if fname != '':
			break
	while True:
		lname = input("Enter the last name of the child: ")
		if lname != '':
			break
	cursor.execute("select fname, lname from persons where fname=? and lname=?;", [fname, lname])
	if cursor.fetchone() != None:
		print("This person is already in our database.")
		return
	
	while True:
		gender = input("Enter the gender of the child (M or F): ")
		if gender == 'M' or gender == 'F' or gender == 'm' or gender == 'f':
			gender = gender.upper()
			break
	while True:
			valid_chars = 0
			bdate = input("Enter date of birth (YYYY-MM-DD): ")
			if len(bdate) != 10:
				print("Birth date must be entered as YYYY-MM-DD")
				continue
			for i in range(10):
				try:
					int_bday = int(bdate[i])
				except:
					if bdate[i] != '-':
						print("Birth date must be entered as YYYY-MM-DD")
						break
				if (i == 4 or i == 7) and bdate[i] != '-':
					print("Birth date must be entered as YYYY-MM-DD")
					break
				if bdate[i] == '-' and i != 4 and i != 7:
					print("Birth date must be entered as YYYY-MM-DD")
					break
				else:
					valid_chars += 1
			if valid_chars == 10:
				break
	while True:
		bplace = input("Enter the place of birth: ")
		if bplace != '':
			break
	while True:
		m_fname = input("Mother's first name: ")
		if m_fname != '':
			break
	while True:
		m_lname = input("Mother's last name: ")
		if m_lname != '':
			break
	while True:
		f_fname = input("Father's first name: ")
		if f_fname != '':
			break
	while True:
		f_lname = input("Father's last name: ")
		if f_lname != '':
			break
	
	cursor.execute("select * from persons where fname=? and lname=?;", [m_fname, m_lname])
	mother = cursor.fetchone()
	if mother == None:
		print("Mother is not in our database. Please provide additional information:")
		while True:
			valid_chars = 0
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
				if (i == 4 or i == 7) and bday[i] != '-':
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
		if bday == '':
			bday = None
		if place == '':
			place = None
		if addr == '':
			addr = None
		if phone_no == '':
			phone_no = None
		cursor.execute("insert into persons values (?, ?, ?, ?, ?, ?);", [m_fname, m_lname, bday, place, addr, phone_no])
		cursor.execute("insert into persons values (?, ?, ?, ?, ?, ?);", [fname, lname, bdate, bplace, addr, phone_no])
	else:
		cursor.execute("insert into persons values (?, ?, ?, ?, ?, ?);", [fname, lname, bdate, bplace, mother[4], mother[5]])

	cursor.execute("select fname, lname from persons where fname=? and lname=?;", [f_fname, f_lname])
	if cursor.fetchone() == None:
		print("Father is not in our database. Please provide additional information:")
		while True:
			valid_chars = 0
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
				if (i == 4 or i == 7) and bday[i] != '-':
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
		if bday == '':
			bday = None
		if place == '':
			place = None
		if addr == '':
			addr = None
		if phone_no == '':
			phone_no = None
		cursor.execute("insert into persons values (?, ?, ?, ?, ?, ?);", [f_fname, f_lname, bday, place, addr, phone_no])
	reg_number = find_available_id("births", "regno")
	current_date = time.strftime("%Y-%m-%d")
	cursor.execute("insert into births values (?,?,?,?,?,?,?,?,?,?);", [str(reg_number),fname,lname,current_date,reg_place,gender,
	f_fname,f_lname,m_fname,m_lname])
	connection.commit()

def register_marriage(reg_place):
	global cursor, connection

	while True:
		p1fname = input("Enter the first name of partner 1: ")
		if p1fname != '':
			break
	while True:
		p1lname = input("Enter the last name of partner 1: ")
		if p1lname != '':
			break
	while True:
		p2fname = input("Enter the first name of partner 2: ")
		if p2fname != '':
			break
	while True:
		p2lname = input("Enter the last name of partner 2: ")
		if p2lname != '':
			break
	reg_number = find_available_id("marriages", "regno")
	current_date = time.strftime("%Y-%m-%d")

	cursor.execute("select fname, lname from persons where fname=? and lname=?;", [p1fname, p1lname])
	if cursor.fetchone() == None:
		print("Partner 1 is not in our database. Please provide additional information:")
		while True:
			valid_chars = 0
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
				if (i == 4 or i == 7) and bday[i] != '-':
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
		if bday == '':
			bday = None
		if place == '':
			place = None
		if addr == '':
			addr = None
		if phone_no == '':
			phone_no = None
		cursor.execute("insert into persons values (?, ?, ?, ?, ?, ?);", [p1fname, p1lname, bday, place, addr, phone_no])
		
	cursor.execute("select fname, lname from persons where fname=? and lname=?;", [p2fname, p2lname])
	if cursor.fetchone() == None:
		print("Partner 2 is not in our database. Please provide additional information:")
		while True:
			valid_chars = 0
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
				if (i == 4 or i == 7) and bday[i] != '-':
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
		if bday == '':
			bday = None
		if place == '':
			place = None
		if addr == '':
			addr = None
		if phone_no == '':
			phone_no = None
		cursor.execute("insert into persons values (?, ?, ?, ?, ?, ?);", [p2fname, p2lname, bday, place, addr, phone_no])

	cursor.execute("insert into marriages values (?, ?, ?, ?, ?, ?, ?);", [str(reg_number), current_date, reg_place, p1fname, p1lname, 
		p2fname, p2lname])
	connection.commit()

def renew_registration():
	global cursor, connection
	while True:
		reg_no = input("Enter the registration number: ")
		try:
			reg_no = int(reg_no)
		except:
			print("Not a valid registration number.")
			continue
		cursor.execute("select regno, expiry from registrations where regno=?;", [reg_no])
		reg = cursor.fetchone()
		if reg != None:
			break
		else:
			print("This registration number does not exist.")
	if reg[1] <= time.strftime("%Y-%m-%d"):
		cursor.execute("select date('now', '+1 year');")
		new_expiry = cursor.fetchone()[0]
	else:
		cursor.execute("select date(?, '+1 year');", [reg[1],])
		new_expiry = cursor.fetchone()[0]
	cursor.execute("update registrations set expiry=? where regno=?", [new_expiry, reg_no])
	connection.commit()

def process_BOS(): 
	"""
	The user should be able to record a bill of sale by providing the vin of a 
	car, the name of the current owner, the name of the new owner, and a 
	plate number for the new registration. If the name of the current owner 
	(that is provided) does not match the name of the most recent owner of the 
	car in the system, the transfer cannot be made.
	"""
	global connection, cursor

	new_screen("Processing a bill of sale")
	vin = input("Enter vin: ")
	current_owner = input("Enter current owner name: ")
	new_owner = input("Enter new owner name: ")
	plate = input("Enter a plate number: ")
	
	# region validate person
	query = """SELECT {p_fname}, {p_lname}
	FROM {p}
	WHERE {p_fname} || " " || {p_lname} LIKE :new_owner;
	""".format(p=TABLE_PERSONS, p_fname=PERSONS_FNAME, p_lname=PERSONS_LNAME)
	cursor.execute(query, {"new_owner" : new_owner})
	result = cursor.fetchone()

	if result == None:
		print("New owner is not in database. Transaction cannot be made")
		transition_screen()
		return

	fname = result[0]
	lname = result[1]
	# endregion

	# check which case of process BOS to take
	query = """SELECT * FROM
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
	cursor.execute(query, {"vin" : vin})
	result = cursor.fetchone()

	if result == None:
		print("Car with vin {0} does not exist. Transfer failed.".format(vin))
		transition_screen()
		return
	
	vin = result[0]
	is_car_new = result[1] == None

	if is_car_new:
		print("Car with vin {0} has no owner yet.".format(vin))
	else:
		query = """SELECT {r_regno}, {r_fname} || " " || {r_lname}
			FROM {r}
			WHERE {r_vin} LIKE :c_vin
			ORDER BY {r_regexp} DESC
			LIMIT 1;
		""".format(r=TABLE_REGISTRATIONS, r_vin=REGISTRATION_VIN,
			r_fname=REGISTRATION_FNAME, r_lname=REGISTRATION_LNAME,
			r_regno=REGISTRATION_REGNO, r_regexp=REGISTRATION_EXPIRY)
		cursor.execute(query, {"c_vin" : vin})
		result = cursor.fetchone()

		if result == None or result[1].lower() != current_owner.lower():
			print("Transfer cannot be made. Some details are invalid.")
			transition_screen()
			return
		
		reg_no = result[0]

		# update expiry date if car has already been registered with an owner
		query = """UPDATE {r} 
		SET {r_exp} = date('now')
		WHERE {r_regno} = :c_regno;
		""".format(r=TABLE_REGISTRATIONS, r_exp=REGISTRATION_EXPIRY, 
		r_regno=REGISTRATION_REGNO)
		cursor.execute(query, {"c_regno" : reg_no})
	
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
	query = """INSERT INTO {r}
	VALUES(:new_regno, date('now'), date('now', '1 year'),
			:plate, :vin, :fname, :lname);
	""".format(r=TABLE_REGISTRATIONS)
	cursor.execute(query, {"new_regno" : new_regno, 
		"plate" : plate, "vin" : vin, "fname" : fname, "lname" : lname})

	connection.commit()
	if is_car_new:
		print("Registration successful!")
	else:
		print("Transfer successful!")
	transition_screen()



def process_payment():
	"""
	Note: This does not consider values with decimal points. 
	Values are truncated to an integer.
	The user should be able to record a payment by entering a valid
	ticket number and an amount. The payment date is automatically set to
	the day of the payment (today's date). A ticket can be paid in
	multiple payments but the sum of those payments cannot exceed the
	fine amount of the ticket.
	"""
	global connection, cursor
	new_screen("Processing a payment")

	# region validate ticket existence
	ticket_number = input("Enter a valid ticket number: ")

	query = """SELECT {t_fine} FROM {t} WHERE {t_tno} = :c_tno;
		""".format(t=TABLE_TICKETS, t_fine=TICKETS_FINE, t_tno=TICKETS_TNO)
	cursor.execute(query, {"c_tno": ticket_number})
	result = cursor.fetchone()

	if result == None:
		print("Ticket does not exist in the system.")
		transition_screen()
		return
		
	fine = result[0]
	# endregion

	# region validate if payment was made
	query = """SELECT * FROM {p} 
	WHERE {p_tno} = :c_tno AND {p_pdate} = date('now');
	""".format(p=TABLE_PAYMENTS, p_tno=PAYMENTS_TNO, p_pdate=PAYMENTS_PDATE)
	cursor.execute(query, {"c_tno" : ticket_number})
	result = cursor.fetchone()

	if result != None:
		print("Payment was already made for this ticket today.")
		transition_screen()
		return
	# endregion

	# region validate amount is not over
	amount_input = input("Enter payment amount: ")

	try:
		if "." in amount_input:
			print("Warning: values after a decimal point are ignored")
			amount_input = amount_input.split(".")[0]
		amount = int(amount_input)
		print("Payment amount entered is: {0}".format(amount))
	except ValueError:
		print("Given amount is not a number.")
		transition_screen()
		return

	if amount <= 0:
		print("Invalid amount.")
		transition_screen()
		return

	query = """SELECT SUM({p_amount})
	FROM {p}
	WHERE {p_tno} = :c_tno;
	""".format(p=TABLE_PAYMENTS, p_amount=PAYMENTS_AMOUNT, p_tno=PAYMENTS_TNO)
	cursor.execute(query, {"c_tno": ticket_number})
	
	old_payments = cursor.fetchone()[0]
	if old_payments == None:
		old_payments = 0

	if old_payments != None and (old_payments + amount) > fine:
		print("Over paid. Cancelling payment.")
		transition_screen()
		return
	# endregion

	# region insert payment
	q_insert = """INSERT INTO {p} VALUES(?, date('now'), ?);
	""".format(p=TABLE_PAYMENTS)
	cursor.execute(q_insert, (ticket_number, amount_input))
	connection.commit()
	print("Payment successful")
	transition_screen()
	# endregion
	

def get_driver():
	"""
	Get a driver abstract. The user should be able to enter a first name and a 
	last name and get a driver abstract, which includes the number of tickets, 
	the number of demerit notices, the total number of demerit points received 
	both within the past two years and within the lifetime.
	"""
	global connection, cursor
	new_screen("Driver abstract")

	first_name = input("Enter a first name: ")
	last_name = input("Enter a last name: ")

	# region Validate that the person in our system
	query = """SELECT * FROM {r}
	WHERE {r_fname} LIKE :fname AND {r_lname} LIKE :lname;
	""".format(r=TABLE_REGISTRATIONS, r_fname=REGISTRATION_FNAME, 
		r_lname=REGISTRATION_LNAME)
	cursor.execute(query, {"fname" : first_name, "lname" : last_name})
	result = cursor.fetchone()

	if result == None:
		print("{0} {1} is not registered in the database.".format(first_name, last_name))
		print("Unable to get driver abstract.")
		transition_screen()
		return
	# endregion

	# region Get values for the abstract	
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
		ticket_count = result[0]

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

	# Uses > for checking the date, excludes dates exactly 2 years earlier than now
	query = """SELECT SUM({d_points}) FROM {d}
	WHERE {d_fname} LIKE :fname AND {d_lname} LIKE :lname 
		AND {d_ddate} > date('now', '-2 year');
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
	# endregion

	if ticket_count == 0:
		transition_screen()
		return

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
		# this should never happen but it's here for safety
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
		
		row = result[ind]
		messages = ("-"*30,
			"Ticket number: {0}".format(row[0]),
			"-"*30,
			"Violation date: {0}".format(row[1]),
			"Violation description: {0}".format(row[2]),
			"Fine: {0}".format(row[3]),
			"Registration number: {0}".format(row[4]),
			"Vehicle make: {0}".format(row[5]),
			"Vehicle model: {0}".format(row[6]),
			"-"*30,
			"")
		display_messages(messages)
		ind += 1
	
	transition_screen()


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

def new_screen(title):
	screen_len = 30

	clear_screen()
	print("-"*screen_len)
	print(title)
	print("-"*screen_len)

def transition_screen():
	input("Press enter to go back to the menu.")
	clear_screen()

def clear_screen():
	os.system('cls' if os.name=='nt' else 'clear')

def display_messages(list_of_messages):
	for item in list_of_messages:
		print(item)

def issue_ticket():
	global connection, cursor
	
	regno = input("Please enter registration number: ")
	
	query = ''' SELECT * FROM registrations r, vehicles v
				WHERE r.regno=? AND r.vin=v.vin '''

	cursor.execute(query, (regno,))
	driver = cursor.fetchone()

	if driver == None:
		print("No matching registration number, taking you back to main menu.")
		time.sleep(2)
		return

	print(driver[5],driver[6],driver[8],driver[9],driver[10],driver[11])

	vdate = input('Violation Date (YYYY-MM-DD): ')
	text = input('Violation Text: ')
	amt = input('Fine Amount: ')

	if vdate == "":
		vdate = str(date.today())

	tno = generate_tno()

	cursor.execute('INSERT INTO tickets(tno,regno,fine, violation,vdate) VALUES (?,?,?,?,?);', 
		(tno, regno, amt, text,vdate))
	connection.commit()

	print("Ticket issued! Now taking you back to the main menu.")
	time.sleep(2)


# For use with issue_ticket(): Generates a unique tno that is greater than any other tno.
def generate_tno():
	global connection, cursor

	#query = '''SELECT tno+1 from tickets where tno != (select max(tno) from tickets)
	query = ''' SELECT max(tno)+1 FROM tickets '''
	cursor.execute(query)
	return cursor.fetchone()[0]


def find_owner():
	global connection, cursor

	while(True):
		os.system('cls' if os.name=='nt' else 'clear')
		print("Find car owner by providing: ")
		make = input("Make: ")
		model = input("Model: ")
		year = input("Year: ")
		color = input("Color: ")
		plate = input("Plate: ")

		if make=="" and model=="" and year=="" and color=="" and plate=="":
			print("Please enter at least One Piece of driver information.")
			time.sleep(2)
			continue
		else:
			break


	result = []
	query = ''' SELECT * FROM registrations r, vehicles v
				WHERE r.vin=v.vin '''
	cursor.execute(query)
	result = cursor.fetchall()
	

	if make != "":
		make1 = []
		query = ''' SELECT * FROM registrations r, vehicles v
					WHERE v.make LIKE ? AND r.vin=v.vin '''

		cursor.execute(query, (make,))
		make1 = cursor.fetchall()
		result = list(set(result) & set(make1))
	if model != "":
		model1 = []
		query = ''' SELECT * FROM registrations r, vehicles v
					WHERE v.model LIKE ? AND r.vin=v.vin '''

		cursor.execute(query, (model,))
		model1 = cursor.fetchall()
		result = list(set(result) & set(model1))
	if year != "":
		year1 = []
		query = ''' SELECT * FROM registrations r, vehicles v
					WHERE v.year=? AND r.vin=v.vin '''

		cursor.execute(query, (year,))
		year1 = cursor.fetchall()
		result = list(set(result) & set(year1))
	if color != "":
		color1 = []
		query = ''' SELECT * FROM registrations r, vehicles v
					WHERE v.color LIKE ? AND r.vin=v.vin '''

		cursor.execute(query, (color,))
		color1 = cursor.fetchall()
		result = list(set(result) & set(color1))
	if plate != "":
		plate1 = []
		query = ''' SELECT * FROM registrations r, vehicles v
					WHERE r.plate LIKE ? AND r.vin=v.vin '''

		cursor.execute(query, (plate,))
		plate1 = cursor.fetchall()
		result = list(set(result) & set(plate1))
	

	i = 0;
	a = len(result)
	if a == 0:
		print("No matching drivers, taking you back to main menu.")
		time.sleep(2)
		return
	elif a < 4:
		os.system('cls' if os.name=='nt' else 'clear')
		print("Owner search results: ")
		print("|Make|Model|Year|Color|Plate #|Reg Date|Expiry Date|Name|")
		while i < 1:
			for r in result:
				print(r[8],r[9],r[10],r[11],r[3],r[1],r[2],r[5],r[6])
			i += 1
		while(True):
			e = input("[e] Back to menu: ")
			if e == 'e' or e == 'E':
				return
	else:                       # Else if there are more than 3 results.
		while i < 1:            # Print results
			os.system('cls' if os.name=='nt' else 'clear')
			print("Owner search results: ")
			print("|Make|Model|Year|Color|Plate #|Reg Date|Expiry Date|Name|")
			j = 1
			for r in result:
				print("[%d] %s %s %s %s %s" % (j, r[8],r[9],r[10],r[11],r[3]))
				j += 1
			i += 1
			print("[e] Back to menu ")
		
		while(True):            # Select result
			action = input("Action: ")
			
			if action == 'e' or action == 'E':
				return
			
			action = int(action)-1
			
			if action <= a:
				j = 0;
				for i in result:
					if j < action:
						j += 1
						continue
					print(i[8],i[9],i[10],i[11],i[3],i[1],i[2],i[5],i[6])
					break
				while (True):
					action = input("[e] Back to menu: ")
					if action == 'e' or action =='E':
						return

def main():
	
	path = "./a3.db"
	defaultPath = path

	connect(path)

	login_screen()
	close_connection()

	return


if __name__ == "__main__":
	main()
