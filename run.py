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

def save_details():
    """
    Allow the user to save the details,
    to the database for later.
    """

    while True:
        print(Fore.LIGHTRED_EX + Style.BRIGHT +
              "Would you like to save these details?\n")
        print("Type 's' to save these details for future use.")
        print("Type 'x' to return to the main menu.")
        print("Type 'z' to exit calculator")

        save = input("Enter your selection here:\n")
        save = save.lower()
        if save == "s":
            list_details = [
                cust_name, type, cost, second_year, third_year
            ]
            print("Saving your details...\n")
            database = SHEET.worksheet('database')
            database.append_row(list_details)
            print(Fore.CYAN + Style.BRIGHT + "Your details have been saved to the database.\n")
            print("\nTaking you to the main page...")
            first_page()
            break
        elif save == "x":
            first_page()
            break
        elif save == "z":
            print("Thanks for using the calculator, goodbye!")
            break
        else:
            print(Fore.LIGHTYELLOW_EX + "Invalid input, please try again.\n")


def kace_stan():
    """Function to price standard Kace Quotes"""
    while True: 
        if quote < data_standard_kace:
            global cost
            cost = quote * 1.04
            print(Fore.CYAN + Style.BRIGHT + f"Your uplifted price is {cost}")
        elif quote >= data_standard_kace:
            print(Fore.RED + Style.BRIGHT + f"Your quote has reached the list price")
            print(Fore.RED + Style.BRIGHT + f"of {data_standard_kace} no uplift needed.")
            print(Fore.RED + Style.BRIGHT + "Directing back to Home page")
            first_page()
            break
            

            print("Would you like pricing for the second and third year? type Y/N")
            multi_year = input("Y/N:\n")
            global second_year
            second_year = cost /100 * 90 
            global third_year
            third_year = cost /100 * 85

            if multi_year == "Y":
                print(Fore.CYAN + Style.BRIGHT + f"Second year price\
                \n{second_year}")
                print(Fore.CYAN + Style.BRIGHT + f"Third year price\
                \n{third_year}")
                save_details()
                break
            elif multi_year == "N":
                print(Fore.CYAN + Style.BRIGHT + "Directing to save page")
                save_details()
                break

        else: 
            print("invalid input")
            break

def kace_mid():
    """Function to price mid Toad Quotes"""
    if quote < data_mid_kace:
        global cost
        cost = quote * 1.06
        print(f"Your uplifted price is {cost}")
    elif quote >= data_mid_kace:
        print(f"Your quote has reached the list \
        price of {data_mid_kace} no uplift needed.")

    print("Would you like pricing for the second and third year? type Y/N")
    multi_year = input("Y/N:\n")
    global second_year
    second_year = cost /100 * 90 
    global third_year
    third_year = cost /100 * 85

    if multi_year == "Y":
            print(Fore.CYAN + Style.BRIGHT + f"Second year price {second_year}.")
            print(Fore.CYAN + Style.BRIGHT + f"Third year price {third_year}.")
            save_details()
    elif multi_year == "N":
            print(Fore.CYAN + Style.BRIGHT + "Directing to save page")
            save_details()

    else: 
        print("invalid input")


def kace_prem():
    """Function to price premiere Toad Quotes"""

    if quote < data_prem_kace:
        global cost
        cost = quote * 1.08
        print(Fore.CYAN + Style.BRIGHT + f"Your uplifted price is {cost}")
    elif quote >= data_prem_kace:
        print(Fore.CYAN + Style.BRIGHT + f"Your quote has reached the list \
        price of {data_prem_kace} no uplift needed.")

    print("Would you like pricing for the second and third year? type Y/N")
    multi_year = input("Y/N:\n")
    global second_year
    second_year = cost /100 * 90 
    global third_year
    third_year = cost /100 * 85

    if multi_year == "Y":
            print(Fore.CYAN + Style.BRIGHT + f"Second year price {second_year}.")
            print(Fore.CYAN + Style.BRIGHT + f"Third year price {third_year}.")
            save_details()
    elif multi_year == "N":
            print(Fore.CYAN + Style.BRIGHT + "Directing to save page")
            save_details()

    else: 
        print("invalid input")


