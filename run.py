# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
# stock = surplus - actual sales 

import gspread  # Python API for Google Sheets
from google.oauth2.service_account import Credentials   # imports credentials from Google
# from pprint import pprint                               #  we need to install this pprint so the data is easy to read when printed to the terminal

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

        data_str = input("Enter your data here: \n")        # add a line in the input section for deployment purposes
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


def updated_worksheet(data, worksheet):
    """ 
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")


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

def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet, collecting
    the last 5 entries for each sandwich and returns the data 
    as a list of lists. 
    """
    sales = SHEET.worksheet("sales")
    #column = sales.col_values(3)
    #print(column)

    columns = []                                    # creating an empty list
    for ind in range(1, 7):
        # print(ind)
        column = sales.col_values(ind)
        columns.append(column[-5:])                 # using slice method with the last 5 numbers.  
                                                    # the colon ":" represents multiple values in the list
    # pprint(columns)

    return columns

def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)     # also will work dividing by 5
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    # print(new_stock_data)
    return new_stock_data


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    
    sales_data = [int(num) for num in data]
    updated_worksheet(sales_data, "sales")
    
    new_surplus_data = calculate_surplus_data(sales_data)
    updated_worksheet(new_surplus_data, "surplus")

    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    updated_worksheet(stock_data, "stock")
    

print("Welcome to love Sandwiches Data Automation\n")
main()
