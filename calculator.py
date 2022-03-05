from datetime import date
 
transaction_data = {
    "transaction_type": "",
    "amount": float(),
    "date": ""
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
    valid_no = ["no", "n"]
    confirm = input("Do you confirm the recording of this entry? (y/n)")
   
    if confirm in valid_yes:
        return confirm in valid_yes
    elif confirm in valid_no:
        return confirm in valid_yes
    else:
        get_confirmation()
       
 
def main():
    income, expense = get_transaction_type()
    get_source_reason(income, expense)
    get_amount()
    get_date()
    confirm = get_confirmation()
    # TODO: put transaction_data into database
    print(transaction_data)
 
main()
