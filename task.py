from file_name_helpers import get_latest_spreadsheet, name_next_sheet, make_file_name


from RPA.Robocorp.Vault import Vault
from RPA.Browser.Selenium import Selenium

from RPA.Excel.Files import Files
from RPA.Tables import Tables

from RPA.FileSystem import FileSystem

credential_secrets = Vault().get_secret("banking")
USER_NAME = credential_secrets["username"]
PASSWORD = credential_secrets["password"]
BANKING_LOGIN_URL= credential_secrets["login_url"]

transaction_secrets = Vault().get_secret("transactions")
PAYCHEQUE_DEPOSIT_DESCRIPTION = transaction_secrets["payroll_deposit_label"]

BUDGET_SPREADSHEET_DIRECTORY = "./DataSets"

VIRTUAL_BROWSER = Selenium()
FILE_SYSTEM_CONTROLLER = FileSystem()
PAY_PERIOD_LENGTH_IN_DAYS = 14
PRIMARY_WORKSHEET = "monthly"


# def retrieve_pay_amount():
#     VIRTUAL_BROWSER.open_available_browser(BANKING_LOGIN_URL)
#     # VIRTUAL_BROWSER.click_element_if_visible("q")
#     VIRTUAL_BROWSER.input_text_when_element_is_visible("ctl00$MainContentFull$ebLoginControl$txtUserName$txField", USER_NAME + '\n')
#     VIRTUAL_BROWSER.input_text_when_element_is_visible("ctl00$MainContentFull$ebLoginControl$txtPassword$txField", PASSWORD + '\n')
#     VIRTUAL_BROWSER.click_element_when_visible("TransactionMainContent_MyAccountsControl_rptMembership_rptAccounts_0_rowAccount_0")

#     DESCRIPTION_ELEMENT_ID = "MainContent_TransactionMainContent_txpTransactions_ctl01_transactionStatementsControl_flwTransactionStatements_GvTransactionStatements_lblDescription_"
#     VALUE_ELEMENT_ID = "MainContent_TransactionMainContent_txpTransactions_ctl01_transactionStatementsControl_flwTransactionStatements_GvTransactionStatements_lblAmount_"
#     ROW_COUNT = VIRTUAL_BROWSER.get_element_count("class:item")

#     # looks through each individual transaction listed to see if the description matches a pay roll deposit
#     for x in range(0, ROW_COUNT):
#         if VIRTUAL_BROWSER.is_element_attribute_equal_to(DESCRIPTION_ELEMENT_ID + str(x), "innerText", PAYCHEQUE_DEPOSIT_DESCRIPTION) :
#             PAYCHEQUE_AMMOUNT = VIRTUAL_BROWSER.get_element_attribute(VALUE_ELEMENT_ID + str(x), "innerText")
#             print("You have aquired " + str(PAYCHEQUE_AMMOUNT) + "CAD in currency")
    
#     print("Done.")



def clone_budget_spreadsheet():
    all_budget_spreadsheets = FILE_SYSTEM_CONTROLLER.list_files_in_directory(BUDGET_SPREADSHEET_DIRECTORY)
    date_of_last_pay = get_latest_spreadsheet(all_budget_spreadsheets)    

    LAST_SPREADSHEET_NAME = make_file_name(date_of_last_pay)
    NEW_SPREADSHEET_NAME = name_next_sheet(date_of_last_pay, PAY_PERIOD_LENGTH_IN_DAYS)

    FILE_SYSTEM_CONTROLLER.copy_file(BUDGET_SPREADSHEET_DIRECTORY + '/' + LAST_SPREADSHEET_NAME, BUDGET_SPREADSHEET_DIRECTORY + '/' + NEW_SPREADSHEET_NAME)

    print (NEW_SPREADSHEET_NAME, " has been created.")
    return NEW_SPREADSHEET_NAME

def retrieve_budget_sheet(WORKBOOK_FILENAME):
    budget_workbook = Files()
    budget_workbook.open_workbook(BUDGET_SPREADSHEET_DIRECTORY + '/' + WORKBOOK_FILENAME)
    try:
        return budget_workbook.read_worksheet(PRIMARY_WORKSHEET)
    finally:
        budget_workbook.close_workbook()

def update_budget_data(sheet):
    print(sheet)



if __name__ == "__main__":
    # retrieve_pay_amount()
    EXCEL_FILE_NAME = clone_budget_spreadsheet()
    monthly_budget_sheet = retrieve_budget_sheet(EXCEL_FILE_NAME)
    update_budget_data(monthly_budget_sheet)

