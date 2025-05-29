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
print("INFO: Starting to read financial_transactions.csv")
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

        # lines.append the first 5 rows    
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

# In[252]:


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
            break
    for transaction in transactions[-3:]:
        print_transaction_row(transaction)
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

# In[253]:


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
def input_option(prompt, options, default=None):

    while True:
        value = input(f"{prompt}{', '.join(options)}: ").strip().lower()

        if value.strip() == '' and default is not None:
            return default

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

def input_default(prompt, default=None):
    value = input(prompt)
    if not value and default is not None:
        return default
    return value.strip()  # Remove leading/trailing whitespace



# # Transaction Validation
# 

# In[254]:


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

def validate_type_amount(transaction):
    if transaction['type'].lower() == 'credit':
        transaction['amount'] = abs(transaction['amount'])
    elif transaction['type'].lower() == 'debit':
        transaction['amount'] = -abs(transaction['amount']) 
    elif transaction['type'].lower() == 'transfer':
        transaction['amount'] = abs(transaction['amount'])


# In[ ]:





# ## Add Transaction CLI

# In[255]:


def create_transaction(id, date, customer_id, amount, type, description):
    transaction = {
        'transaction_id': id,
        'date': date,
        'customer_id': customer_id,
        'amount': amount,
        'type': type,
        'description': description
    }
    return transaction

def add_transaction(transaction):
    transactions.append(transaction)
    Unique_ID.add(id)
    return transaction

def add_transaction_cli():

    last_id = transactions[-1]['transaction_id'] if transactions else 0
    last_customer_id = transactions[-1]['customer_id'] if transactions else 0
    last_type = transactions[-1]['type'] if transactions else 'Credit'
    while True:
        transaction_id = int(input_int(f"Enter transaction ID[{last_id+1}]: ", default=last_id + 1))
        if validate_transaction_id(transaction_id): break


    default_date = datetime.now().strftime("%Y-%m-%d")
    date = input_date(f"Enter transaction date [{default_date}]: ", default=default_date)
    customer_id = input_int(f"Enter customer ID [{last_customer_id}]: ", default=last_customer_id)
    amount = input_decimal("Enter transaction amount $[0.00]: ", default=0.00)
    type = input_option("Enter transaction type: ", ['Credit', 'Debit', 'Transfer'], default=last_type)
    description = input_default("Enter transaction description: ", default="No description provided.") 

    transaction = create_transaction(transaction_id, date, customer_id, amount, type, description)
    print_transaction_row(transaction)
    confirm = input_option("Confirm transaction? (yes/no): ", ['yes', 'no'], default='yes')
    if confirm.lower() != 'yes':
        log("INFO: Transaction not added.")
        return None     
    log(f"INFO: Added transaction: {transaction}")
    return transaction



# ## View Menu

# In[256]:


def cli_view_menu():
    view_option = input_option("View transactions by type: ", ['Credit', 'Debit', 'Transfer', 'All'])
    print(f"INFO: Viewing transactions of type: {view_option}")
    if view_option == 'All':
        view_transaction_table(transactions)
    else:
        filtered_transactions = [t for t in transactions if t['type'].lower() == view_option.lower()]
        view_transaction_table(filtered_transactions)


# ## Update Delete

# In[257]:


