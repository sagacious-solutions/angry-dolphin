import datetime
from datetime import timedelta, date

# def parse_filename(filename):
    

# This gets passed a list of my budget spread sheets, it determines the latest one based on FILENAME formatted as (YEAR-MONTH-DAY) eg.(2021-10-4)
def get_latest_filename(all_filenames):
    TEN_YEARS_AGO_IN_WEEKS = 520
    latest_budget_file_name = datetime.datetime.now() - timedelta(weeks = TEN_YEARS_AGO_IN_WEEKS) # initialize to be old

    print ()    


    for filename in all_filenames :
        if filename.name.startswith(str(datetime.datetime.now().date().year)):
            string_date_array = filename.name.split('.')[0].split('-')
            date_array = []

            for date in string_date_array:
                date_array.append(int(date))

            budget_file_date = datetime.datetime(date_array[0],date_array[1],date_array[2])      

            if budget_file_date > latest_budget_file_name:
                latest_budget_file_name = budget_file_date

    return latest_budget_file_name



# Takes in the DATE OBJECT found for the last budget file name, returns a STRING to create the next budget file
def name_next_sheet (date_of_last, PAY_PERIOD_LENGTH):
    next_budget_date = date_of_last + timedelta(days = PAY_PERIOD_LENGTH)

    return make_file_name(next_budget_date)

# Takes in the DATE OBJECT, returns a STRING with file extension
def make_file_name (date_for_file):
    FILENAME = date_for_file.isoformat().split("T")[0] + ".xlsx"

    return FILENAME

    