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


def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet, collecting the last
    5 entries for each sandwich and returns the data as a list of lists.
    """
    sales = SHEET.worksheet("sales")
    # column = sales.col_values(3) # We're using the col_values() method by gspread (Python API for Google Sheets)
    # print(column)

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:]) # Collects the last 5 entries for each sandwich
    
    return columns


def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10% 
    """
    print("Calculating stock data...\n")
    new_stock_data = []

    for column in data: 
        int_column = [int(num) for num in column] # We are converting our values into integers
        average = sum(int_column) / len(int_column) # This expression would also work sum(int_column)/5 as we know our stock will always have 5 items
        stock_num = average * 1.1 # This will add 10% to the average
        new_stock_data.append(round(stock_num))
        
    return new_stock_data

def main():
    """
    Run all program functionsm
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales") # We need to call our function and pass it our sales_data list
    new_surplus_data = calculate_surplus_data(sales_data) # Calculates our surplus data and returns it to the new surplus data variable
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")


print("Welcome to Love Sandwiches Data Automation\n")
main() # Handy way to test an individual function - by commenting out the main() function for it not to run at the same time

# stock - sales = surplus
# These are methods from the gspread library