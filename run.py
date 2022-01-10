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
    print("Please enter your name, gender, weight(kg), height(cm) and age here...\n")
    print("Example: Jim Carter, male, 59, 165, 30\n")

    data_str = input("Enter your data here:")

    user_data = data_str.split(",")
    print(f"The data provide is {data_str}")
    return user_data

def update_user_dataworksheet(data):
    """
    Update user data from the input, and add new row
    in Google Sheet
    """
    print("Updating User Data...\n")
    user_worksheet = SHEET.worksheet("user_info")
    user_worksheet.append_row(user_data)
    print("User worksheet updated successfully.\n")

user_data = get_user_info()
update_user_dataworksheet(user_data)
