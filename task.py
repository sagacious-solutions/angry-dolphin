"""Template robot with Python."""
import time
# import os # so you can import enviroment variables

from RPA.Robocorp.Vault import Vault

secret = Vault().get_secret("credentials")
USER_NAME = secret["username"]
PASSWORD = secret["password"]
BANKING_LOGIN_URL= secret["login_url"]

from RPA.Browser.Selenium import Selenium
VIRTUAL_BROWSER = Selenium()


def minimal_task():
    VIRTUAL_BROWSER.open_available_browser(BANKING_LOGIN_URL)
    # VIRTUAL_BROWSER.click_element_if_visible("q")
    VIRTUAL_BROWSER.input_text_when_element_is_visible("ctl00$MainContentFull$ebLoginControl$txtUserName$txField", USER_NAME + '\n')
    VIRTUAL_BROWSER.input_text_when_element_is_visible("ctl00$MainContentFull$ebLoginControl$txtPassword$txField", PASSWORD + '\n')
    VIRTUAL_BROWSER.click_element_when_visible("TransactionMainContent_MyAccountsControl_rptMembership_rptAccounts_0_rowAccount_0")
    # time.sleep(4)
    time.sleep(10);
    print("Done.")


if __name__ == "__main__":
    minimal_task()




# lib.input_text("id:user-name", username)
# lib.input_text("id:password", password)