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

select = input("Please select a calculator mode, Type renewal or currency: ")
product = input("Please select your product, Toad or Kace: ")
level = input("Please select support level, standard, mid, premier: ")
pricuplift = int(input("Please enter the price to uplift: "))e_
print(f"You have chosen {select} for {product} support level {level} and last years price was {price_uplift}.")



#this is how you get access to one individual cell
data = int(price.acell( 'B2').value)

def uplift_cal():
    if price_uplift == data:
        print("No Uplift List Price has Been Reached")
    else: 
        final = price_uplift * 1.3
        print(final)

def mode_select(x):
    if select == "renewal":
        uplift_cal()
    elif select == "currency":
        print("not created yet")


mode_select(select)



#Create a function to uplift a price entered by a user

uplift_cal()