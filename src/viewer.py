from tkinter import *

def give_tex(master, text):
    tk = Toplevel(master)
    tk.transient(master)
    tk.rowconfigure(0, weight = 1)
    tk.columnconfigure(0, weight = 1)
    tk.title('Code TeX')
    tt = Text(tk)
    tt.grid(sticky = 'nswe')
    tt.insert('end', text)
    tk.wait_window()
