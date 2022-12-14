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
import time

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

        save = input("Enter your selection here:\n")
        save = save.lower()
        if save == "s":
            list_details = [
                cust_name, type, level, cost, second_year, third_year
            ]
            print("Saving your details...\n")
            database = SHEET.worksheet('database')
            database.append_row(list_details)
            print(Fore.CYAN + Style.BRIGHT + "Your details have been saved to\
            \nthe database.")
            print("\nTaking you to the main page...")
            first_page()
        elif save == "x":
            first_page()
        else:
            print(Fore.LIGHTYELLOW_EX + "Invalid input, please try again.\n")


def multi(vue):
    """
    Function that calculates a second and third year price for the user based on the 
    uplifted one year price
    """
    
    print("Would you like pricing for the second and third year? type Y/N")
    multi_year = input("Y/N:\n")
    if multi_year == "Y":
        global second_year
        second_year = vue /100 * 90 
        global third_year
        third_year = vue /100 * 85

        table = Table(title = "Pricing")

        table.add_column("First Year")
        table.add_column("Second Year")
        table.add_column("Third Year")

        table.add_row(str(vue), str(second_year), str(third_year))

        console = Console()
        console.print(table)

        save_details()

    elif multi_year == "N":
        print(Fore.CYAN + Style.BRIGHT + "Directing to home page")
        time.sleep(2)
        first_page()
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
    """function to uplift the price of the previous renewal"""
    global cost

    console = Console()
    console.print("Please enter last years renewal price", style= "bright_white bold")

    
    try:
        value = float(input(Fore.GREEN + Style.BRIGHT + "Amount:\n"))
        if ((support == "s") and (value < data_standard_toad)):
            cost = value * 1.04
            table = Table(title="Uplift")
            table.add_column("Uplifted price")
            table.add_row(str(cost))
            console = Console()
            console.print(table)
            multi(cost)
        elif ((support == "m") and (value < data_mid_toad)):
            cost = value * 1.05
            table = Table(title="Uplift")
            table.add_column("Uplifted price")
            table.add_row(str(cost))
            console = Console()
            console.print(table)
            multi(cost)
        elif ((support == "p") and (value < data_mid_toad)):
            cost = value * 1.07
            table = Table(title="Uplift")
            table.add_column("Uplifted price")
            table.add_row(str(cost))
            console = Console()
            console.print(table)
            multi(cost)
        else:
            console.print("Your quote has reached list price no uplift\n", style= "red", justify= "center")
    except ValueError:
        print(Fore.LIGHTYELLOW_EX + "The values you have entered are not in \
the correct format, please try again.\n")
        pricing_toad(product, support, cust_name)
 

        while True:
            console = Console()
            console.print("What would you like to do now?", style = "bold medium_purple", justify = "center")
            console.print("Type 'a' to start another calculation.", style = "bold bright_white", justify = "center")
            console.print("Type 'b' to return to the main menu.", style = "bold bright_white", justify = "center")
            console.print("Type 'c' to exit the renewal calculator\n", style = "bold bright_white", justify = "center")

            selection = input(Fore.GREEN + Style.BRIGHT + "Enter your selection here:\n")
            selection = selection.lower()

            if selection == "a":
                new_customer()
            elif selection == "b":
                first_page()
            elif selection == "c":
                print(f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}\
            \nThank you for using the calculator and goodbye.")
            break
            time.sleep(3)

       
