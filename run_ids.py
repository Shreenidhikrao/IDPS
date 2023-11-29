import datetime
import os
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import psutil
filename=""

with open('temp/admin.pass', 'r') as file:
    sudo_passwd = file.read()


foldername = 'logs'


def run_IF(duration_secs, process_lock, sudo_passwd, filename, interface_var):
    if duration_secs>0:
        if filename.endswith('.conf'):
            if interface_var.get():
                with process_lock:
                    datetime_string = datetime.datetime.now().strftime("%d-%m-%y@%H.%M.%S")
                    new_folderpath = f'{foldername}/{datetime_string}'
                    os.system(f'sudo mkdir {new_folderpath}')
                    command = f'sudo python3 /mnt/nvmen1p3/IntrusionFocus/Learningmodel/extract.py'
                    command = f'sudo python3 /mnt/nvmen1p3/IntrusionFocus/Learningmodel/main.py'
                    s_process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, preexec_fn=os.setsid)
                    s_process.stdin.write(sudo_passwd.encode('utf-8') + b'\n')
                    s_process.stdin.flush()
                    

def stop_IF(window, sudo_password):
    password_window = tk.Tk()
    password_window.title("Password:")

    password_label = tk.Label(password_window, text="Enter the OTP to stop  manually:")
    password_label.pack(padx=20, pady=20)

    password_entry = tk.Entry(password_window, show="*")
    password_entry.pack(padx=20, pady=10)

    def verify_password():
        entered_password = password_entry.get()

        # Run the pkill command only if the entered password is correct
        if entered_password == sudo_password:
            p = subprocess.run(['sudo', '-S', 'pkill', 's'])
            password_window.destroy()
            window.destroy()
            messagebox.showinfo('s stopped', 'Program stopped successfully.')
            

        else:
            messagebox.showerror('Incorrect Password', 'Incorrect password entered. Please try again.')
            password_entry.delete(0, tk.END)

    password_button = tk.Button(password_window, text="Stop s", command=verify_password)
    password_button.pack(padx=20, pady=10)
    password_window.resizable(False,False)
    password_window.mainloop()


def show_s_window():
    input_window = tk.Tk()
    input_window.title('Run Intrusion Focus')
    input_window.geometry('495x300')

    label = tk.Label(input_window, text='Enter the number of hours to run IF:')
    label.grid(row=0, column=0, padx=10, pady=15)

    entry = tk.Entry(input_window, width=5)
    entry.grid(row=0, column=1, padx=5, pady=10)

    interface_frame = tk.Frame(input_window)
    interface_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

    # Label for network interface dropdown menu
    interface_label = tk.Label(interface_frame, text='Select network interface to listen on:')
    interface_label.grid(row=0, column=0, padx=5, pady=10)

    # Dropdown menu for network interfaces
    global interface_var
    interface_var = tk.StringVar()
    interface_menu = tk.OptionMenu(interface_frame, interface_var, *psutil.net_if_addrs().keys())
    interface_menu.grid(row=0, column=1, padx=5, pady=10)

    # File selection button and label
    file_frame = tk.Frame(input_window)
    file_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

    file_label = tk.Label(file_frame, text='')
    file_label.grid(row=2, column=1, padx=5, pady=10)

    def select_file():
        global filename

    file_button = tk.Button(file_frame, text='Ready', command=select_file)
    file_button.grid(row=2, column=0, padx=10, pady=10)



    def start_IF():
        
        time=entry.get()    #time entered
        try:
        # check if any variable is missing
            if time and interface_var and filename !="":
                try:
                    time = float(time)
                    if time >= 0 and (time.is_integer() or time != int(time)):
                        duration_secs = int(time * 60 * 60)
                        input_window.destroy()
                        # Prompt user for sudo password
                        sudo_password = tk.simpledialog.askstring("Password Initialisation", "Enter your OTP :\n(⚠️ Disclaimer: Remember this password\n )\n", show='*')

                        # Check if password is correct
                        p = subprocess.run(['sudo', '-S', 'true'], input=bytes(sudo_password + '\n', 'utf-8'), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        if p.returncode != 0:
                            messagebox.showerror("Incorrect Password", "The password you entered is incorrect. Please try again.")
                            return

                       
                        process_lock = threading.Lock()
                        s_thread = threading.Thread(target=run_s, args=(duration_secs, process_lock, sudo_passwd,filename,interface_var))
                        s_thread.start()

                        status_window = tk.Tk()
                        status_window.title("Intrusion Focus is Running")

                        status_label = tk.Label(status_window, text="Intrusion Focus is currently running.")
                        status_label.pack(padx=20, pady=20)

                        status_button = tk.Button(status_window, text="Stop IF", command=lambda: stop_IF(status_window, sudo_password))
                        status_button.pack(padx=20, pady=10)


                    else:
                        messagebox.showerror("Error", "Enter a valid time")
                except ValueError:
                    messagebox.showerror("Error", "Enter a valid time")
            else:
                messagebox.showerror("Error", "Enter Values") 
        except ValueError:
            messagebox.showerror("Error", "Enter Values")        

    button_active_bg, button_active_fg = '#f00', '#fff'
    start_button = tk.Button(input_window, text="Start IF",relief='groove', cursor='hand2', activebackground=button_active_bg,
                             activeforeground=button_active_fg,command=start_IF,width=58,height=5)
    start_button.place(x=3,y=200)
    input_window.resizable(False,False)
    input_window.mainloop()

if not os.path.exists(foldername):
    os.system(f'sudo mkdir {foldername}')

i=3
try:
    while i>0:
        sudo_password = tk.simpledialog.askstring("Password", "\nEnter your administrator password:\n", show='*')

        if sudo_password==sudo_passwd:
            i=0
            show_s_window()
        elif(sudo_password is None):
            exit()
        elif(sudo_password==""):
            messagebox.showerror("Error","Enter password")
        else:
            messagebox.showerror("Error", "ⓘ Incorrect password, try again. (Attempt:"+str(i)+")")
            i=i-1
except tk.TclError:
    exit()
    
