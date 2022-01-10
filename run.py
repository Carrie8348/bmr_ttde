import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
from googleapiclient import discovery



SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('fitness')


def get_user_info():
    """
    Get user basic info for calculate BMR,
    un a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 3 numbers separated
    by commas. The loop will repeatedly request data, until it is valid.
    """

    while True:
        print("Hello, this is User BMI calculating center...\n")
        print("Please enter your weight(kg), height(cm) here...\n")
        print("Example: 60, 162\n")

        data_str = input("Enter your data here:")

        user_data = data_str.split(",")
        validate_user_data(user_data)

        if validate_user_data(user_data):
            print("Data is valid!")
            break

        print(f"The data provide is {data_str}")

    return user_data

def validate_user_data(values):
    """
    Inside the try, convert strings into values, 
    raise ValueError if strings cannot be converted into int,
    or if there aren't exactly 2 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 2:
            raise ValueError(
                f"Exactly 2 values required, you provide {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data:{e}, please try again. \n")
        return False
    
    return True

def update_user_dataworksheet(data):
    """
    Update user data from the input, and add new row
    in Google Sheet
    """
    print("Updating User Data...\n")
    user_worksheet = SHEET.worksheet("user_info")
    user_worksheet.append_row(data)
    print("User worksheet updated successfully.\n")

def calculate_bmi(user_data):
    """
    Calculate user bmi based on the string value
    """
    print("Calculating BMI...\n")
    bmi_data = []
    weight = user_data[0]
    height = user_data[1]
    result = (weight / height / height) * 10000
    rounded_result = round(result, 2)
    bmi_data = rounded_result
    print(f"Your BMI is {bmi_data}..\n")

    return bmi_data
  

def update_bmi_worksheet(new_bmi_data):
    """
    Update bmi data in worksheet
    """
    print("Updating BMI sheet...'\n")
    bmi_worksheet = SHEET.worksheet("bmi")
    bmi_worksheet.append_row(new_bmi_data)
    print("BMI worksheet updated successfully.\n")
    

def main():
    """
    Run all programs
    """
    user_data = get_user_info()
    user_data = [int(num) for num in user_data]
    update_user_dataworksheet(user_data)
    new_bmi_data = [calculate_bmi(user_data)]
    update_bmi_worksheet(new_bmi_data)

main()