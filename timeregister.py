import pandas as pd
from time import strftime, strptime, mktime, localtime
import holidays
from datetime import datetime
import configparser

timestamp_format = "%Y-%m-%d %H:%M:%S"

class TimeRegister:
    def __init__(self):
        self.file_path = ''
        self.load_config('./config')

    def load_config(self, config_file_path):
        # Create a ConfigParser object
        config = configparser.ConfigParser()

        # Read the configuration file
        config.read(config_file_path)

        # Accessing values from the config file
        if 'Settings' in config:
            if 'data_file_path' in config['Settings']:
                self.file_path = config['Settings']['data_file_path']
            else:
                print("Missing file path in the config file.")
        else:
            print("No 'Settings' section found in the config file.")

    def get_data_from_file(self):
        try:
            # Try to read the CSV file into a DataFrame
            df = pd.read_csv(self.file_path)

        except FileNotFoundError:
            # Handle the case where the file doesn't exist
            print(f"The file '{self.file_path}' does not exist. Creating an empty DataFrame.")
            data = {'Date': [],
                    'Time': [],
                    'Type': []}
            df = pd.DataFrame(data)
        return df

    def get_current_time(self):
        # Get current date and time
        return strftime("%H:%M:%S")

    def get_current_date(self):
        # Get current date and time
        return strftime("%Y-%m-%d")

    def is_last_clock_in(self, data):
        return data.iloc[-1]['Type'] == 'In'

    def is_last_clock_out(self, data):
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
    def set_in_timestamp(self, df, date, time):
        return df

    @add_timestamp_entry('Out')
    def set_out_timestamp(self, df, date, time):
        return df

    def write_data_to_file(self, df):
        df.to_csv(self.file_path, index=False)

    def date_range_filter(self, df, start_date, end_date):
        return df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    def get_worked_hours(self, df):    
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

    def _is_weekend(self, date_string):
        # Convert the input date string to a datetime object
        date_object = datetime.strptime(date_string, '%Y-%m-%d')

        # Check if the day of the week is either Saturday (5) or Sunday (6)
        return date_object.weekday() in [5, 6]
    
    def _is_holiday(self, date):
        return True if holidays.country_holidays('SE').get(date) else False

    def get_balance_per_day(self, worked_hours):

        balance_per_day = 0
        balance = {}

        for day in worked_hours:
            if self._is_weekend(day) or self._is_holiday(day):
                balance_per_day += worked_hours[day]
            else:
                # Total balance
                balance_per_day += worked_hours[day] - 8
            balance[day] = balance_per_day
        print(balance)

        return balance            

