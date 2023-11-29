import os
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import ImageTk, Image

with open('.resources/temp/admin.pass', 'r') as file:
    sudo_passwd = file.read()

i=3
try:
    while i>0:
        sudo_password = tk.simpledialog.askstring("Password", "\nEnter your administrator password:\n", show='*')

        if sudo_password==sudo_passwd:
            try:
                i=0
                # create the main window
                root = tk.Tk()
                root.title('Intrusion focus')
                root.geometry('1200x650+1+1')
                root.resizable(False, False)


                # define the functions for the buttons
                def run_ids():
                    command='sudo -S python3 .resources/run_ids.py'
                    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, preexec_fn=os.setsid)
                    process.stdin.write(sudo_password.encode('utf-8') + b'\n')
                    process.stdin.flush()

                def exit_app():
                    if messagebox.askokcancel(title='Exit', message='Are you sure?'):
                        root.destroy()

                def log_analyser():
                    command="sudo -S python3 .resources/loganalyzer.py"
                    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, preexec_fn=os.setsid)
                    process.stdin.write(sudo_password.encode('utf-8') + b'\n')
                    process.stdin.flush()

                def about():
                    command="python3 .resources/about.py"
                    os.system(command)

                
                # create the buttons
                button_width, button_height = 20, 2
                button_font = ('TkDefaultFont', 15)
                button_bg, button_fg = '#000', '#fff'
                button_active_bg, button_active_fg = '#f00', '#fff'
                run_button = tk.Button(root, width=button_width, height=button_height, text='LOG ANALYZER', font=button_font,
                                    bg=button_bg, fg=button_fg, relief='groove', cursor='hand2', activebackground=button_active_bg,
                                    activeforeground=button_active_fg, command=log_analyser)
                run_button.place(x=480, y=330)

                run_button = tk.Button(root, width=button_width, height=button_height, text='RUN', font=button_font,
                                    bg=button_bg, fg=button_fg, relief='groove', cursor='hand2', activebackground=button_active_bg,
                                    activeforeground=button_active_fg, command=run_ids)
                run_button.place(x=480, y=230)


                # create the menu bar
                menu_bar = tk.Menu(root)

                file_menu = tk.Menu(menu_bar, tearoff=0)

                file_menu.add_command(label='Exit', command=exit_app)
                menu_bar.add_cascade(label='Option', menu=file_menu)
                file_menu1 = tk.Menu(menu_bar, tearoff=0)
                file_menu1.add_command(label='Intrusion Focus', command=about)
                menu_bar.add_cascade(label='About', menu=file_menu1)
                root.config(menu=menu_bar)
                root.mainloop()
            except tk.TclError:
                break
        elif(sudo_password is None):
            exit()
        elif(sudo_password==""):
            messagebox.showerror("Error","Enter password")
        else:
            i=i-1
            messagebox.showerror("Error", "ⓘ Incorrect password, try again. (Attempts Left:"+str(i)+")")
            
except tk.TclError:
    exit()
