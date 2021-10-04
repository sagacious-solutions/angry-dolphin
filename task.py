from file_name_helpers import get_latest_spreadsheet, name_next_sheet


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
PAY_PERIOD_LENGTH_IN_DAYS = 14 


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
    all_budget_spreadsheets = FILE_SYSTEM_CONTROLLER.list_files_in_directory(budget_spreadsheet_directory)
    date_of_last_pay = get_latest_spreadsheet(all_budget_spreadsheets)    

    NEW_SPREADSHEET_NAME = name_next_sheet(date_of_last_pay, PAY_PERIOD_LENGTH_IN_DAYS)

    print (NEW_SPREADSHEET_NAME)


if __name__ == "__main__":
    # retrieve_pay_amount()
    clone_budget_spreadsheet()