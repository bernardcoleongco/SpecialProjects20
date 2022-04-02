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
    connect("./income_and_expense.db")
 
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
    connect("./income_and_expense.db")
 
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
    connect("./income_and_expense.db")
 
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
    connect("./income_and_expense.db")
    cursor.execute("""SELECT SUM(amount) FROM income;""")
    total_income = cursor.fetchall()[0][0]
    if total_income:
        print("Your Total Income: $" + str(total_income))
    else:
        print("No income yet!")
    sleep(2.5) # allow time to read the above
 
def get_total_expenses():
    # sums up total income from database
    global connection, cursor
    connect("./income_and_expense.db")
    cursor.execute("""SELECT SUM(amount) FROM expenses;""")
    total_expenses = cursor.fetchall()[0][0]
    if total_expenses:
        print("Your Total Expenses: $" + str(total_expenses))
    else:
        print("No expenses yet!")
    sleep(2.5) # allow time to read the above
 
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
 
    connection.close()

    sleep(2.5) # allow time to read any closing messages

    main()
 
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
        cursor.execute("""SELECT * FROM income;""")
        entries = cursor.fetchall()
        print("Income: ")
        for i in entries:
            source = i[0]
            amount = i[1]
            date = i[2]
            print("Source: " + source, "Amount: " + str(amount), "Date: " + date)
        get_total_income()
       
        # show expenses
        cursor.execute("""SELECT * FROM expenses;""")
        entries = cursor.fetchall()
        for i in entries:
            reason = i[0]
            amount = i[1]
            date = i[2]
            print("Reason: " + reason, "Amount: " + str(amount), "Date: " + date)
        get_total_expenses()
        main()
   
    elif request == "2":
        processTransaction()
   
    else:
        exit()
 
main()
