import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import ImageTk, Image
s=tk.Tk()
s.title('ABOUT')
s.geometry('600x515')
tc='''
Intrusion Focus is a Open Source Application developed by us for  
Network intrusion detection systems 
----------------------------------------------------------------

               	   	Intrusion Focus
               	   
        	   Version 1.0.0
        	   
        	   
                By Shreenidhi K Rao
                   Paramatmuni Neha
                   Vinayaka Hegde
                   Vaishnavi R Bhat
                

'''
################################
# create a canvas to display the background image
canvas = tk.Canvas(ss, width=600, height=515)
canvas.pack(fill=tk.BOTH, expand=True)

# load and display the background image

img = Image.open('.resources/images/about.jpg')
img = img.resize((600, 515), Image.ANTIALIAS)
img = ImageTk.PhotoImage(img)
canvas.create_image(0, 0, image=img, anchor=tk.NW)

###################################################

T=scrolledtext.ScrolledText(s,width=69, height=28)
T.insert(tk.INSERT,tc)
T.config(state='disabled')
# place the text widget on top of the image
canvas.create_window( 15, 10, anchor=tk.NW, window=T)

s.resizable(False, False)
s.mainloop()
