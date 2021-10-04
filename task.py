import datetime
from datetime import timedelta

from RPA.Robocorp.Vault import Vault
from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from RPA.FileSystem import FileSystem

credential_secrets = Vault().get_secret("banking")
USER_NAME = credential_secrets["username"]
PASSWORD = credential_secrets["password"]
BANKING_LOGIN_URL= credential_secrets["login_url"]

transaction_secrets = Vault().get_secret("transactions")
PAYCHEQUE_DEPOSIT_DESCRIPTION = transaction_secrets["payroll_deposit_label"]

budget_spreadsheet_directory = "./DataSets"

VIRTUAL_BROWSER = Selenium()
FILE_SYSTEM_CONTROLLER = FileSystem()


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

# This gets passed a list of my budget spread sheets, it determines the latest one based on FILENAME formatted as (YEAR-MONTH-DAY) eg.(2021-10-4)
def get_latest_spreadsheet(sheets):
    TEN_YEARS_AGO_IN_WEEKS = 520
    latest_budget_file_name = datetime.datetime.now() - timedelta(weeks = TEN_YEARS_AGO_IN_WEEKS)

    for sheet in sheets :
        string_date_array = sheet.name.split('.')[0].split('-')
        date_array = []

        for date in string_date_array:
            date_array.append(int(date))

        budget_file_date = datetime.datetime(date_array[0],date_array[1],date_array[2])      

        if budget_file_date > latest_budget_file_name:
            latest_budget_file_name = budget_file_date

    print("Here is latest file", latest_budget_file_name)
    return latest_budget_file_name


def clone_budget_spreadsheet():
    all_budget_spreadsheets = FILE_SYSTEM_CONTROLLER.list_files_in_directory(budget_spreadsheet_directory)
    get_latest_spreadsheet(all_budget_spreadsheets)

if __name__ == "__main__":
    # retrieve_pay_amount()
    clone_budget_spreadsheet()