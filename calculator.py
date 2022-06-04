from datetime import date
import sqlite3
from time import sleep
 
connection = None
cursor = None
 
transaction_data = {
    "transaction_type": "",
    "amount": float(),
    "date": "",
}
 
def get_transaction_type():
    valid_income_transaction = ["i", "income",  "inc",  "+"]
    valid_expense_transaction = ["e", "expense","exp", "-"]
    # input either income or expense
    transaction_type = input("Income or Expense? Input one of: " + " ".join(valid_income_transaction) + " or " + " ".join(valid_expense_transaction) + "\n")
   
    # validate
    income = False
    expense = False
    if transaction_type in valid_income_transaction:
        transaction_data.update({"transaction_type": "income"})
        income = True
    elif transaction_type in valid_expense_transaction:
        transaction_data.update({"transaction_type": "expense"})
        expense = True
    else:
        income, expense = get_transaction_type()
    return income, expense
 
def get_source_reason(income, expense):
    if income:
        source = input("Source of income? ")
        if len(source):
            transaction_data.update({"source": source})
        else:
            get_source_reason(income, expense)
 
    elif expense:
        reason = input("Reason for expense? ")
        if len(reason):
            transaction_data.update({"reason": reason})
        else:
            get_source_reason(income, expense)
 
def get_amount():
    # make sure it's an integer or float
    amount = input("Transaction amount in dollars: ")
    try:
        amount = float(amount)
        transaction_data.update({"amount": amount})
    except ValueError:
        get_amount()
 
def get_date():
    today = date.today()
 
    transaction_date = input("Date of transaction as dd/mm/yyyy? (Hit enter to default to today's date) ")
    if not len(transaction_date):
        transaction_data.update({"date": today.strftime("%d/%m/%Y")})
        return
    day, month, year = transaction_date.split("/")
 
    # validate
    try:
        year = int(year)
        month = int(month)
        day = int(day)
        transaction_date = date(year, month, day)
    except ValueError:
        get_date()
   
    if transaction_date <= today:
        transaction_data.update({"date": transaction_date.strftime("%d/%m/%Y")})
 
def get_confirmation():
    valid_yes = ["yes", "y"]
 
    confirm = input("Do you confirm the recording of the above entry? (y/n)").replace("\n", "").replace(" ", "")
   
    return confirm in valid_yes

def tables_exist():
    global connection, cursor
    # check if the tables already exist in the db
    cursor.execute("""SELECT count(*) FROM sqlite_master WHERE type='table' AND (name='income' OR name='expenses');""")
    tables = cursor.fetchone()[0]
 
    return tables == 2

def create_tables():
    global connection, cursor
 
    if not tables_exist():
        cursor.execute("""CREATE TABLE IF NOT EXISTS income (source varchar, amount float, date varchar)""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS expenses (reason varchar, amount float, date varchar)""")
        connection.commit()
 
        # check that everything is as it should be
        cursor.execute(""" SELECT * FROM income; """)
        income = cursor.fetchall()
        cursor.execute(""" SELECT * FROM expenses; """)
        expenses = cursor.fetchall()
        assert len(income) == 0
        assert len(expenses) == 0
        assert tables_exist() == True
 
def connect(path):
    global connection, cursor
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
 
    # this only commits the cursor.execute directly before it
    # you don't need to commit select queries
    # but you should be commiting create and insert and update and replace queries
    # that you expect to change the databse
    connection.commit()
 
def income_insertion():
    global connection, cursor
 
    cursor.execute("""SELECT count(*) FROM income;""")
    before = cursor.fetchone()[0]
 
    income = (transaction_data["source"], transaction_data["amount"], transaction_data["date"])
    cursor.execute("""INSERT INTO income (source, amount, date) VALUES (?, ?, ?);""", income)
    connection.commit()
 
    cursor.execute(""" SELECT count(*) FROM income; """)
    after = cursor.fetchone()[0]
   
    assert (after > before)
   
    cursor.execute("""SELECT * FROM income WHERE source = ? AND amount = ? AND date = ?;""", income)
    toPrintIncome = cursor.fetchall()[0]
    cursor.execute("""SELECT * FROM income""")
    print(cursor.fetchall())
 
    print("Successfully added new income: " + str(toPrintIncome))
   
    connection.commit()
 
def expenses_insertion():
    global connection, cursor
 
    cursor.execute("""SELECT count(*) FROM expenses;""")
    before = cursor.fetchone()[0]
 
    expenses = (transaction_data["reason"], transaction_data["amount"], transaction_data["date"])
    cursor.execute("""INSERT INTO expenses (reason, amount, date) VALUES (?, ?, ?);""", expenses)
    connection.commit()
 
    cursor.execute("""SELECT count(*) FROM expenses;""")
 
    after = cursor.fetchone()[0]
    assert (after > before)
 
    cursor.execute("""SELECT * FROM expenses WHERE reason = ? AND amount = ? AND date = ?;""", expenses)
    toPrintExpense = cursor.fetchall()[0]
 
    print("Successfully added new expense: " + str(toPrintExpense))
 
    connection.commit()

