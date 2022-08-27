def Convert(string):
    li = list(string.split(" "))
    return li



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