def cli_update_delete_menu():
    view_transaction_table(transactions)
    transaction_id = input_int("Enter transaction ID to update/delete: ")
    transaction = next((t for t in transactions if t['transaction_id'] == transaction_id), None)

    if not transaction:
        log(f"ERROR: Transaction ID {transaction_id} not found.")
        return

    ## deepcopy of transaction 
    import copy
    from copy import deepcopy
    original_transaction = copy.deepcopy(transaction)

    while True:
        ## concatenate the lists:  list + [ manual list of options ]
        ## titled_keys = [key.title() for key in original_keys]
        print_transaction_row(transaction)
        action = input_option("Edit: ", list(transactions[0].keys()) +['Cancel', 'Delete', 'Exit'])
        if action == 'Delete':
            print("Delete the Following Transaction:")
            print_transaction_row(transaction)
            confirm = input_option("Are you sure you want to delete this transaction? ", ['Delete', 'Cancel'])
            if confirm.lower() == 'delete':
                transaction['type'] = 'Deleted'  # Mark as deleted
                transactions.remove(transaction)
                Unique_ID.remove(transaction['transaction_id'])
                log(f"INFO: Deleted transaction ID {transaction_id}.")
                print(f"Transaction ID {transaction_id} deleted.")
            else:
                print("Deletion cancelled.")

        elif action == 'Exit':
            ## sort transactions by transaction_id
            transactions.sort(key=lambda x: x['transaction_id'])
            return

        elif action == 'Cancel':
            ## retstore the original transaction
            print("Cancelling transaction update.")
            print_transaction_row(transaction)
            if (transaction in transactions):
                print("Transaction update cancelled, no changes made.")
                log(f"INFO: Update Canceled.  Transaction ID {transaction_id}")
            else:
                print("Transaction update cancelled, transaction not found in list.")
                print("Appending original transaction.")
                transactions.append(original_transaction)
                ## sort transactions by transaction_id
                transactions.sort(key=lambda x: x['transaction_id'])
                log(f"INFO: Delete Canceled.  Transaction ID {transaction_id}")
            return

        ## transaction_id=int, date=datetime, customer_id=int, amount=Decimal, type= ['Credit', 'Debit', 'Transfer'], description=str
        elif action == 'transaction_id':
            while True:
                tmp_id = input_int(f"Enter new transaction ID (current: {transaction[action]}): ", default=transaction[action])
                if validate_transaction_id(tmp_id):
                    transaction[action] = tmp_id
                    break
        elif action == 'date':
            transaction[action] = input_date(f"Enter new date (YYYY-MM-DD, current: {transaction[action].strftime('%Y-%m-%d')}): ", default=transaction[action])
        elif action == 'customer_id':
            transaction[action] = input_int(f"Enter new customer ID (current: {transaction[action]}): ", default=transaction[action])
        elif action == 'amount':
            transaction['amount'] = input_decimal(f"Enter new amount (current: {transaction[action]}): ", default=transaction[action])
            validate_type_amount(transaction)
        elif action == 'type':
            transaction['type']= input_option(f"Enter new transaction type (current: {transaction[action]}): ", ['Credit', 'Debit', 'Transfer'])
            validate_type_amount(transaction)
        elif action == 'description':
            transaction[action] = input_default(f"Enter new description (current: {transaction[action]}): ", default=transaction[action])



        else:       
            transaction[action] = input_default(f"[FallBack] Enter new value for {action} (current: {transaction[action]}): ", default=transaction[action])                             

        log(f"INFO: Updated transaction ID: {transaction_id}, Field: {action}\n")





# ## Analyze Transactions

# In[258]:


"""
----------------------------------
Financial Summary (all):
Total Credits: $6478.39
Total Debits: $7969.68
Total Transfers: $0.00
Net Balance: $-1491.29

By Type:
    Credit: $6478.39,   xx%
    Debit: $7969.68,    xx%
    Transfer: $0.00,    xx%

Highlighted Customer: 
    Customer ID: 12345
    Credits: ##, $6478.39
    Debits: ##, $7969.68
    Transfers: ##, $0.00


Financial Summary (2022):
    ...
"""


# In[ ]:


def padded_dollars(amount, width=10):
    return f"${amount:,.2f}".rjust(width)  # Adjust the width as needed