def kace_pricing():
    """function to uplift the price"""
    level = str(input("Standard,Mid,Premiere:\n"))

    if level == "Standard":
        kace_stan()
    elif level == "Mid":
        kace_mid()
    elif level == "Premiere":
        kace_prem()
    else:
        print(f"{level} is not a valid input try again")
        kace_pricing()


def toad_stan():
    """Function to price standard Toad Quotes"""

    while True: 
        if quote < data_standard_toad:
            global cost
            cost = quote * 1.04
            print(Fore.CYAN + Style.BRIGHT + f"Your uplifted price is {cost}")
        elif quote >= data_standard_toad:
            print(Fore.RED + Style.BRIGHT + f"Your quote has reached the list price")
            print(Fore.RED + Style.BRIGHT + f"of {data_standard_toad} no uplift needed.")
            print(Fore.RED + Style.BRIGHT + "Directing back to Home page")
            first_page()
            break

        print("Would you like pricing for the second and third year? type Y/N")
        multi_year = input("Y/N:\n")
        global second_year
        second_year = cost /100 * 90 
        global third_year
        third_year = cost /100 * 85

        if multi_year == "Y":
            print(Fore.CYAN + Style.BRIGHT + f"Second year price {second_year}.")
            print(Fore.CYAN + Style.BRIGHT + f"Third year price {third_year}.")
            save_details()
        elif multi_year == "N":
            print(Fore.CYAN + Style.BRIGHT + "Directing to save page")
            save_details()

        else: 
            print("invalid input")


def toad_mid():
    """Function to price mid Toad Quotes"""

    if quote < data_mid_toad:
        global cost
        cost = quote * 1.05
        print(f"Your uplifted price is {cost}")
    elif quote >= data_mid_toad:
        print(f"Your quote has reached the list \
        price of {data_mid_toad} no uplift needed.")

    print("Would you like pricing for the second and third year? type Y/N")
    multi_year = input("Y/N:\n")
    global second_year
    second_year = cost /100 * 90 
    global third_year
    third_year = cost /100 * 85

    if multi_year == "Y":
            print(Fore.CYAN + Style.BRIGHT + f"Second year price {second_year}.")
            print(Fore.CYAN + Style.BRIGHT + f"Third year price {third_year}.")
            save_details()
    elif multi_year == "N":
            print(Fore.CYAN + Style.BRIGHT + "Directing to save page")
            save_details()

    else: 
        print("invalid input")


def toad_prem():
    """Function to price premiere Toad Quotes"""

    if quote < data_prem_toad:
        global cost
        cost = quote * 1.07
        print(Fore.CYAN + Style.BRIGHT + f"Your uplifted price is {cost}")
    elif quote >= data_prem_toad:
        print(Fore.CYAN + Style.BRIGHT + f"Your quote has reached the list \
        price of {data_prem_toad} no uplift needed.")

    print("Would you like pricing for the second and third year? type Y/N")
    multi_year = input("Y/N:\n")
    global second_year
    second_year = cost /100 * 90 
    global third_year
    third_year = cost /100 * 85

    if multi_year == "Y":
            print(Fore.CYAN + Style.BRIGHT + f"Second year price {second_year}.")
            print(Fore.CYAN + Style.BRIGHT + f"Third year price {third_year}.")
            save_details()
    elif multi_year == "N":
            print(Fore.CYAN + Style.BRIGHT + "Directing to save page")
            save_details()

    else: 
        print("invalid input")


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

    print(Fore.CYAN + Style.BRIGHT +
    "Please enter Toad if your Quote is for a Toad product.")
    print(Fore.CYAN + Style.BRIGHT +
    "Please enter Kace if your Quote is for a Kace Product.\n")
    
    global type
    type = input("Please enter your choice here:\n")

    print(Fore.CYAN + Style.BRIGHT + "Please enter the cost of last years renewal quote.")
    global quote
    quote = float(input("Amount:\n"))

    if type == "Toad":
        toad_pricing()   
    elif type == "Kace":
        kace_pricing()     
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