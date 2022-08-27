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
from rich.console import Console
from rich.table import Table


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

def multi(vue):
    print("Would you like pricing for the second and third year? type Y/N")
    multi_year = input("Y/N:\n")
    if multi_year == "Y":
        global second_year
        second_year = vue /100 * 90 
        global third_year
        third_year = vue /100 * 85
        print(Fore.CYAN + Style.BRIGHT + f"Second year price {second_year}.")
        print(Fore.CYAN + Style.BRIGHT + f"Third year price {third_year}.")
        print(Fore.CYAN + Style.BRIGHT + "Directing to save page")
        save_details()
    elif multi_year == "N":
        print(Fore.CYAN + Style.BRIGHT + "Directing to save page")
        save_details()
    else:
        print("invalid input")

def pricing_kace(product, support):
    """function to uplift the price"""
    value = float(input("Amount:\n"))
    global cost 

    if ((support == "s") and (product == "kace")\
       and (value < data_standard_kace)):
        global cost
        cost = value * 1.05
        print(Fore.CYAN + Style.BRIGHT + f"Your uplifted price is {cost}")
        multi(cost)
    elif ((support == "m") and (product == "kace")\
       and (value < data_mid_kace)):
        cost = value * 1.07
        print(Fore.CYAN + Style.BRIGHT + f"Your uplifted price is {cost}")
        multi(cost)
    elif ((support == "p") and (product == "kace")\
       and (value < data_mid_kace)):
        cost = value * 1.09
        print(Fore.CYAN + Style.BRIGHT + f"Your uplifted price is {cost}") 
        multi(cost)
    else:
        print("Your quote has reached list price no uplift")


def pricing_toad(product, support, cust_name):
    """function to uplift the price"""
    value = float(input("Amount:\n"))
    global cost

    if ((support == "s") and (product == "toad")\
       and (value < data_standard_toad)):
        cost = value * 1.04
        print(Fore.CYAN + Style.BRIGHT + f"Your uplifted price is {cost}")
        multi(cost)
    elif ((support == "m") and (product == "toad")\
       and (value < data_mid_toad)):
        cost = value * 1.06
        print(Fore.CYAN + Style.BRIGHT + f"Your uplifted price is {cost}")
        multi(cost)
    elif ((support == "p") and (product == "toad")\
       and (value < data_mid_toad)):
        cost = value * 1.08
        print(Fore.CYAN + Style.BRIGHT + f"Your uplifted price is {cost}")
        multi(cost)
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

    if stored_info.find(cust_name, in_column=1):
        print("Already Present")
        new_customer()
    elif cust_name.isalpha() and len(cust_name) > 1 and len(cust_name) < 16:
        print(Fore.LIGHTYELLOW_EX + "Customer name")
    else:
        print("Not accepted try again")
        new_customer()
        

    print(Fore.CYAN + Style.BRIGHT + "Please enter your product: Toad or Kace")
    global type
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
        pricing_toad(type, level, cust_name)
    elif type == "kace":
        pricing_kace(type, level, cust_name)
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
        data = (Convert(user_record))
        print(data)

        print(f"{Fore.LIGHTCYAN_EX }{Style.BRIGHT}\n{user_record}\n")

        table = Table(title = "Historical Data")

        table.add_column("Name")
        table.add_column("Product")
        table.add_column("First Year")
        table.add_column("Second Year")
        table.add_column("Third Year")
       
        table.add_row(data[13], data[17], data[25], data[33], data[40])
        
        

        console = Console()
        console.print(table)
        

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


def Convert(string):
    li = list(string.split(" "))
    return li


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