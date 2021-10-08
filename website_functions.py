from RPA.Browser.Selenium import Selenium

from RPA.Robocorp.Vault import Vault

import time

VIRTUAL_BROWSER = Selenium()

# This function logs into online banking, Its generalized to reuse later
def login_to_banking():
    credential_secrets = Vault().get_secret("banking")
    USER_NAME = credential_secrets["username"]
    PASSWORD = credential_secrets["password"]
    BANKING_LOGIN_URL= credential_secrets["login_url"]

    VIRTUAL_BROWSER.open_available_browser(BANKING_LOGIN_URL)
    VIRTUAL_BROWSER.input_text_when_element_is_visible("ctl00$MainContentFull$ebLoginControl$txtUserName$txField", USER_NAME + '\n')
    VIRTUAL_BROWSER.input_text_when_element_is_visible("ctl00$MainContentFull$ebLoginControl$txtPassword$txField", PASSWORD + '\n')

# This function retrieves the last paycheque amount
def retrieve_pay_amount():
    transaction_secrets = Vault().get_secret("transactions")
    PAYCHEQUE_DEPOSIT_DESCRIPTION = transaction_secrets["payroll_deposit_label"]

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


# Login to online banking and pay power bill
# Currently not able to complete billpayment due to 2 factor authentication on bank site
# To be completed later if wanted
def pay_power_bill(bill_amount_float) :
    BILL_PAYMENTS_ELEMENT = "Container2_transactionMenus_top_topS_4_liAmg_0"
    HAMBURGER_ELEMENT = "MenuToogle"
    PAY_BILLS_ELEMENT = "Container2_transactionMenus_top_topS_4_topSI_0_aSMG_0"
    POWER_BILL_FIELD_ELEMENT_NAME = "ctl00$ctl00$MainContent$TransactionMainContent$txpTransactions$ctl01$rpBulkPayments$ctl01$txtAmount$txField"
    CONTINUE_BUTTON_ID = "MainContent_TransactionMainContent_txpTransactions_btnNextFlowItem"
    CONFIRM_BUTTON_XPATH = "//*[text() = 'Confirm']"

    login_to_banking()

    # Navigate to bill payments page
    VIRTUAL_BROWSER.click_element_when_visible(HAMBURGER_ELEMENT)
    VIRTUAL_BROWSER.click_element_when_visible(BILL_PAYMENTS_ELEMENT)
    VIRTUAL_BROWSER.click_element_when_visible(PAY_BILLS_ELEMENT)

    # Enter bill_amount_float into bill payee
    VIRTUAL_BROWSER.input_text_when_element_is_visible(POWER_BILL_FIELD_ELEMENT_NAME, str(bill_amount_float))
    VIRTUAL_BROWSER.click_element_when_visible(CONTINUE_BUTTON_ID)    
    
    # Confirm bill payment
    VIRTUAL_BROWSER.click_element_when_visible(CONFIRM_BUTTON_XPATH)
    # Two factor authentication has been implemented by bank. This will need more work to get around that.
    time.sleep(3)

    

def get_power_bill():
    bills_secrets = Vault().get_secret("bills")
    POWER_PROVIDER_LOGIN = bills_secrets["power_provider_login"]
    LOGIN_EMAIL = bills_secrets["email"]
    LOGIN_PASSWORD = bills_secrets["password"]

    VIRTUAL_BROWSER.open_available_browser(POWER_PROVIDER_LOGIN)
    VIRTUAL_BROWSER.input_text_when_element_is_visible("email", LOGIN_EMAIL)
    VIRTUAL_BROWSER.input_text_when_element_is_visible("password", LOGIN_PASSWORD + '\n')

    VIRTUAL_BROWSER.wait_until_element_is_visible("class=bill_amount", 10,"Unable to locate amount due")
    BILL_AMMOUNT_STRING = VIRTUAL_BROWSER.get_element_attribute("class=bill_amount", "innerText")
    BILL_AMOUNT_FLOAT = float(BILL_AMMOUNT_STRING.split('$')[1])


    if BILL_AMOUNT_FLOAT > 0 :
        print("You owe " + BILL_AMMOUNT_STRING + "for power.")
    else :
        print("Nothing currently owed for power")


    return BILL_AMOUNT_FLOAT