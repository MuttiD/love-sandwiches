# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import gspread  # Python API for Google Sheets
from google.oauth2.service_account import Credentials   # imports credentials from Google

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
    """ Get sales figures input from the user """
    print("Please enter sales data from the last marlet.")
    print("Data should be six numbers, separated by commas.")
    print("Example: 10,20,30,40,50,60\n")           # \n will add a row here

    data_str = input("Enter your data here: ")
    print(f"The data provided is {data_str}")

get_sales_data()