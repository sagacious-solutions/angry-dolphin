# ## Using Vault Example
# This simple robot shows how to use the Vault functionality locally and in Control Room.
#
# > NOTE: This example needs some manual configuration steps. You can find the full tutorial and instructions on [Robocorp's documentation site](https://robocorp.com/docs/development-guide/variables-and-secrets/vault).
#
#
# In Robocorp Lab, click on the `>> Run all` button above to run the whole example, or you can execute each cell by using the `> Run cell` button.

*** Settings ***
Documentation     Using the vault functionality locally and in Control Room.
Library           RPA.Robocorp.Vault
Variables         variables.py

*** Tasks ***
Get and log the value of the vault secrets using the Get Secret keyword
    ${secret}=    Get Secret    credentials
    # Note: in real robots, you should not print secrets to the log. this is just for demonstration purposes :)
    Log    ${secret}[username]
    Log    ${secret}[password]

*** Tasks ***
Get and log the value of the vault secrets using the imported variables file
    # Note: in real robots, you should not print secrets to the log. this is just for demonstration purposes :)
    # This works because we are importing the `variables.py` file:
    Log    ${USER_NAME}
    Log    ${PASSWORD}
