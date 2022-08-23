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

"""Constant Variables for List  Pice for each Product and Support Level"""
data_standard_toad = float(price.acell('C3').value)
data_mid_toad = float(price.acell('C4').value)
data_prem_toad = float(price.acell('C5').value)
data_standard_kace = float(price.acell('D3').value)
data_mid_kace = float(price.acell('D4').value)
data_prem_kace = float(price.acell('D5').value)

def multi(vue):
    print("Would you like pricing for the second and third year? type Y/N")
    multi_year = input("Y/N:\n")
    if multi_year == "Y":
        second_year = vue /100 * 90 
        third_year = vue /100 * 85
        print(Fore.CYAN + Style.BRIGHT + f"Second year price {second_year}.")
        print(Fore.CYAN + Style.BRIGHT + f"Third year price {third_year}.")
    elif multi_year == "N":
        print(Fore.CYAN + Style.BRIGHT + "Directing to save page")
    else:
        print("invalid input")

def pricing_kace(product, support):
    print("hello")

def pricing_toad(product, support):
    """function to uplift the price"""
    value = float(input("Amount:\n"))

    if ((support == "s") and (product == "toad")\
       and (value < data_standard_toad)):
        cost = value * 1.04
        print(Fore.CYAN + Style.BRIGHT + f"Your uplifted price is {cost}")
        multi(cost)
    elif ((support == "m") and (product == "toad")\
       and (value < data_mid_toad)):
        cost = value * 1.06
        print(Fore.CYAN + Style.BRIGHT + f"Your uplifted price is {cost}")
    elif ((support == "p") and (product == "toad")\
       and (value < data_mid_toad)):
        cost = value * 1.08
        print(Fore.CYAN + Style.BRIGHT + f"Your uplifted price is {cost}") 
    else:
        print("Your quote has reached list price no uplift")

    
def new_customer():
    print(Fore.CYAN + Style.BRIGHT + "To get started, please enter your\
    \ncustomer name.")
    print(Fore.CYAN + Style.BRIGHT + "Names must be between 2 and 15\
    \ncharacters,")
    print(Fore.CYAN + Style.BRIGHT + "and should contain only letters from a\
    \nto z.")
    global cust_name
    cust_name = input("Enter your customer name here:\n")

    if cust_name.isalpha() and len(cust_name) > 1 and len(cust_name) < 16:
        print("Customer name accepted")
    else:
        print(Fore.LIGHTYELLOW_EX + "The name you have entered is not valid,please try again.")
        new_customer()

    print(Fore.CYAN + Style.BRIGHT + "Please enter your product: Toad or Kace")
    type = input("Please enter your choice here:\n")
    type = type.lower()

    if ((type == "toad") or (type == "kace")):
        print("Product accepted")
    else:
        print(Fore.LIGHTYELLOW_EX + "The product is not valid,please try again.")
        new_customer()

    print(Fore.CYAN + Style.BRIGHT + "Please enter the support level of your quote\
    \n's' for Standard, 'm' for Mid and 'p' for Premiere")
    level = str(input("s,m or p: "))
    level = level.lower()
    if ((level == "s") or (level == "m") or (level == "p")):
        print("Support level accepted")
    else:
        print(Fore.LIGHTYELLOW_EX + "The support level is not valid,please try again.")
        new_customer()
    
    
    if type == "toad":
        pricing_toad(type, level)
    elif type == "kace":
        pricing_kace(type, level)
    else:
        print(Fore.LIGHTYELLOW_EX + "Invalid input, please try again.\n")
        new_customer()

def hist_data():
    """
    Allows user to view saved details
    """
    cust_name = input("Enter your customer name here:\n")

    if stored_info.find(cust_name, in_column=1):
         print(Fore.LIGHTGREEN_EX + Style.BRIGHT +
              "\nThe details you currently have saved are:\n")
         df = pd.DataFrame(stored_info.get_all_records())
         user_record = df.loc[df['Customer'] == cust_name].to_string(index=False)
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
        elif selection == "b":
            first_page()
        elif selection == "c":
            print(f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}\
        \nThank you for using the calculator and goodbye.")
        break

    else:
        print(Fore.LIGHTYELLOW_EX +
        "\nYou do not currently have any details stored.")
        print(Fore.LIGHTYELLOW_EX + "Returning to the main menu...")
        first_page()


def first_page():
    """
    Intro Page where the user can select the mode they want to use.
    """
    print(Fore.GREEN + Style.BRIGHT + "Welcome to your Renewal Calculator!\n")
    print(Fore.MAGENTA + Style.BRIGHT + """\
     ----------
    | -------- |
    ||12345678||
    |----------|
    |[M|#|C][-]|
    |[7|8|9][+]|
    |[4|5|6][x]|
    |[1|2|3][%]|
    |[.|O|:][=]|
     ----------\n""")

    print("This program lets you to enter last years")
    print("renewal cost and get this years uplifted price.")
    print("Along with multi-year pricing.\n")
    print("You can also save and retrieve customer pricing details")

    while True:
        print(Fore.CYAN + Style.BRIGHT + "Enter 1 if you want to start a new\
        \ncalculation.")
        print(Fore.CYAN + Style.BRIGHT + "Enter 2 if you want to access\
        \nhistorical data for a customer")

        mode = input("Please enter your selection here:\n")
        if mode == "1":
            new_customer()
            break
        elif mode == "2":
            hist_data()
            break
        else:
            print(Fore.LIGHTYELLOW_EX + "Invalid input, please try again.\n")         

first_page()