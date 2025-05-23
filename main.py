#!/usr/bin/env python
# coding: utf-8

# # Code-Ky - AI Jan 2025 - Week 8 Python Project

# # Questions
# * What is the 'Transfer' transaction type?

# ## Load Transactions

# In[ ]:


# open and read financial_transactions.csv into a list of dictionaries
# and print the first 5 rows 
import sys
import csv
from datetime import datetime
from decimal import Decimal, DecimalException

# Parse date with datetime.strptime
# Make amount negative for 'debit'
# Create dictionary with all fields
# Add to transactions
# Catch FileNotFoundError, ValueError

def tab(x=1): 
    return "   " * x

def log(msg): 
    print(msg)
    # append to log.txt file
    try: 
        with open('log.txt', 'a') as f:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{current_time} - {msg}\n")
    except Exception as e:
        print(f"ERROR: Error writing to log file: {e}")
        sys.exit(1)

print();
print ("INFO: Starting to read financial_transactions.csv")
transactions = []   # Global so I can use it elsewhere as well
try: 
    with open('financial_transactions.csv', mode='r') as file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(file)

        # create a set to check for duplicates
        Unique_ID = set()
        # Track id Numbers
        id_number = 0
        # Track input Row Numbers
        row_number = 0
        # Read all the rows into a list of dictionaries
        for row in csv_reader:
            row_number += 1

            # Convert date to datetime object
            try: 
                row['date'] = datetime.strptime(row['date'],"%Y-%m-%d")
            except ValueError as e:
                log(f"WARNING: Error parsing date: {e}\n{tab()}Row[{row_number}]: {row}")
                continue

            # Debit or Credit
            try: 
                if row['type'] == 'debit':
                    # Convert amount to negative decimal
                    row['amount'] = -Decimal(row['amount'])
                else:
                    # Convert amount to positive decimal
                    row['amount'] = Decimal(row['amount'])
            except DecimalException as e:
                log(f"WARNING: Error parsing amount: {e}\n{tab()}Row[{row_number}]: {row}")
                continue

            # Convert ID to Integer
            try: 
                row['transaction_id'] = int(row['transaction_id'])
            except ValueError as e:
                log(f"WARNING: Error parsing ID: {e}\n{tab()}Row[{row_number}]: {row}")
                continue
            # check id is sequential 
            if row['transaction_id'] <= id_number:
                log(f"WARNING: ID is not sequential: {row['transaction_id']}\n{tab()}Row[{row_number}]: {row}")
                continue
            else :
                id_number = row['transaction_id']
            # Check for duplicate ID
            if row['transaction_id'] in Unique_ID:
                log(f"WARNING: Duplicate ID found: {row['transaction_id']}\n{tab()}Row[{row_number}]: {row}")
                continue
            else:
                Unique_ID.add(row['transaction_id'])
            transactions.append(row)

        # Print the first 5 rows    
        if True:
            print("INFO:")
            print(f"{tab()}Number of transactions: {len(transactions)}")

            print(f"{tab()}First 5 transactions:")
            for i in range(5):
                print(tab(2), transactions[i])


except FileNotFoundError:
    print("The file 'financial_transactions.csv' was not found.")
    sys.exit(1)

except ValueError as e:
    print(f"Value error: {e}")
    sys.exit(1)

except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)



# ## View Transactions

# In[ ]:


import textwrap
def view_transaction_table(transactions, max_lines=10, type=None):
    """
    View transactions in a table format.
    """
    # track lines and max lines
    count = 0
    header_length = 82

    print_transaction_header()
    for transaction in transactions:
        if type and transaction['type'] != type:
            continue
        print_transaction_row(transaction)
        count += 1
        if max_lines and count >= max_lines:
            ## print_transaction_footer()
            message = f"... Truncating Data to {max_lines} matching lines ..."
            print(f"{message: ^{header_length}}")
            print_transaction_row(transactions[-1])
            break
    print_transaction_footer()


# Use ODD-Length separator or things will get wonky.
def print_transaction_row(transaction, fill= ' ', separator=' | '):
    left = separator[1:]
    right = separator[:-1]

    ## special handling so we can pass a string or date.
    try: 
        date = transaction['date'].strftime('%b %d, %Y')
    except AttributeError:
        date = transaction['date']

    print(f"{left}{transaction['transaction_id']:{fill}<6}{separator}{date:{fill}<12}" +
          f"{separator}{transaction['customer_id']:{fill}<8}{separator}{transaction['amount']:{fill}<8}{separator}{transaction['type']:{fill}<8}" + 
          f"{separator}{textwrap.shorten(transaction['description'],24, placeholder=' ...'):{fill}<24}{right}")