def get_total_income():
    # sums up total income from database
    global connection, cursor
    cursor.execute("""SELECT SUM(amount) FROM income;""")
    total_income = cursor.fetchall()[0][0]
    if total_income:
        print("Your Total Income: $" + str(total_income))
    else:
        print("No income yet!")
    sleep(2.5) # allow time to read the above
    return total_income
 
def get_total_expenses():
    # sums up total expenses from database
    global connection, cursor
    cursor.execute("""SELECT SUM(amount) FROM expenses;""")
    total_expenses = cursor.fetchall()[0][0]
    if total_expenses:
        print("Your Total Expenses: $" + str(total_expenses))
    else:
        print("No expenses yet!")
    sleep(2.5) # allow time to read the above
    return total_expenses

def get_networth():
    income = get_total_income()
    expenses = get_total_expenses()
    if income and expenses:
        print("Your networth: $" + str(income-expenses))
    elif income and not expenses:
        print("Your networth: $" + str(income))
    elif not income and expenses:
        print("Your networth: -$" + str(expenses))
    else:
        print("You don't have any income or expenses recorded yet! Please record some first!")
    
    sleep(2.5) # allow time to read the above

def get_income_by_source():
    global connection, cursor
    cursor.execute("""SELECT SUM(amount), source FROM income GROUP BY source;""")
    income_list = cursor.fetchall()
    for i in income_list:
        amount = i[0]
        source = i[1]
        print("Total Amount: " + str(amount) + " | Source: " + str(source))

    sleep(2.5) # allow time to read the above

def get_expenses_by_reason():
    global connection, cursor
    cursor.execute("""SELECT SUM(amount), reason FROM expenses GROUP BY reason;""")
    expenses_list = cursor.fetchall()
    for i in expenses_list:
        amount = i[0]
        reason = i[1]
        print("Total Amount: " + str(amount) + " | Reason: " + str(reason))

    sleep(2.5) # allow time to read the above

def by_month():
	global connection, cursor
	by_month = {}
	cursor.execute("""SELECT SUBSTR(date,4,2) as month, SUM(amount) FROM income GROUP BY month;""")
	income_by_month = cursor.fetchall()
	print("Income Breakdown by Month")
	for i in income_by_month:
		month = i[0]
		amount = i[1]
		by_month[month] = amount
		print("Month: " + str(month) + " Total Income: $" + str(amount))

	sleep(2.5) # allow time to read the above

	more = input("See further income breakdown by source? (y/n)\n")
	if more == "y":
		by_source = {}
		cursor.execute("""SELECT SUBSTR(date,4,2) as month, source, SUM(amount) FROM income GROUP BY month, source;""")
		income_by_month_source = cursor.fetchall()
		for s in income_by_month_source:
			month = s[0]
			source = s[1]
			amount = s[2]
			if month in by_source.keys():
				if source in by_source[month].keys():
					by_source[month][source] = by_source[month][source] + amount
				else:
					by_source[month][source] = amount
			else:
				by_source[month] = {source: amount}
		
		for m in by_source:
			print("Month: " + str(m))
			for s in by_source[m]:
				print("Source: " + str(s) + " Total Income: " + str(by_source[m][s]))

	sleep(2.5) # allow time to read the above

	cursor.execute("""SELECT SUBSTR(date,4,2) as month, SUM(amount) FROM expenses GROUP BY month;""")
	expenses_by_month = cursor.fetchall()
	print("Expenses Breakdown by Month")
	for e in expenses_by_month:
		month = e[0]
		amount = e[1]
		if month in by_month.keys():
			by_month[month] = by_month[month] - amount
		else:
			by_month[month] = 0-amount
		print("Month: " + str(month) + " Total Expenses: $" + str(amount))

	sleep(2.5) # allow time to read the above

	more = input("See further expenses breakdown by reason? (y/n)\n")
	if more == "y":
		by_reason = {}
		cursor.execute("""SELECT SUBSTR(date,4,2) as month, reason, SUM(amount) FROM expenses GROUP BY month, reason;""")
		expenses_by_month_reason = cursor.fetchall()
		for r in expenses_by_month_reason:
			month = r[0]
			reason = r[1]
			amount = r[2]
			if month in by_reason.keys():
				if reason in by_reason[month].keys():
					by_reason[month][reason] = by_reason[month][reason] + amount
				else:
					by_reason[month][reason] = amount
			else:
				by_reason[month] = {reason: amount}
		
		for m in by_reason:
			print("Month: " + str(m))
			for r in by_reason[m]:
				print("Reason: " + str(r) + " Total Expenses: " + str(by_reason[m][r]))
				
	sleep(2.5) # allow time to read the above

	for m in by_month:
		print("Month: " + str(m) + " Networth: $" + str(by_month[m]))

	sleep(2.5) # allow time to read the above

