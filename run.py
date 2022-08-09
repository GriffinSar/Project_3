import gspread 
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Sales_Program')
price = SHEET.worksheet('Price')



def renew_cal():
    if cost == data:
        print("No Uplift List Price has Been Reached")
    else: 
        final = cost * 1.07
        print(f"Your uplifted price is {final}")

def renew_info():
    """ 
    Intro page for renewal calculator. Allows the user to select
    the product and level and current renewal price. 
    """
    print("Please fill out the requested information to get your quote pricing")

    product = input("Is your product, Toad, Kace or OneIdentity?: ")
    
    level = input("Is the level of support Standard, Mid or Premier?: ")
    
    cost = float(input("What is the price of your renewal quote?: "))

    print(f"Your product is {product} the level is {level} and the price is {cost}")
    
    print ("Is this correct? Y/N")
    approval = input("Please enter Y if the informatiton is correct or N if you need to re-enter: ")
    
def intro_page():
    """
     Introductory screen for the user, explains what the calculator does
     and gives them the ability to select the mode they want to use.
    """

    print("Welcome to the Sales Calculator!\n")

    print("""\
     __________
    | ________ |
    ||12345678||
    |##########|
    |[M|#|C][-]|
    |[7|8|9][+]|
    |[4|5|6][x]|
    |[1|2|3][%]|
    |[.|O|:][=]|
     ----------\n """)

    print("This program allows you to convert currency or help you price your renewal quote")

    while True:
        print("To get started, please enter convert if you want the currency converter.")
        print("Enter renewal if you want to price your renewal quote")

        type = input("Please enter your choice here:\n")

        if type == "convert":
            convert_cal()
            break
        elif type == "renewal":
            renew_info()
            break
        else:
            print("Invalid input, please try again.\n")

intro_page()