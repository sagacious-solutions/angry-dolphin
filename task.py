import time
# import os # so you can import enviroment variables

from RPA.Robocorp.Vault import Vault

credential_secrets = Vault().get_secret("banking")
USER_NAME = credential_secrets["username"]
PASSWORD = credential_secrets["password"]
BANKING_LOGIN_URL= credential_secrets["login_url"]

transaction_secrets = Vault().get_secret("transactions")
PAYCHEQUE_DEPOSIT = transaction_secrets["payroll_deposit_label"]


from RPA.Browser.Selenium import Selenium
VIRTUAL_BROWSER = Selenium()


def retrieve_pay_amount():
    VIRTUAL_BROWSER.open_available_browser(BANKING_LOGIN_URL)
    # VIRTUAL_BROWSER.click_element_if_visible("q")
    VIRTUAL_BROWSER.input_text_when_element_is_visible("ctl00$MainContentFull$ebLoginControl$txtUserName$txField", USER_NAME + '\n')
    VIRTUAL_BROWSER.input_text_when_element_is_visible("ctl00$MainContentFull$ebLoginControl$txtPassword$txField", PASSWORD + '\n')
    VIRTUAL_BROWSER.click_element_when_visible("TransactionMainContent_MyAccountsControl_rptMembership_rptAccounts_0_rowAccount_0")

    DESCRIPTION_ELEMENT_ID = "MainContent_TransactionMainContent_txpTransactions_ctl01_transactionStatementsControl_flwTransactionStatements_GvTransactionStatements_lblDescription_"
    VALUE_ELEMENT_ID = "MainContent_TransactionMainContent_txpTransactions_ctl01_transactionStatementsControl_flwTransactionStatements_GvTransactionStatements_lblAmount_"
    ROW_COUNT = VIRTUAL_BROWSER.get_element_count("class:item")

    # looks through each individual transaction listed to see if the description matches a pay roll deposit
    for x in range(0, ROW_COUNT):
        if VIRTUAL_BROWSER.is_element_attribute_equal_to(DESCRIPTION_ELEMENT_ID + str(x), "innerText", PAYCHEQUE_DEPOSIT) :
            PAYCHEQUE_AMMOUNT = VIRTUAL_BROWSER.get_element_attribute(VALUE_ELEMENT_ID + str(x), "innerText")
            print("You have aquired " + str(PAYCHEQUE_AMMOUNT) + "CAD in currency")
    
    print("Done.")


if __name__ == "__main__":
    retrieve_pay_amount()




# lib.input_text("id:user-name", username)
# lib.input_text("id:password", password)