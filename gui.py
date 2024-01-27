import tkinter as tk
from tkinter import messagebox
import timeregister
from time import strftime
import matplotlib.pyplot as plt

def timestamp_decorator(func):
    def wrapper():
        data = tr.get_data_from_file()
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
            tr.write_data_to_file(data)
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
    data = tr.get_data_from_file()

    #data = tr.date_range_filter(data, '2024-01-01', '2024-01-09')

    worked_hours = tr.get_worked_hours(data)

    balance = tr.get_balance_per_day(worked_hours)

    dates = list(worked_hours.keys())
    worked_hours_per_day = list(worked_hours.values())
    balance_per_day = list(balance.values())

    fig, (ax1, ax2) = plt.subplots(2, sharex=True, facecolor='black')

    ax1.set_facecolor("black")
    ax2.set_facecolor("black")

    ax1.bar(dates, worked_hours_per_day, color="green")
    ax2.bar(dates, balance_per_day, color=['red' if val < 0 else 'green' for val in balance_per_day])

    axlabel_font={'family': 'Ubuntu Mono', 'weight': 'bold', 'size': 12}

    ##
    # Set labels

    ax1.set_ylabel("Worked hours", color="cyan", fontdict=axlabel_font)
    ax2.set_ylabel("Balance", color="cyan", fontdict=axlabel_font)

    ax2.set_xlabel("Date", color="cyan", fontdict=axlabel_font)
    
    ##
    # Set ticks color

    ax1.tick_params(color='cyan', labelcolor='cyan')
    ax2.tick_params(color='cyan', labelcolor='cyan')

    ##
    # Set axes (spines) colors

    ax1.spines['bottom'].set_color('cyan')
    ax1.spines['left'].set_color('cyan')
    
    ax2.spines['bottom'].set_color('cyan')
    ax2.spines['left'].set_color('cyan')

    plt.setp( ax2.xaxis.get_majorticklabels(), rotation=30, ha="right" )

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
                 font=('Ubuntu Mono', 11, 'bold'))

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

tr = timeregister.TimeRegister()

# Run the main loop
window.mainloop()
