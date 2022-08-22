# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
# stock = surplus - actual sales 

import gspread  # Python API for Google Sheets
from google.oauth2.service_account import Credentials   # imports credentials from Google
from pprint import pprint

# scope lists the APIs that a programm access to run
# SCOPE in capital is a constant
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """ 
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers separated
    by commas. The loop will repeatedly request data, until it is valid. 
    """
    # adding a while loop so that we are not needing to run the programm manually all the time
    # and it will stop once the required parametres are satisfied (6 integers numbers)
    while True:

        print("Please enter sales data from the last marlet.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")           # \n will add a row here

        data_str = input("Enter your data here: ")
        #split method returns the broken up values as a list
        sales_data = data_str.split(",")
        

        if validate_data(sales_data):
            print("Data is valid!")
            break
    
    return sales_data


def validate_data(values):
    """ 
    Inside the try, converts all strings values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values
    """

    try:
        # convert into integer for every value in values
        [int(value) for value in values]  
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True    


def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided
    """
    print("Updating sales worksheet...\n")
    
    # getting into the sales tab in the worksheet
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()    #  this method is from gspread
    # pprint(stock)                                      #  we need to install this pprint so the data is easy to read when printed to the terminal
    stock_row = stock[-1]                                #  reminding that -1 means the last value of a list
    #print(f"stock row: {stock_row}")
    #print(f"sales row: {sales_row}")

    
    surplus_data = []                                   # define an empty list
    for stock, sales in zip(stock_row, sales_row):     # this zip will automatically interate between the two lists (stock_row and sales_row)
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    print(new_surplus_data)

print("Welcome to love Sandwiches Data Automation\n")
main()