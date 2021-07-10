import gspread # Imports the entire gspread library so that we can access any function, class, or method within it
from google.oauth2.service_account import Credentials # Imports the credentials class which is part of the service_account function from the google-auth library

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

    # while loop - these lines of code will keep running until the data provided is valid

    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10, 20, 30, 40, 50, 60\n")

        data_str = input("Enter your data here: ") # Asks the user the data
        # print(f"The data provided is {data_str}") # String value provided by users, we can remove this after testing

        sales_data = data_str.split(",") # Converts the string of data from the user into a list of values
        validate_data(sales_data)

        if validate_data(sales_data): # We use a single if statement to call our validate data function, passing it our sales_data list
            print("Data is valid!")
            break # while loop is stopped with the break keyword

    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """

    # Try statement with "f" string
    # "e" variable is standard Python shorthand for "error"
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
        )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again!\n")
        return False # We can use our 'return' value as the condition for ending our while loop
    
    return True


data = get_sales_data()