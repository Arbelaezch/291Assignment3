
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
	lifetime_ticket_count = 0
	demerit_count = 0
	lifetime_demerit_count = 0
	latest_points = 0
	lifetime_points = 0

	# count ticket lifetime
	query = """SELECT COUNT(*) FROM {r}, {t}
	WHERE {r}.{r_fname} LIKE :fname AND {r}.{r_lname} LIKE :lname AND 
		{t}.{t_regno} = {r}.{r_regno};
	""".format(r=TABLE_REGISTRATIONS, t=TABLE_TICKETS, r_fname=REGISTRATION_FNAME,
		r_lname=REGISTRATION_LNAME, t_regno=TICKETS_REGNO, r_regno=REGISTRATION_REGNO)
	cursor.execute(query, {"fname" : first_name, "lname" : last_name})
	result = cursor.fetchone()

	if result != None:
		lifetime_ticket_count = result[0]

	# count ticket latest
	query = """SELECT COUNT(*) FROM {r}, {t}
	WHERE {r}.{r_fname} LIKE :fname AND {r}.{r_lname} LIKE :lname AND 
		{t}.{t_regno} = {r}.{r_regno} AND {t}.{t_vdate} > date('now', '-2 year');
	""".format(r=TABLE_REGISTRATIONS, t=TABLE_TICKETS, r_fname=REGISTRATION_FNAME,
		r_lname=REGISTRATION_LNAME, t_regno=TICKETS_REGNO, r_regno=REGISTRATION_REGNO,
		t_vdate=TICKETS_VDATE)
	cursor.execute(query, {"fname" : first_name, "lname" : last_name})
	result = cursor.fetchone()

	if result != None:
		ticket_count = result[0]

	# count demerit points and sum of demerits (lifetime)
	query = """SELECT COUNT(*), SUM({d_points}) FROM {d}
	WHERE {d_fname} LIKE :fname AND {d_lname} LIKE :lname;
	""".format(d=TABLE_DEMERITS, d_fname=DEMERITS_FNAME, d_lname=DEMERITS_LNAME,
		d_points=DEMERITS_POINTS)
	cursor.execute(query, {"fname" : first_name, "lname" : last_name})
	result = cursor.fetchone()

	if result != None:
		lifetime_demerit_count = result[0]
		lifetime_points = result[1]
		if lifetime_points == None:
			lifetime_points = 0

	# Uses > for checking the date, excludes dates exactly 2 years earlier than now
	# latest demerit info
	query = """SELECT COUNT(*), SUM({d_points}) FROM {d}
	WHERE {d_fname} LIKE :fname AND {d_lname} LIKE :lname 
		AND {d_ddate} > date('now', '-2 year');
	""".format(d=TABLE_DEMERITS, d_fname=DEMERITS_FNAME, d_lname=DEMERITS_LNAME,
		d_points=DEMERITS_POINTS, d_ddate=DEMERITS_DDATE)
	cursor.execute(query, {"fname" : first_name, "lname" : last_name})
	result = cursor.fetchone()

	if result != None:
		demerit_count = result[0]
		latest_points = result[1]
		if latest_points == None:
			latest_points = 0
	
	messages = ("Driver abstract for {0} {1}".format(first_name, last_name),
		"-" * 30,
		"Lifetime record",
		"-" * 30,
		"Number of tickets: {0}".format(lifetime_ticket_count),
		"Number of demerit notices: {0}".format(lifetime_demerit_count),
		"Demerit points: {0}".format(lifetime_points),
		"-" * 30,
		"Latest records (within 2 years)",
		"-" * 30,
		"Number of tickets: {0}".format(ticket_count),
		"Number of demerit notices: {0}".format(demerit_count),
		"Demerit points: {0}".format(latest_points),
		"-" * 30)
	display_messages(messages)
	# endregion

	if lifetime_ticket_count == 0:
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

