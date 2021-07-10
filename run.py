import gspread # Imports the entire gspread library so that we can access any function, class, or method within it
from google.oauth2.service_account import Credentials # Imports the credentials class which is part of the service_account function from the google-auth library
from pprint import pprint

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
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers separated
    by commas. The loop will repeatedly request data, until it is valid.
    """

    # while loop - these lines of code will keep running until the data provided is valid

    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10, 20, 30, 40, 50, 60\n")

        data_str = input("Enter your data here: ") # Asks the user the data
        # print(f"The data provided is {data_str}")
        # String value provided by users, we can remove this after testing

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

# Function that inserts data into our spreadsheet


def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided.
    """
    print("Updating sales worksheet...\n") # The \n adds a space between paragraphs
    sales_worksheet = SHEET.worksheet("sales") # We are using the worksheet method to acces our "sales" worksheet in the spreadsheet
    sales_worksheet.append_row(data) # The append_row method adds a new row to the end of our data in the worksheet selected
    print("Sales worksheet updated successfully!\n")


def update_surplus_worksheet(data):
    """
    Update surplus worksheet, add new row with the list data provided.
    """
    print("Updating surplus worksheet...\n")
    surplus_worksheet = SHEET.worksheet("surplus")
    surplus_worksheet.append_row(data)
    print("Surplus worksheet updated successfully!\n")


def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully!\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure substracted from the stock: 
    - Positive surplus indicates wate
    - Negative surplus inficates extra made when stock was sold out
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values() # Method to fetch all of the cells from our stock worksheet
    # pprint(stock) # We are using the pprint() method instead of the standard print() statement, so our data is easier to read when it's printed to the terminal
    # To use pprint(), I need to install it to the top of the file too
    # Results in the terminal: each nested list corresponds to a row in our stock worksheet
    stock_row = stock[-1] # To access the last list in the stock data - simpliest way to do this is by using slice - slices the final item form the list
    # print(f"stock row: {stock_row}")
    # print(f"sales row: {sales_row}")

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales 
        surplus_data.append(surplus)

    return surplus_data


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales") # We need to call our function and pass it our sales_data list
    new_surplus_data = calculate_surplus_data(sales_data) # Calculates our surplus data and returns it to the new surplus data variable
    update_worksheet(new_surplus_data, "surplus")


print("Welcome to Love Sandwiches Data Automation\n")
main()

# stock - sales = surplus
# These are methods from the gspread library