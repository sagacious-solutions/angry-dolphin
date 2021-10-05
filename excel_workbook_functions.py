
from RPA.Excel.Files import Files
from RPA.FileSystem import FileSystem

FILE_SYSTEM_CONTROLLER = FileSystem()

# Parameters for modifying spread sheet
BUDGET_SPREADSHEET_DIRECTORY = "./DataSets"
PRIMARY_WORKSHEET = "monthly"
BUDGET_COLUMN_HEIGHT_IN_ROWS = 12
EARLY_MONTH_BILLS = 'C'
LATE_MONTH_BILLS = 'D'
BILLS_FOR_PAY_PERIOD = 'F'
PAY_PERIOD_LENGTH_IN_DAYS = 14


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


def add_bill_to_budget(workbook, BILL_AMMOUNT, BILL_ROW):
    print("adding bill to budget")
    workbook.set_cell_value(BILL_ROW, BILLS_FOR_PAY_PERIOD, BILL_AMMOUNT, PRIMARY_WORKSHEET)

# This updates monthly bills sheet with the bills for this pay period
def update_bills_sheet(EXCEL_FILE_NAME, POWER_BILL_AMMOUNT):
    budget_workbook = Files()
    POWER_BILL_SHEET_ROW = 7

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

    if POWER_BILL_AMMOUNT > 0 :
        add_bill_to_budget(budget_workbook, POWER_BILL_AMMOUNT, POWER_BILL_SHEET_ROW)
    
    budget_workbook.save_workbook()
    budget_workbook.close_workbook()