def financial_summary(subset_of_transactions = None, title="Financial Summary"):
    lines = []
    if subset_of_transactions is None:
        subset_of_transactions = transactions

    total_credits = sum(t['amount'] for t in subset_of_transactions if t['type'].lower() == 'credit')
    total_debits = sum(t['amount'] for t in subset_of_transactions if t['type'].lower() == 'debit')
    total_transfers = sum(t['amount'] for t in subset_of_transactions if t['type'].lower() == 'transfer')
    total_abs_dollars = sum(abs(t['amount']) for t in subset_of_transactions)
    net_balance = total_credits + total_debits + total_transfers

    page_width = 50
    col1 = 16
    col2 = 16
    separator = '   '

    lines.append("-" * page_width)
    lines.append(title)
    lines.append("-" * page_width)
    lines.append(f"{'Total Credits:': <{col1}}{separator}{padded_dollars(total_credits, col2)}  {100 * total_credits / total_abs_dollars:.2f}%")
    lines.append(f"{'Total Debits:': <{col1}}{separator}{padded_dollars(total_debits, col2)}  {100 * -total_debits / total_abs_dollars:.2f}%")
    lines.append(f"{'Total Transfers:': <{col1}}{separator}{padded_dollars(total_transfers, col2)}  {100 * total_transfers / total_abs_dollars:.2f}%")
    lines.append(f"{'Net Balance:': <{col1}}{separator}{padded_dollars(net_balance, col2)}")
    lines.append("\n")

    # By Type
    lines.append("By Type:")
    lines.append(f"{'\tCredit: ': <{col1}}{separator}{padded_dollars(total_credits, col2)}  {100 * total_credits / total_abs_dollars:.2f}%")
    lines.append(f"{'\tDebit: ': <{col1}}{separator}{padded_dollars(total_debits, col2)}  {100 * -total_debits / total_abs_dollars:.2f}%") 
    lines.append(f"{'\tTransfer: ': <{col1}}{separator}{padded_dollars(total_transfers, col2)}  {100 * total_transfers / total_abs_dollars:.2f}%")
    lines.append("-" * page_width)
    lines.append("\n\n")

    return lines


# In[ ]:


def analyze_transactions():
    global transactions
    lines = []

    print("\nINFO: Analyzing transactions...")
    output = financial_summary(transactions,"Financial Summary (All Transactions)")
    print("\n".join(output))
    lines.append(output)

    subset = [t for t in transactions if t['date'].year == 2022]
    output = financial_summary(subset,"Financial Summary (2022)")
    print("\n".join(output))
    lines.append(output)

    # find the customer with the higest debit amount
    # get a unique set of customer IDs
    customer_ids = set(t['customer_id'] for t in transactions)

    # for each customer, calculate the total debits 
    highest_debit_customer = { 'customer_id': None, 'debits': Decimal(0) }
    for customer_id in customer_ids:
        selected = [t for t in transactions if t['customer_id'] == customer_id and t['type'].lower() == 'debit']
        total_debits = sum(t['amount'] for t in selected)
        ## debits are negative ... 
        if total_debits < highest_debit_customer['debits']:
            highest_debit_customer = {
                'customer_id': customer_id,
                'debits': total_debits
            }

    subset = [t for t in transactions if t['customer_id'] == highest_debit_customer['customer_id']]
    print(f"INFO: Customer with Highest Debits, ID: {highest_debit_customer}")
    ## view_transaction_table(subset, max_lines=10)
    output = financial_summary(subset, f"Financial Summary (Customer ID: {highest_debit_customer['customer_id']})")
    print("\n".join(output))
    lines.append(output)

    # write lines to analysis.txt
    try:
        with open('analysis.txt', 'w') as f:
            for line in lines:
                if isinstance(line, list):
                    f.write("\n".join(line) + "\n")
                else:
                    f.write(line + "\n")
    except Exception as e:
        log(f"ERROR: Error writing to analysis.txt: {e}")
        sys.exit(1)


    return lines


# ## CLI Setup
# 

# In[ ]:


import sys
import os

CLI_EXIT = False
def exit_cli():
    global CLI_EXIT
    CLI_EXIT = True
    print("Exiting CLI...")

 # Create a dictionary of Actions and Functions
actions = {
    'ADd':      add_transaction_cli,
    'Analyze':  analyze_transactions, # Placeholder for analyze function
    'Cls':      lambda: os.system('cls'), # clear the screen
    'EDit':     cli_update_delete_menu, 
    'vieW':     cli_view_menu, ## lambda: cli_view_menu(),
    'SAve':     'save_transactions',
    }

# sort the actions alaphabetically lowercase
actions = dict(sorted(actions.items()))
# add an entry to dictionary for exit
actions['eXit'] = exit_cli




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

