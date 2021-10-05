from RPA.Browser.Selenium import Selenium

from RPA.Robocorp.Vault import Vault

credential_secrets = Vault().get_secret("banking")
USER_NAME = credential_secrets["username"]
PASSWORD = credential_secrets["password"]
BANKING_LOGIN_URL= credential_secrets["login_url"]

transaction_secrets = Vault().get_secret("transactions")
PAYCHEQUE_DEPOSIT_DESCRIPTION = transaction_secrets["payroll_deposit_label"]

VIRTUAL_BROWSER = Selenium()

# This function logs into online banking, Its generalized to reuse later
def login_to_banking():
    VIRTUAL_BROWSER.open_available_browser(BANKING_LOGIN_URL)
    VIRTUAL_BROWSER.input_text_when_element_is_visible("ctl00$MainContentFull$ebLoginControl$txtUserName$txField", USER_NAME + '\n')
    VIRTUAL_BROWSER.input_text_when_element_is_visible("ctl00$MainContentFull$ebLoginControl$txtPassword$txField", PASSWORD + '\n')

# This function retrieves the last paycheque amount
def retrieve_pay_amount():
    login_to_banking()

    VIRTUAL_BROWSER.click_element_when_visible("TransactionMainContent_MyAccountsControl_rptMembership_rptAccounts_0_rowAccount_0")

    DESCRIPTION_ELEMENT_ID = "MainContent_TransactionMainContent_txpTransactions_ctl01_transactionStatementsControl_flwTransactionStatements_GvTransactionStatements_lblDescription_"
    VALUE_ELEMENT_ID = "MainContent_TransactionMainContent_txpTransactions_ctl01_transactionStatementsControl_flwTransactionStatements_GvTransactionStatements_lblAmount_"
    ROW_COUNT = VIRTUAL_BROWSER.get_element_count("class:item")

    # looks through each individual transaction listed to see if the description matches a pay roll deposit
    for x in range(0, ROW_COUNT):
        if VIRTUAL_BROWSER.is_element_attribute_equal_to(DESCRIPTION_ELEMENT_ID + str(x), "innerText", PAYCHEQUE_DEPOSIT_DESCRIPTION) :
            PAYCHEQUE_AMMOUNT = VIRTUAL_BROWSER.get_element_attribute(VALUE_ELEMENT_ID + str(x), "innerText")
            print("You have aquired " + str(PAYCHEQUE_AMMOUNT) + "CAD in currency")
    
    print("Done.")
    return PAYCHEQUE_AMMOUNT