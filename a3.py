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
	pass
def register_marriage():
	pass
def renew_registration():
	pass
def process_BOS():
	pass

def process_payment():
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
