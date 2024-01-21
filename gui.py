import tkinter as tk
from tkinter import messagebox
import timeregister as tr
from time import strftime
import matplotlib.pyplot as plt

def timestamp_decorator(func):
    def wrapper():
        file_path = 'data.csv'
        data = tr.get_data_from_file(file_path)
        try:
            date = tr.get_current_date()
            time = tr.get_current_time()
            data, result_text = func(data, date, time)
            label.after(1000, clock)
            confirmation = messagebox.askquestion("Confirmation", 
                                        "Are you sure you want to register?\n" +
                                        date + " " + time)
            if confirmation == 'no':
                return
            label.config(text=result_text)
            tr.write_data_to_file(data, file_path)
        except:
            messagebox.showerror("Error", "Register two entries of same type in a row not possible")
    return wrapper

@timestamp_decorator
def clock_in_cmd(data, date, time):
    if tr.is_last_clock_out(data):
        data = tr.set_in_timestamp(data, date, time)
        return data, "Clock in registered at\n" + date + time
    else:
        raise

@timestamp_decorator
def clock_out_cmd(data, date, time):
    if tr.is_last_clock_in(data):
        data = tr.set_out_timestamp(data, date, time)
        return data, "Clock out registered at\n" + date + time
    else:
        raise

def balance_cmd():
    data = tr.get_data_from_file('data.csv')

    #data = tr.date_range_filter(data, '2024-01-01', '2024-01-09')

    worked_hours = tr.get_worked_hours(data)

    categories = list(worked_hours.keys())
    values = list(worked_hours.values())
    plt.figure("Balance", facecolor='black')
    ax = plt.axes()
    ax.set_facecolor("black")
    ax.bar(categories, values, color="green")

    ax.set_xlabel("Date", color="cyan")
    plt.xticks(color='cyan')
    
    ax.set_ylabel("Worked hours", color="cyan")
    plt.yticks(color='cyan')

    ax.tick_params(axis='x', color='cyan')
    ax.tick_params(axis='y', color='cyan')

    ax.spines['bottom'].set_color('cyan')
    ax.spines['left'].set_color('cyan')

    plt.setp( ax.xaxis.get_majorticklabels(), rotation=20, ha="right" )

    plt.tight_layout()
    plt.show()

def on_close():
    plt.close('all')
    window.destroy()

def clock():
    current_time = "Welcome to time register program!\n" + strftime('%Y-%m-%d %H:%M:%S')
    label.config(text=current_time)
    label.after(1000, clock)

# Create the main window
window = tk.Tk()
window.title("Time register")
window.geometry("360x150")
window.resizable(False, False)
window.configure(bg="black")
window.protocol("WM_DELETE_WINDOW", on_close)

# Create a label
label = tk.Label(window, 
                 text="Welcome to time register program!",
                 background="black",
                 foreground='cyan',
                 font=('consolas', 11, 'bold'))

label.pack(pady=10)

# Create a button
clockInButton = tk.Button(window, 
                          text="Clock In", 
                          command=clock_in_cmd, 
                          width=10,
                          height=2)

clockInButton.place(x=50, y=50)

clockOutButton = tk.Button(window, 
                           text="Clock Out", 
                           command=clock_out_cmd, 
                           width=10, 
                           height=2)

clockOutButton.place(x=200, y=50)

showBalanceButton = tk.Button(window, 
                           text="Balance", 
                           command=balance_cmd,
                           width=10, 
                           height=2)

showBalanceButton.place(x=50, y=100)

clock()

# Run the main loop
window.mainloop()