def new_customer():
    """
    Function to let user enter their details along with quote type so they can be 
    directed to the correct calculation"""

    console = Console()
    console.print("To get started, please enter your\
    \ncustomer name.", style = "bold bright_white", justify = "center")
    console.print("Names must be between 2 and 15\
    \ncharacters,", style = "bold bright_white", justify = "center")
    console.print("and should contain only letters from a\
    \nto z.", style = "bold bright_white", justify = "center")

    global cust_name
    cust_name = input(Fore.GREEN + Style.BRIGHT + "Enter your customer name here:\n")
    cust_name = cust_name.lower()

    if cust_name.isalpha() and len(cust_name) > 1 and len(cust_name) < 16:
        console.print("Customer name accepted", style= "bright_yellow", justify= "center")
    else:
        console.print("Not accepted try again", style= "bold bright_red")
        new_customer()
        

    console.print("Please enter your product: Toad or Kace", style= "bright_white bold")
    global type
    type = input(Fore.GREEN + Style.BRIGHT + "Please enter your choice here:\n")
    type = type.lower()

    if ((type == "toad") or (type == "kace")):
        console.print("Product accepted", style= "bright_yellow", justify= "center")
    else:
        print(Fore.LIGHTYELLOW_EX + "The product is not valid,please try again.")
        new_customer()

    console.print("Please enter the support level of your quote\
    \n'S' for Standard, 'M' for Mid and 'P' for Premiere", style = "bright_white bold")
    global level
    level = input(Fore.GREEN + Style.BRIGHT + "S,M or P:\n ")
    level = level.lower()
    if ((level == "s") or (level == "m") or (level == "p")):
        console.print("Support level accepted", style= "bright_yellow", justify= "center")
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
    Function that  lets the user enter details to access saved data
    """
    cust_name = str(input(Fore.LIGHTGREEN_EX + Style.BRIGHT +\
        "Enter your customer name here:\n"))
    cust_name = cust_name.lower()

    if stored_info.find(cust_name, in_column=1):
        console = Console()
        console.print("\nThe details you currently have saved are:\n", style= "white", justify= "center")
        df = pd.DataFrame(stored_info.get_all_records())
        user_record = df.loc[df['Customer'] == cust_name]\
            .to_string(index=False)

        print(f"{Fore.MAGENTA }{Style.BRIGHT}\n{user_record}\n")
        time.sleep(3)

        while True:
            console = Console()
            console.print("What would you like to do now?", style = "bold medium_purple", justify = "center")
            console.print("Type 'a' to check another customer.", style = "bold bright_white", justify = "center")
            console.print("Type 'b' to return to the main menu.", style = "bold bright_white", justify = "center")
            
            selection = input(Fore.GREEN + Style.BRIGHT + "Enter your selection here:\n")
            selection = selection.lower()

            if selection == "a":
                hist_data()
            elif selection == "b":
                first_page()
            else:
                print("Incorect input, please try again")
                hist_data()
    else:
        console = Console()
        time.sleep(2)
        console.print("You do not currently have any details stored.", style = "bright_white bold", justify= "center")
        console.print("Returning to the main menu...\n\n\n", style = "bright_white bold", justify= "center")
        time.sleep(2)
        first_page()
    

def first_page():
    """
    Intro Page where the user can select the mode they want to use.
    """
    console = Console()
    console.print("Welcome to your Renewal Calculator!\n", style = "underline bold", justify = "center")
    console.print("""\
     ----------
    | -------- |
    ||12345678||
    |----------|
    |[M|#|C][-]|
    |[7|8|9][+]|
    |[4|5|6][%]|
    |[1|2|3][%]|
    |[.|O|:][=]|
     ----------\n""", justify = "center")

    console.print("This program lets you to enter last years", style = "bold purple", justify = "center")
    console.print("renewal cost and get this years uplifted price.", style = "bold purple", justify = "center")
    console.print("Along with multi-year pricing.", style = "bold purple", justify = "center")
    console.print("You can also save and retrieve customer pricing details\n", style = "bold purple", justify = "center")
    
    while True:
        console.print("Enter 1 if you want to start a new calculation.", style = "bright_white", justify = "center")
        console.print("Enter 2 if you want to access historical data for a customer", style = "bright_white", justify = "center")
        console.print("Enter 3 if you want to exit the calculator\n", style = "bright_white", justify = "center")

        mode = input(Fore.GREEN + Style.BRIGHT + "Please enter your selection here:\n")
        if mode == "1":
            new_customer()
            break
        elif mode == "2":
            hist_data()
            break
        elif mode == "3":
            console.print("Exiting calculator.\n", style = "bright_yellow", justify= "center")
            break        
        else:
            console.print("Invalid input, try again .\n", style = "bright_yellow", justify= "center")
            time.sleep(2)
            first_page()

            
first_page()