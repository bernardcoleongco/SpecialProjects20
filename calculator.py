import datetime
 
all_data = {
    "Transaction Type": "",
    "Origin or Destination": "",
    "Amount": "",
    "Date": ""
}
 
def data():
    # input either income or expense
    choose = input("Income or Expense? ")
    all_data.update({"Transaction Type": choose})
 
    # from/to, amount, date (optional)
    choose2 = input("From or where to is this money going? ")
    all_data.update({"Origin or Destination": choose2})
    if choose == "Income" or choose == "Expense":
        transactionAmount = input("How much money was involved in this transaction? ")
        all_data.update({"Amount": transactionAmount})
    else:
        print("You did not answer")
 
    transactionDate = input("When did you make this transaction? (if not applicable, type n) ")
 
    if transactionDate == "n":
        transactionDate = datetime.datetime.now()
        all_data.update({"Date": transactionDate})
 
 
def main():
    data()
    print(all_data)
 
main()
