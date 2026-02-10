from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from PIL import Image, ImageTk
import os
import time

#from customwidgets import *
#from confr import *

#import language
#_ = language.get

class ToolTip(object):
    id = None
    tw = None

    def __init__(self, widget, text, mode_HTML = False):
        self.relief = 'solid'
        self.borderwidth = 1
        self.justify = 'left'
        self.color = '#FFFFEA'
        self.widget = widget
        self.text = text
        self.waittime = 500 if not mode_HTML else 1000
        self.wraplength = 270
        self.mode_HTML = mode_HTML
        self.opened = False
        if not self.mode_HTML:
            self.widget.bind("<Leave>", self.leave)
        else:
            self.widget.bind("<Leave>", self.wait_leave)

        self.widget.bind("<ButtonPress>", self.leave)
        self.widget.bind("<Enter>", self.enter)

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def wait_leave(self, event = None):
        if not self.opened:
            self.leave()
            return

        self.widget.after(self.waittime, self.wait_leave)

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def get_height(self, label):
        images = label.text.image_names()
        img_name = label.text.image_cget(images[0], 'image')
        img = label.text.images[img_name]
        return int(img.height()/12)

    def showtip(self, event=None):
        if self.opened:
            return
        self.opened = True
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        if not self.mode_HTML:
            label = Label(self.tw,
                          text=self.text,
                          justify=self.justify,
                          background=self.color,
                          relief=self.relief,
                          borderwidth=self.borderwidth,
                          wraplength = self.wraplength)

            label.pack(ipadx=1)

        else:
            #print(int(12*len(self.text)/self.wraplength))
            label = HTML(self.tw,
                         view = 'noscroll.notable',
                         background=self.color,
                         relief=self.relief,
                         borderwidth=self.borderwidth,
                         width = int(self.wraplength/12),
                         #height = 
                         )

            label.add_content(self.text)
            label.pack(ipadx=1)
            self.tw.bind('<Leave>', self.sortir)
            h = self.get_height(label) + int(12*len(self.text)/self.wraplength) - 1
            label.text.config(height = h)

    def sortir(self, event = None):
        self.opened = False

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            self.opened = False
            tw.destroy()

    def change(self, text):
        self.text = text