def print_transaction_header():
    ## create a transaction named header
    top = {
        'transaction_id': '-',
        'date': '-',
        'customer_id': '-',
        'amount': '-',
        'type': '-',
        'description': '-'
    }
    labels = {
        'transaction_id': 'ID',
        'date': 'Date',
        'customer_id': 'Customer',
        'amount': 'Amount',
        'type': 'Type',
        'description': 'Description'
    }
    footer = { 
        'transaction_id': '-',
        'date': '-',
        'customer_id': '-',
        'amount': '-',
        'type': '-',
        'description': '-'
    }
    print_transaction_row(top, fill='-', separator='-.-')
    print_transaction_row(labels, fill=' ', separator=' | ')    
    print_transaction_row(footer, fill='-', separator='-|-')

def print_transaction_footer():
    footer = {
        'transaction_id': '-',
        'date': '-',
        'customer_id': '-',
        'amount': '-',
        'type': '-',
        'description': '-'
    }
    print_transaction_row(footer, fill='-', separator='-^-')


if __name__ == "__main__":
    # Example usage
    print()
    view_transaction_table(transactions)
    # Add more functionality as needed
    # e.g., filter by transaction_id, date, amount, type


# # CLI Input Validation

# In[ ]:


## input_int
def input_int(prompt, default=None):
    while True:
        try:
            value = input(prompt)
            if not value and default is not None:
                return default
            return int(value)
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

## input_datetime YYYY-MM-DD
def input_date(prompt, default=None):
    while True:
        try:
            value = input(prompt)
            if not value and default is not None:
                return default
            return datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            print("Invalid input. Please enter a valid date in YYYY-MM-DD format.")

## input_decimal
def input_decimal(prompt, default=None):
    while True:
        try:
            value = input(prompt)
            if not value and default is not None:
                return default
            return Decimal(value)
        except (ValueError, DecimalException):
            print("Invalid input. Please enter a valid decimal number.")

## input string from selected list of words. Title Case
def input_option(prompt, options):

    while True:
        value = input(f"{prompt}{', '.join(options)}: ").strip().lower()

        matches = [k for k in options if value in k.lower()]

        if len(matches) == 1:
            value = matches[0]
            return value
        elif len(matches) > 1:
            print(f"Ambiguous Input: {', '.join(matches)}")
            continue
        else :
            print(f"Invalid Input.")
            continue




# # Transaction Validation
# 

# In[ ]:


def validate_transaction_id(transaction_id):
    """
    Validate transaction ID.
    """
    last_id = transactions[-1]['transaction_id'] if transactions else 0
    if not isinstance(transaction_id, int):
        log("ERROR: Transaction ID must be an integer.")
        return False
    if transaction_id <= 0:
        log("ERROR: Transaction ID must be a positive integer.")
        return False
    if transaction_id in Unique_ID:
        log("ERROR: Transaction ID already exists.")
        return False
    if transaction_id <= last_id:
        log(f"ERROR: Transaction ID must be greater than the last ID [{last_id}].")
        return False
    return True


# ## Add Transaction CLI

# In[ ]:


def add_transaction(id, date, customer_id, amount, type, description):
    transaction = {
        'transaction_id': id,
        'date': date,
        'customer_id': customer_id,
        'amount': amount,
        'type': type,
        'description': description
    }
    transactions.append(transaction)
    Unique_ID.add(id)
    return transaction

def add_transaction_cli():

    last_id = transactions[-1]['transaction_id'] if transactions else 0
    while True:
        transaction_id = int(input_int(f"Enter transaction ID[{last_id+1}]: "))
        if validate_transaction_id(transaction_id): break


    date = input_date(f"Enter transaction date (YYYY-MM-DD): ")
    customer_id = input_int("Enter customer ID: ")
    amount = input_decimal("Enter transaction amount: ")
    type = input_option("Enter transaction type: ", ['Credit', 'Debit', 'Transfer'])
    description = input("Enter transaction description: ") 

    transaction = add_transaction(transaction_id, date, customer_id, amount, type, description)
    log(f"INFO: Added transaction: {transaction}")
    return transaction



# ## CLI Setup
# 

# In[ ]:


import sys

CLI_EXIT = False
def exit_cli():
    global CLI_EXIT
    CLI_EXIT = True
    print("Exiting CLI...")

 # Create a dictionary of Actions and Functions
actions = {
    'ADd':      add_transaction_cli,
    'CLs':      lambda: os.system('cls'), # clear the screen
    'deLete':   'delete_transaction',
    'Update':   'update_transaction',
    'vieW':     lambda: view_transaction_table(transactions),
    'Save':     'save_transactions',
    }

# sort the actions alaphabetically lowercase
actions = dict(sorted(actions.items()))
# add an entry to dictionary for exit
actions['Exit'] = exit_cli




# ## CLI Loop
# 

# In[ ]:


print()
while CLI_EXIT == False:
    # Ask user for input
    print()
    print("-= Hornet Financial Calculator (Alpha) =-")
    action = input_option(f"Action: ",list(actions.keys()))

    if action in actions:
        # if the action is a function, call it
        if callable(actions[action]):
            actions[action]()
        else:
            print(f"Action '{action}' is not callable or has not been implemented.")
    else:
        print(f"Invalid action: {action}")
        continue    

