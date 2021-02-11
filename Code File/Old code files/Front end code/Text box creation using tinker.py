# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 15:01:25 2020

@author: surendra_dattatrey
"""

import tkinter as tk
from tkinter import ttk
 
 
window = tk.Tk()
 
window.title("Enter Job description:")
window.minsize(600,400)
 
def clickMe():
    label.configure(text= 'Hello ' + name.get())
 
label = ttk.Label(window, text = "Enter Your Name")
label.grid(column = 0, row = 0)
 
 
name = tk.StringVar()
nameEntered = ttk.Entry(window, width = 200, textvariable = name)
nameEntered.grid(column = 0, row = 100)
 
 
button = ttk.Button(window, text = "Click Me", command = clickMe)
button.grid(column= 0, row = 2)
 
window.mainloop()
