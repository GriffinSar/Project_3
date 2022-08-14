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

data_standard_toad = float(price.acell('B2').value)
data_mid_toad = float(price.acell('B3').value)
data_prem_toad = float(price.acell('B4').value)

def toad_stan():
    """Function to price standard Toad Quotes"""

    if quote < data_standard_toad:
        cost = quote * 1.03
        print(Fore.CYAN + Style.BRIGHT + f"Your uplifted price is {cost}")
    elif quote >= data_standard_toad:
        print(Fore.CYAN + Style.BRIGHT + f"Your quote has reached the list \
        price of {data_standard_toad} no uplift needed.")

    print("Would you like pricing for the second and third year? type Y/N")
    multi_year = input("Y/N: ")
    second_year = cost /100 * 90 
    print(second_year)
    third_year = cost /100 * 85

    if multi_year == "Y":
        print(Fore.CYAN + Style.BRIGHT + f"Second year price {second_year}.")
        print(Fore.CYAN + Style.BRIGHT + f"Third year price {third_year}.")
    else :
        print(Fore.CYAN + Style.BRIGHT + "nothing")


def toad_mid():
    """Function to price mid Toad Quotes"""

    if quote < data_mid_toad:
        cost = quote * 1.05
        print(f"Your uplifted price is {cost}")
    elif quote >= data_mid_toad:
        print(f"Your quote has reached the list \
        price of {data_mid_toad} no uplift needed.")

def toad_prem():
    """Function to price premiere Toad Quotes"""

    if quote < data_prem_toad:
        cost = quote * 1.07
        print(Fore.CYAN + Style.BRIGHT + f"Your uplifted price is {cost}")
    elif quote >= data_prem_toad:
        print(Fore.CYAN + Style.BRIGHT + f"Your quote has reached the list \
        price of {data_prem_toad} no uplift needed.")

def toad_pricing():
    """function to uplift the price"""
    level = str(input("Standard,Mid,Premiere: "))

    if level == "Standard":
        toad_stan()
    elif level == "Mid":
        toad_mid()
    elif level == "Premiere":
        toad_prem()
    else:
        print(f"{level} is not a valid input try again")
        toad_pricing()

def new_customer():
    print("To get started, please enter your username.")
    print("Usernames must be between 2 and 15 characters,")
    print("and should contain only letters from a to z.\n")
    
    global cust_name
    cust_name = input("Enter your customer name here:\n")

    if cust_name.isalpha() and len(cust_name) > 1 and len(cust_name) < 16:
        print("Customer name accepted")
    else:
        print(Fore.LIGHTYELLOW_EX +
                "\nThe username you have entered is not valid, \
                please try again.\n")

    print(Fore.CYAN + Style.BRIGHT +
    "Please enter Toad if your Quote is for a Toad \
    \nproduct.")
    print(Fore.CYAN + Style.BRIGHT +
    "Please enter Kace if your Quote is for a \
    \nKace Product.\n")
    
    global type
    type = input("Please enter your choice here:\n")
    global quote
    quote = float(input("Amount: "))

    if type == "Toad":
        toad_pricing()   
    elif type == "Kace":
        print("Goodbye")      
    else:
        print(Fore.LIGHTYELLOW_EX + "Invalid input, please try again.\n")

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