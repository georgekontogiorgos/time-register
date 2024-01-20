import pandas as pd
from time import strftime

def get_data_from_file(file_path):
    try:
        # Try to read the CSV file into a DataFrame
        df = pd.read_csv(file_path)

    except FileNotFoundError:
        # Handle the case where the file doesn't exist
        print(f"The file '{file_path}' does not exist. Creating an empty DataFrame.")
        data = {'Timestamp': [],
            'Type': []}
        df = pd.DataFrame(data)
    return df

def get_current_time():
    # Get current date and time
    return strftime("%Y-%m-%d %H:%M:%S")

def is_last_clock_in(data):
    return data.iloc[-1]['Type'] == 'In'

def is_last_clock_out(data):
    return data.iloc[-1]['Type'] == 'Out'

def add_timestamp_entry(entry_type):
    def decorator(func):
        def wrapper(df, timestamp):
            # Create a new row to append
            new_data = {'Timestamp': timestamp, 'Type': entry_type}

            # Convert the new row to a DataFrame
            new_row_df = pd.DataFrame([new_data])

            # Append the new row to the DataFrame
            return pd.concat([df, new_row_df], ignore_index=True)
        
        return wrapper
    return decorator

@add_timestamp_entry('In')
def set_in_timestamp(df, timestamp):
    return df

@add_timestamp_entry('Out')
def set_out_timestamp(df, timestamp):
    return df

def write_data_to_file(df, file_path):
    df.to_csv(file_path, index=False)