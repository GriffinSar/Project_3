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
hello = SHEET.worksheet('hello')

data = float(hello.acell( 'B4').value)


print("Please enter the currency you want to convert Euro to and the amount: ")

to_currency = str(
        input("Enter in the currency you'd like to convert to: ")).upper()

amount = float(input("Enter in the amount of money: "))

print(amount * data)




