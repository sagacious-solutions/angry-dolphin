from file_name_helpers import get_latest_filename, name_next_sheet, make_file_name

from RPA.Excel.Files import Files
from RPA.Tables import Tables
from RPA.FileSystem import FileSystem


TABLE_MANIPULATOR = Tables()
FILE_SYSTEM_CONTROLLER = FileSystem()

# Parameters for modifying spread sheet
BUDGET_SPREADSHEET_DIRECTORY = "./DataSets"
PRIMARY_WORKSHEET = "monthly"
BUDGET_COLUMN_HEIGHT_IN_ROWS = 12
EARLY_MONTH_BILLS = 'C'
LATE_MONTH_BILLS = 'D'
BILLS_FOR_PAY_PERIOD = 'F'
PAY_PERIOD_LENGTH_IN_DAYS = 14


# This gets the last pay period workbook and makes a copy of it for the current pay period and returns the filename
def clone_budget_spreadsheet():
    file_list_from_directory = FILE_SYSTEM_CONTROLLER.list_files_in_directory(BUDGET_SPREADSHEET_DIRECTORY)
    date_of_last_pay = get_latest_filename(file_list_from_directory)    

    LAST_SPREADSHEET_NAME = make_file_name(date_of_last_pay)
    NEW_SPREADSHEET_NAME = name_next_sheet(date_of_last_pay, PAY_PERIOD_LENGTH_IN_DAYS)

    FILE_SYSTEM_CONTROLLER.copy_file(BUDGET_SPREADSHEET_DIRECTORY + '/' + LAST_SPREADSHEET_NAME, BUDGET_SPREADSHEET_DIRECTORY + '/' + NEW_SPREADSHEET_NAME)

    print (NEW_SPREADSHEET_NAME, " has been created.")
    return NEW_SPREADSHEET_NAME

# This function will copy a column of values from one column to another
def copy_worksheet_column(workbook ,sheet, source, destination):
    START_AFTER_HEADER = 1
    
    for row in range(START_AFTER_HEADER, BUDGET_COLUMN_HEIGHT_IN_ROWS):
        try: 
            source_value = workbook.get_cell_value(row, source, sheet)
            workbook.set_cell_value(row, destination, source_value, sheet)
        except:
            print("copy_worksheet_column failed")

    return workbook


# This updates monthly bills sheet with the bills for this pay period
def update_bills_sheet(EXCEL_FILE_NAME):
    budget_workbook = Files()

    try:
        budget_workbook.open_workbook(BUDGET_SPREADSHEET_DIRECTORY + '/' + EXCEL_FILE_NAME)
    except:
        print ("We were unable to open a workbook named ", EXCEL_FILE_NAME)
        return

    print("Updating workbook ", EXCEL_FILE_NAME)

    PAY_DATE_DAY = int(EXCEL_FILE_NAME.split('-')[2].split('.')[0])

    if PAY_DATE_DAY <= 15 :
        copy_worksheet_column(budget_workbook, PRIMARY_WORKSHEET, LATE_MONTH_BILLS, BILLS_FOR_PAY_PERIOD)
    else :
        copy_worksheet_column(budget_workbook, PRIMARY_WORKSHEET, EARLY_MONTH_BILLS, BILLS_FOR_PAY_PERIOD)
    
    budget_workbook.save_workbook()
    budget_workbook.close_workbook()