def by_year():
	global connection, cursor
	by_month = {}
	cursor.execute("""SELECT SUBSTR(date,7,4) as year, SUM(amount) FROM income GROUP BY year;""")
	income_by_month = cursor.fetchall()
	print("Income Breakdown by Year")
	for i in income_by_month:
		month = i[0]
		amount = i[1]
		by_month[month] = amount
		print("Year: " + str(month) + " Total Income: $" + str(amount))

	sleep(2.5) # allow time to read the above

	more = input("See further income breakdown by source? (y/n)\n")
	if more == "y":
		by_source = {}
		cursor.execute("""SELECT SUBSTR(date,7,4) as year, source, SUM(amount) FROM income GROUP BY year, source;""")
		income_by_month_source = cursor.fetchall()
		for s in income_by_month_source:
			month = s[0]
			source = s[1]
			amount = s[2]
			if month in by_source.keys():
				if source in by_source[month].keys():
					by_source[month][source] = by_source[month][source] + amount
				else:
					by_source[month][source] = amount
			else:
				by_source[month] = {source: amount}
		
		for m in by_source:
			print("Year: " + str(m))
			for s in by_source[m]:
				print("Source: " + str(s) + " Total Income: " + str(by_source[m][s]))

	sleep(2.5) # allow time to read the above

	cursor.execute("""SELECT SUBSTR(date,7,4) as year, SUM(amount) FROM expenses GROUP BY year;""")
	expenses_by_month = cursor.fetchall()
	print("Expenses Breakdown by Year")
	for e in expenses_by_month:
		month = e[0]
		amount = e[1]
		if month in by_month.keys():
			by_month[month] = by_month[month] - amount
		else:
			by_month[month] = 0-amount
		print("Year: " + str(month) + " Total Expenses: $" + str(amount))

	sleep(2.5) # allow time to read the above

	more = input("See further expenses breakdown by reason? (y/n)\n")
	if more == "y":
		by_reason = {}
		cursor.execute("""SELECT SUBSTR(date,7,4) as year, reason, SUM(amount) FROM expenses GROUP BY year, reason;""")
		expenses_by_month_reason = cursor.fetchall()
		for r in expenses_by_month_reason:
			month = r[0]
			reason = r[1]
			amount = r[2]
			if month in by_reason.keys():
				if reason in by_reason[month].keys():
					by_reason[month][reason] = by_reason[month][reason] + amount
				else:
					by_reason[month][reason] = amount
			else:
				by_reason[month] = {reason: amount}
		
		for m in by_reason:
			print("Year: " + str(m))
			for r in by_reason[m]:
				print("Reason: " + str(r) + " Total Expenses: " + str(by_reason[m][r]))
				
	sleep(2.5) # allow time to read the above

	for m in by_month:
		print("Year: " + str(m) + " Networth: $" + str(by_month[m]))

	sleep(2.5) # allow time to read the above

def breakdown_by_month_or_year():
    month_or_year = input("See breakdown by 1) month or 2) year?\n")
    if month_or_year == "1":
    	by_month()
    elif month_or_year == "2":
    	by_year()

def processTransaction():
    # database init
    create_tables()
    # user input
    income, expense = get_transaction_type()
    get_source_reason(income, expense)
    get_amount()
    get_date()
 
    # confirm entry
    print(transaction_data)
    confirm = get_confirmation()
 
    if confirm:
        if income:
            # put to income table
            income_insertion()
        elif expense:
            expenses_insertion()
    else:
        print("Transaction cancelled, data not saved.")

    sleep(2.5) # allow time to read any closing messages

    main()

def show_all_income():
    global connection, cursor

    cursor.execute("""SELECT * FROM income;""")
    entries = cursor.fetchall()
    print("Income: ")
    for i in entries:
        source = i[0]
        amount = i[1]
        date = i[2]
        print("Source: " + source, "Amount: " + str(amount), "Date: " + date)

def show_all_expenses():
    global connection, cursor

    cursor.execute("""SELECT * FROM expenses;""")
    entries = cursor.fetchall()
    for i in entries:
        reason = i[0]
        amount = i[1]
        date = i[2]
        print("Reason: " + reason, "Amount: " + str(amount), "Date: " + date)

def main():
    global connection, cursor
    connect("./income_and_expense.db")

    request = input("Do you want to see your #1 existing income and expenses or #2 input new income or expenses? (1 or 2) \nClick any other key to quit.\n")
 
    if request == "1":
        if not tables_exist():
            print("You don't have any income or expenses recorded yet! Please record some first!")
            sleep(2.5) # allow time to read the message
            main()
 
        # show income
        show_all_income()
        get_total_income()
       
        # show expenses
        show_all_expenses()
        get_total_expenses()

        specifics = input("Do you want to see #1 your networth, #2 income by source, #3 expenses by reason, #4 breakdown by month/year?\n")

        if specifics == "1":
            get_networth()
        elif specifics == "2":
            get_income_by_source()
        elif specifics == "3":
            get_expenses_by_reason()
        elif specifics == "4":
            breakdown_by_month_or_year()

        main()
   
    elif request == "2":
        processTransaction()
   
    else:
        connection.close()
        exit()
 
main()
