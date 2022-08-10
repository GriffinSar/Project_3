"""
Imports external libraries for the program
Connects APIs and allow access via credentials file
"""

import gspread 
from google.oauth2.service_account import Credentials
import colorama
from colorama import Fore, Style
colorama.init(autoreset=True)

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

""" Variables for pricing"""

data_standard_toad = float(price.acell('B2').value)
data_mid_toad = float(price.acell('B3').value)
data_prem_toad = float(price.acell('B4').value)

def toad_pricing():
    level = str(input("standard,mid,premiere: "))
    price = float(input("Amount: "))

    if level == "standard":
        if price < data_standard_toad:
            cost = price * 1.03
            print(f"Your uplifted price is {cost}")
        elif price >= data_standard_toad:
            print(f"Your quote has reached the list \
            price of {data_standard_toad} no uplift needed.")
        else:
            print(f"{level} is not a valid input try again")
            toad_pricing()

def start_page():
    """ 
    Introduction page for user
    """

    print(Fore.CYAN + Style.BRIGHT +
        "Welcome to your renewal calculator!\n")
    print(Fore.MAGENTA + Style.BRIGHT + """\
     _________
    | ________ |
    ||12345678||
    |----------|
    |[M|#|C][-]|
    |[7|8|9][+]|
    |[4|5|6][x]|
    |[1|2|3][%]|
    |[.|O|:][=]|
     __________ \n""")

    print("This program allows you to enter last years")
    print("renewal cost and get this years uplifted price.")
    print("Along with multi-year pricing.\n")


    print(Fore.CYAN + Style.BRIGHT +
    "Please enter Toad if your Quote is for a Toad \
    \nproduct.")
    print(Fore.CYAN + Style.BRIGHT +
    "Please enter Kace if your Quote is for a \
    \nKace Product.\n")

    type = input("Please enter your choice here:\n")

    if type == "Toad":
        toad_pricing()   
    elif type == "Kace":
        print("Goodbye")      
    else:
        print(Fore.LIGHTYELLOW_EX + "Invalid input, please try again.\n")


start_page()
