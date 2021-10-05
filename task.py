from online_banking_functions import retrieve_pay_amount
from excel_workbook_functions import *
from tabulate import tabulate


from RPA.FileSystem import FileSystem

# For debugging purposes only
def debugging_deleteLastCreateFile():
    FILE_SYSTEM_CONTROLLER = FileSystem()
    MISSING_OK = False
    FILENAME = "2021-10-15.xlsx"
    BUDGET_SPREADSHEET_DIRECTORY = "./DataSets"

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
