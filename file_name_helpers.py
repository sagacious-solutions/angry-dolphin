import datetime
from datetime import timedelta, date

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



# Takes in the DATE OBJECT found for the last budget file name, returns a STRING to create the next budget file
def name_next_sheet (date_of_last, PAY_PERIOD_LENGTH):
    next_budget_date = date_of_last + timedelta(days = PAY_PERIOD_LENGTH)
    next_budget_filename = next_budget_date.isoformat()

    return next_budget_filename.split("T")[0] + ".xlsx"

    