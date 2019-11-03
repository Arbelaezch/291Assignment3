import os
import time
import getpass
import sqlite3

connection = None
cursor = None

# I like keeping table names in string variables to minimize errors
# region Table Constants
# region Tickets
TABLE_TICKETS = "tickets"
TICKETS_TNO = "tno"
TICKETS_REGNO = "regno"
TICKETS_FINE = "fine"
TICKETS_VIOLATION = "violation"
TICKETS_VDATE = "vdate"
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
	global cursor

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
		cursor.execute("insert into persons values (?, ?, ?, ?, ?, ?);", [f_fname, f_lname, bday, place, addr, phone_no])
	cursor.execute("select max(regno) from births;")
	reg_number = cursor.fetchone()[0] + 1
	current_date = time.strftime("%Y-%m-%d")
	reg_place = "Edmonton"
	cursor.execute("insert into births values (?,?,?,?,?,?,?,?,?,?);", [str(reg_number),fname,lname,current_date,reg_place,gender,
	f_fname,f_lname,m_fname,m_lname])

def register_marriage():
	# Need to check if empty strings appear as null in SQL
	global cursor

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
	cursor.execute("select max(regno) from marriages;")
	reg_number = cursor.fetchone()[0] + 1
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
		cursor.execute("insert into persons values (?, ?, ?, ?, ?, ?);", [p2fname, p2lname, bday, place, addr, phone_no])

def renew_registration():
	global cursor
	while True:
		reg_no = input("Enter the registration number: ")
		try:
			reg_no = int(reg_no)
		except:
			print("Not a valid registration number.")
			continue
		cursor.execute("select regno, regdate from registrations where regno=?;", [reg_no])
		reg = cursor.fetchone()
		if reg != None:
			break
		else:
			print("This registration number does not exist.")
	if reg[1] <= time.strftime("%Y-%m-%d"):
		cursor.execute("select date('now', '+1 year');")
		new_expiry = cursor.fetchone()[0]
	else:
		cursor.execute("select date('?', '+1 year);", reg[1])
		new_expiry = cursor.fetchone()[0]
	cursor.execute("update registrations set expiry=? where regno=?", [new_expiry, reg_no])

def process_BOS():
	pass

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
	pass

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


def main():
	
	path = "./a3.db"
	defaultPath = path

	connect(path)

	login_screen()
	close_connection()

	return


if __name__ == "__main__":
    main()
