import tkinter as tk
from tkinter import messagebox
import timeregister as tr
from time import strftime

def timestamp_decorator(func):
    def wrapper():
        file_path = 'data.csv'
        data = tr.get_data_from_file(file_path)
        try:
            timestamp = tr.get_current_time()
            data, result_text = func(data, timestamp)
            confirmation = messagebox.askquestion("Confirmation", 
                                        "Are you sure you want to register?\n" +
                                        timestamp)
            if confirmation == 'no':
                return
            label.config(text=result_text)
            tr.write_data_to_file(data, file_path)
        except:
            messagebox.showerror("Error", "Register two entries of same type in a row not possible")
    return wrapper

@timestamp_decorator
def clock_in_cmd(data, timestamp):
    if tr.is_last_clock_out(data):
        data = tr.set_in_timestamp(data, timestamp)
        return data, "Clock in registered at\n" + timestamp
    else:
        raise

@timestamp_decorator
def clock_out_cmd(data, timestamp):
    if tr.is_last_clock_in(data):
        data = tr.set_out_timestamp(data, timestamp)
        return data, "Clock out registered at\n" + timestamp
    else:
        raise

def clock():
    current_time = "Welcome to time register program!\n" + strftime('%Y-%m-%d %H:%M:%S')
    label.config(text=current_time)
    label.after(1000, clock)

# Create the main window
window = tk.Tk()
window.title("Time register")
window.geometry("360x100")
window.resizable(False, False)
window.configure(bg="black")

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

clock()

# Run the main loop
window.mainloop()
