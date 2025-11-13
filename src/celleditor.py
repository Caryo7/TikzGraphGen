from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from PIL import Image, ImageTk
import os
import time

#from customwidgets import *
from tooltip import *
#from confr import *

#import language
#_ = language.get

class ComboPopup(ttk.Combobox):
    def __init__(self, parent, iid, col, cmd_begin, cmd, **kw):
        super().__init__(parent, **kw)
        self.tv = parent
        self.iid = iid
        self.col = col
        self.cmd = cmd
        if col != '#0':
            self.old_text = self.tv.set(iid, col)
        else:
            self.old_text = self.tv.item(iid)['text']

        self.set(self.old_text)
        cmd_begin()
        self.data = self.old_text
        ToolTip(self, self.old_text)

        self.focus()
        self.bind("<Escape>", self.on_escape)
        self.bind("<<ComboboxSelected>>", self.new_selection)
        self.bind("<Return>", self.on_return)

    def new_selection(self, event=None):
        self.data = self.get()
        if self.col != '#0':
            self.tv.set(self.iid, self.col, self.data)
        else:
            self.tv.item(self.iid, text = self.data)

        self.close(True)

    def on_return(self, event):
        self.close()

    def on_escape(self, event):
        self.tv.set(self.iid, self.col, self.old_text)
        self.close(True)

    def close(self, force = False):
        if not force:
            self.new_selection()

        self.destroy()
        for c in self.cmd:
            c()

class EntryPopup(ttk.Entry):
    def __init__(self, parent, iid, col, text, cmd_begin, cmd, **kw):
        super().__init__(parent, **kw)
        self.tv = parent
        self.iid = iid
        self.col = col
        self.cmd = cmd
        cmd_begin()

        self.insert(0, text)
        self.select_range(0, END)
        ToolTip(self, text)
        self.data = text

        self.focus_force()
        self.bind("<Return>", self.on_return)
        self.bind("<Escape>", self.on_escape)

    def on_return(self, event):
        self.close()

    def on_escape(self, event):
        self.destroy()
        for c in self.cmd:
            c()

    def close(self):
        self.data = self.get()
        if self.col == '#0':
            self.tv.item(self.iid, text=self.data)
        else:
            self.tv.set(self.iid, self.col, self.data)

        self.destroy()
        for c in self.cmd:
            c()

class TextPopup(Text):
    def __init__(self, parent, iid, col, text, cmd_begin, cmd, **kw):
        super().__init__(parent, wrap = 'word', **kw)
        self.tv = parent
        self.iid = iid
        self.col = col
        self.cmd = cmd
        self.ttc = False
        self.ttr = False
        cmd_begin()

        self.insert('0.0', text)
        self.tag_add('sel', '0.0', 'end-1c')
        ToolTip(self, text)
        self.data = text

        self.focus_force()
        self.bind("<KeyPress>", self.kp)
        self.bind("<KeyRelease>", self.kr)
        self.bind("<Escape>", self.on_escape)

    def kp(self, event):
        if event.keysym in ('Control_L', 'Control_R'):
            self.ttc = True
            self.check()
        elif event.keysym in ('Return'):
            self.ttr = True
            self.check()

    def kr(self, event):
        if event.keysym in ('Control_L', 'Control_R'):
            self.ttc = False
            self.check()
        elif event.keysym in ('Return'):
            self.ttr = False
            self.check()

    def check(self):
        if self.ttc and self.ttr:
            self.close()

    def on_escape(self, event):
        self.destroy()
        for c in self.cmd:
            c()

    def close(self):
        self.data = self.get('0.0', 'end')
        self.data = self.data.rstrip('\n')
        if self.col == '#0':
            self.tv.item(self.iid, text=self.data)
        else:
            self.tv.set(self.iid, self.col, self.data)

        self.destroy()
        for c in self.cmd:
            c()

