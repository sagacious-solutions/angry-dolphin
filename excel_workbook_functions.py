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


# This gets the last pay period workbook and makes a copy of it for the current pay period
def clone_budget_spreadsheet():
    file_list_from_directory = FILE_SYSTEM_CONTROLLER.list_files_in_directory(BUDGET_SPREADSHEET_DIRECTORY)
    date_of_last_pay = get_latest_filename(file_list_from_directory)    

    LAST_SPREADSHEET_NAME = make_file_name(date_of_last_pay)
    NEW_SPREADSHEET_NAME = name_next_sheet(date_of_last_pay, PAY_PERIOD_LENGTH_IN_DAYS)

    FILE_SYSTEM_CONTROLLER.copy_file(BUDGET_SPREADSHEET_DIRECTORY + '/' + LAST_SPREADSHEET_NAME, BUDGET_SPREADSHEET_DIRECTORY + '/' + NEW_SPREADSHEET_NAME)

    print (NEW_SPREADSHEET_NAME, " has been created.")
    return NEW_SPREADSHEET_NAME

# This gets the sheet requested from the opened workbook and returns it as a table
def make_table_from_workbook_sheet(WORKBOOK_FILENAME):
    budget_workbook = Files()

    try:
        budget_workbook.open_workbook(BUDGET_SPREADSHEET_DIRECTORY + '/' + WORKBOOK_FILENAME)

        return budget_workbook.read_worksheet_as_table(PRIMARY_WORKSHEET)
    except:
        print ("We were unable to open a workbook named", WORKBOOK_FILENAME)        
    finally: 
        budget_workbook.close_workbook()


# This updates the newly opened sheet with correct bills for the time of the month
def update_budget_table(budget_table, EXCEL_FILE_NAME):
    print("Updating budget spread sheet for", EXCEL_FILE_NAME)

    PAY_DATE_DAY = int(EXCEL_FILE_NAME.split('-')[2].split('.')[0])

    print(PAY_DATE_DAY)

    if PAY_DATE_DAY <= 15 :
        print("EARLY PAY")
        updated_table = copy_table_column(budget_table, LATE_MONTH_BILLS, BILLS_FOR_PAY_PERIOD)
    else :
        print ("late pay")
        updated_table = copy_table_column(budget_table, EARLY_MONTH_BILLS, BILLS_FOR_PAY_PERIOD)

    return updated_table    


# This function will copy a column of values from one column to another
def copy_table_column(sheet, source, destination):
    START_AFTER_HEADER = 1
    
    for row in range(START_AFTER_HEADER, BUDGET_COLUMN_HEIGHT_IN_ROWS):
        source_value = TABLE_MANIPULATOR.get_table_cell(sheet, row, source)
        # TABLE_MANIPULATOR.set_table_cell(row, destination, source_value)
        TABLE_MANIPULATOR.set_table_cell(sheet ,row, destination, source_value)

    return sheet

    
def update_budget_workbook_with_new_table(EXCEL_FILE_NAME, new_budget_table):
    HEADER = False
    EXIST_OK = False
    budget_workbook = Files()
    
    try:
        budget_workbook.open_workbook(BUDGET_SPREADSHEET_DIRECTORY + '/' + EXCEL_FILE_NAME)

        budget_workbook.create_worksheet("BUDGET", new_budget_table, EXIST_OK, HEADER)
        # budget_workbook.append_rows_to_worksheet(new_budget_table, PRIMARY_WORKSHEET, HEADER)

        budget_workbook.save_workbook()

        print("Workbook " + EXCEL_FILE_NAME + " has been updated!")
    except:
        print("Unable to complete @update_budget_workbook_with_new_table")
    finally:
        budget_workbook.close_workbook()
