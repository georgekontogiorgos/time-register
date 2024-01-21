import pandas as pd
from time import strftime, strptime, mktime, localtime
from holidays import CountryHoliday
from datetime import date

timestamp_format = "%Y-%m-%d %H:%M:%S"

def get_data_from_file(file_path):
    try:
        # Try to read the CSV file into a DataFrame
        df = pd.read_csv(file_path)

    except FileNotFoundError:
        # Handle the case where the file doesn't exist
        print(f"The file '{file_path}' does not exist. Creating an empty DataFrame.")
        data = {'Date': [],
                'Time': [],
                'Type': []}
        df = pd.DataFrame(data)
    return df

def get_current_time():
    # Get current date and time
    return strftime("%H:%M:%S")

def get_current_date():
    # Get current date and time
    return strftime("%Y-%m-%d")

def is_last_clock_in(data):
    return data.iloc[-1]['Type'] == 'In'

def is_last_clock_out(data):
    if data.empty:
        return True
    else:
        return data.iloc[-1]['Type'] == 'Out'

def add_timestamp_entry(entry_type):
    def decorator(func):
        def wrapper(df, date, time):
            # Create a new row to append
            new_data = {'Date': date, 'Time': time, 'Type': entry_type}

            # Convert the new row to a DataFrame
            new_row_df = pd.DataFrame([new_data])

            # Append the new row to the DataFrame
            return pd.concat([df, new_row_df], ignore_index=True)
        
        return wrapper
    return decorator

@add_timestamp_entry('In')
def set_in_timestamp(df, date, time):
    return df

@add_timestamp_entry('Out')
def set_out_timestamp(df, date, time):
    return df

def write_data_to_file(df, file_path):
    df.to_csv(file_path, index=False)

def date_range_filter(df, start_date, end_date):
    return df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

def get_worked_hours(df):    
    worked_hours = {}
    for index, row in df.iterrows():
        date = row['Date']
        time = row['Time']
        entry_type = row['Type']
        entry_epoch = mktime(strptime(date + " " + time, "%Y-%m-%d %H:%M:%S"))

        if entry_type == 'In':
            clock_in_time = entry_epoch
            last_date = date
        elif entry_type == 'Out':
            if date == last_date:
                worked_hours_temp = (entry_epoch - clock_in_time)/3600
                try:
                    worked_hours[date] += worked_hours_temp
                except:
                    worked_hours[date] = worked_hours_temp
            else:
                last_day_out_epoch = mktime(strptime(last_date + " 23:59:59", "%Y-%m-%d %H:%M:%S"))
                worked_hours[last_date] = (last_day_out_epoch - clock_in_time)/3600
                new_day_in_epoch = mktime(strptime(date + " 0:0:0", "%Y-%m-%d %H:%M:%S"))
                worked_hours[date] = (entry_epoch - new_day_in_epoch)/3600
        else:
            raise
    return worked_hours
