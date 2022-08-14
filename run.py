"""
Imports external libraries for the program
Connects APIs and allow access via credentials file
"""

import gspread 
from google.oauth2.service_account import Credentials
import colorama
from colorama import Fore, Style
colorama.init(autoreset=True)
import pandas as pd

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
stored_info = SHEET.worksheet('database')


def new_customer():
    print("To get started, please enter your username.")
    print("Usernames must be between 2 and 15 characters,")
    print("and should contain only letters from a to z.\n")
    
    global cust_name
    cust_name = input("Enter your customer name here:\n")

    if cust_name.isalpha() and len(cust_name) > 1 and len(cust_name) < 16:
        welcome_user()
    else:
         print(Fore.LIGHTYELLOW_EX +
                  "\nThe username you have entered is not valid, \
please try again.\n")

def hist_data():
    """
    Allows user to view saved details
    """
    cust_name = input("Enter your customer name here:\n")

    if stored_info.find(cust_name, in_column=1):
         print(Fore.LIGHTGREEN_EX + Style.BRIGHT +
              "\nThe details you currently have saved are:\n")
         df = pd.DataFrame(stored_info.get_all_records())
         user_record = df.loc[df['cust_name'] == cust_name].to_string(index=False)
         print(f"{Fore.LIGHTCYAN_EX }{Style.BRIGHT}\n{user_record}\n")

         while True:
            print("What would you like to do now?")
            print("Type 'a' to check another customer.")
            print("Type 'b' to return to the main menu.")
            print("Type 'c' to exit the renewal calculator")

            selection = input("Enter your selection here:\n")
            selection = selection.lower()
            if selection == "a":
                hist_data()
                break
            elif selection == "b":
                first_page()
                break
            elif selection == "c":
                print(f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}\n\
Thank you for using the calculator and goodbye.")
                break
            else:
                print(Fore.LIGHTYELLOW_EX +
                      "Invalid input, please try again.\n")

    else:
        print(Fore.LIGHTYELLOW_EX +
              "\nYou do not currently have any details stored.")
        print(Fore.LIGHTYELLOW_EX + "Returning to the main menu...")
        first_page()

        
def first_page():
    """ 
        Intro Page
    """
    print(Fore.CYAN + Style.BRIGHT +
        "Welcome to your Renewal Calculator!\n")
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

    print("This program lets you to enter last years")
    print("renewal cost and get this years uplifted price.")
    print("Along with multi-year pricing.\n")

    print(Fore.CYAN + Style.BRIGHT +
    "To start enter 1 if you want to start a new calculation.")
    print(Fore.CYAN + Style.BRIGHT +
    "Enter 2 if you want to pull historical data for a customer")

    mode = input("Please enter your choice here:\n")
    
    if mode == "1":
        new_customer()
    elif mode == "2":
        hist_data()
    else:
        print(Fore.LIGHTYELLOW_EX + "Invalid input, please try again.\n")

first_page()