class CellEditor:
    FAVORI_ON  = '★'
    FAVORI_OFF = '☆'

    def __init__(self, widget, actions = {}, command = lambda: None, beg_cmd = lambda: None):
        self.widget = widget
        self.able_tooltip = IntVar(value = 1)
        self.popup_ready = False
        self.widget.bind('<Double-Button-1>', self.edit)
        self.widget.bind('<Button-1>', self.button_pressed)
        self.actions = actions
        self.command = command
        self.beg_cmd = beg_cmd

    def getText(self, rowid, column):
        if column != '#0':
            return self.widget.item(rowid)['values'][int(column.replace('#', ''))-1]
        else:
            return self.widget.item(rowid)['text']

    def edit(self, event):
        if not self.able_tooltip.get():
            return

        self.popup_ready = False
        self.able_tooltip.set(0)
        rowid = self.widget.identify_row(event.y)
        column = self.widget.identify_column(event.x)
        try:
            x, y, width, height = self.widget.bbox(rowid, column)
        except:
            self.able_tooltip.set(1)
            return

        pady = height / 2

        skip = False
        if column in self.actions:
            cmd = self.actions[column]
            if cmd['type'] == 'Entry':
                text = self.getText(rowid, column)
                self.entryPopup = EntryPopup(self.widget, rowid, column, text, cmd_begin = self.beg_cmd, cmd = [lambda: self.able_tooltip.set(1), self.command])
                skip = True
                t = 'Entry'

            elif cmd['type'] == 'Text':
                text = self.getText(rowid, column)
                self.entryPopup = TextPopup(self.widget, rowid, column, text, cmd_begin = self.beg_cmd, cmd = [lambda: self.able_tooltip.set(1), self.command])
                skip = True
                t = 'Text'

            elif cmd['type'] == 'Combo':
                vals = cmd['values']
                if 'restrict' in cmd.keys():
                    vals = vals[self.getText(rowid, cmd['restrict'])]

                self.entryPopup = ComboPopup(self.widget, rowid, column, cmd_begin = self.beg_cmd, cmd = [lambda: self.release_combo(rowid, column, cmd), self.command], values=vals)
                skip = True
                t = 'Combo'

        if not skip:
            self.able_tooltip.set(1)
            self.popup_ready = False
            return

        if t == 'Text':
            self.entryPopup.place(x=x, y=y + pady, width=width, anchor='nw')
        else:
            self.entryPopup.place(x=x, y=y + pady, width=width, height=1.25 * height, anchor='w')

        self.popup_ready = True

    def release_combo(self, rowid, column, args):
        self.able_tooltip.set(1)
        if 'autoinsert' in args.keys():
            col_name = self.getText(rowid, args['restrict'])
            col, ai = args['autoinsert']

            v = args['values'][col_name]
            ai = ai[col_name]
            ## On doit avoir le paramètre restrict !!
            index = v.index(self.entryPopup.data)

            if col == '#0':
                self.widget.item(rowid, text=ai[index])
            else:
                self.widget.set(rowid, col, ai[index])

        if 'autoreset' in args.keys():
            for col in args['autoreset']:
                if col == column:
                    continue

                if col == '#0':
                    self.widget.item(rowid, text = '')
                else:
                    self.widget.set(rowid, col, '')

        if 'command' in args.keys():
            args['command'](self.widget.item(rowid))

    def button_pressed(self, evt = None):
        if self.popup_ready:
            self.entryPopup.destroy()
            self.able_tooltip.set(1)
            self.popup_ready = False
        else:
            rowid = self.widget.identify_row(evt.y)
            column = self.widget.identify_column(evt.x)
            for col, cmd in self.actions.items():
                if col == column and cmd['type'] == 'switch':
                    old = self.widget.item(rowid)['values'][int(column.replace('#', ''))-1]
                    if old == self.FAVORI_ON:
                        new = self.FAVORI_OFF
                    else:
                        new = self.FAVORI_ON

                    if column == '#0':
                        self.widget.item(rowid, text=new)
                    else:
                        self.widget.set(rowid, column, new)
