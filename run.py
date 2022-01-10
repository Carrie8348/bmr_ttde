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
SHEET = GSPREAD_CLIENT.open('fitness')


def get_user_info():
    """
    Get user basic info for calculate BMR
    """
    print("Hello, this is User BMR calculating center...\n")
    print("Please enter your weight(kg), height(cm) and age here...\n")
    print("Example: 59, 165, 30\n")

    data_str = input("Enter your data here:")

    user_data = data_str.split(",")
    print(f"The data provide is {data_str}")
    return user_data

def validate_user_data(values):
    """
    Inside the try, convert strings into values, 
    raise ValueError if strings cannot be converted into int,
    or if there aren't exactly 3 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 3:
            raise ValueError(
                f"Exactly 3 values required, you provide {len(values)}"
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
    user_worksheet.append_row(user_data)
    print("User worksheet updated successfully.\n")

def calculate_bmr(user_data):
    print('')

user_data = get_user_info()
user_data = [int(num) for num in user_data]
update_user_dataworksheet(user_data)
calculate_bmr(user_data)
