from online_banking_functions import retrieve_pay_amount
from excel_workbook_functions import *
from file_name_helpers import get_latest_filename, name_next_sheet, make_file_name


from RPA.FileSystem import FileSystem

BUDGET_SPREADSHEET_DIRECTORY = "./DataSets"

# This gets the last pay period workbook and makes a copy of it for the current pay period and returns the filename
def clone_budget_spreadsheet():
    file_list_from_directory = FILE_SYSTEM_CONTROLLER.list_files_in_directory(BUDGET_SPREADSHEET_DIRECTORY)
    date_of_last_pay = get_latest_filename(file_list_from_directory)    

    LAST_SPREADSHEET_NAME = make_file_name(date_of_last_pay)
    NEW_SPREADSHEET_NAME = name_next_sheet(date_of_last_pay, PAY_PERIOD_LENGTH_IN_DAYS)

    FILE_SYSTEM_CONTROLLER.copy_file(BUDGET_SPREADSHEET_DIRECTORY + '/' + LAST_SPREADSHEET_NAME, BUDGET_SPREADSHEET_DIRECTORY + '/' + NEW_SPREADSHEET_NAME)

    print (NEW_SPREADSHEET_NAME, " has been created.")
    return NEW_SPREADSHEET_NAME

# For debugging purposes only
def debugging_deleteLastCreateFile():
    FILE_SYSTEM_CONTROLLER = FileSystem()
    MISSING_OK = False
    FILENAME = "2021-10-15.xlsx"

    try: 
        print("TRY TO DELETE LAST FILE", FILENAME)
        FILE_SYSTEM_CONTROLLER.remove_file(BUDGET_SPREADSHEET_DIRECTORY + "/" + FILENAME,MISSING_OK)
    except:
        print("We couldn't find the file")

if __name__ == "__main__":
    # retrieve_pay_amount()
    debugging_deleteLastCreateFile()
    
    EXCEL_FILE_NAME = clone_budget_spreadsheet()

    update_bills_sheet(EXCEL_FILE_NAME)
