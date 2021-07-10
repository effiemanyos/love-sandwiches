import gspread # Imports the entire gspread library so that we can access any function, class, or method within it.
from google.oauth2.service_account import Credentials # Imports the credentials class which is part of the service_account function from the google-auth library.

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Variable naming convention for constant variable values that should not be changed = CAPITALIZED

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


# Function to collect sales data from our user and description of the function

def get_sales_data():
    """
    Get sales figures input from the user
    """
    print("Please enter sales data from the last market.")
    print("Data should be six numbers, separated by commas.")
    print("Example: 10, 20, 30, 40, 50, 60\n")

    data_str = input("Enter your data here: ")
    print(f"The data provided is {data_str}") # String value


get_sales_data()