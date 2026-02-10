from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.simpledialog import *

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

from widgets.celleditor import *
import preview
import viewer
import tex.surface as tex

class GraphicSurface(ttk.Frame):
    def __init__(self, unsave):
        super().__init__()
        self.unsave_extern_command = unsave

        self.rowconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.curbs = {}

        self.lst = ttk.Treeview(self, columns = ('#1', '#2', '#3', '#4', '#5', '#6', '#7'), height = 10)
        self.lst.grid(row = 0, column = 0, pady = 5, padx = 5, sticky = 'nswe', columnspan = 3)
        self.lst.heading('#0', text = 'Abscisse f1(x)')
        self.lst.heading('#1', text = 'Ordonées f2(x)')
        self.lst.heading('#2', text = 'Hauteur  f3(x, y)')
        self.lst.heading('#3', text = 'Couleur')
        self.lst.heading('#4', text = 'Domaine a:b;c:d')
        self.lst.heading('#5', text = 'Style')
        self.lst.heading('#6', text = 'Légende')
        self.lst.heading('#7', text = 'Marks')
        self.lst.column('#0', width=150)
        self.lst.column('#1', width=150)
        self.lst.column('#2', width=150)
        self.lst.column('#3', width=80)
        self.lst.column('#4', width=90)
        self.lst.column('#5', width=70)
        self.lst.column('#6', width=150)
        self.lst.column('#7', width = 30)
        r = CellEditor(self.lst,
                       actions = {'#0': {'type': 'Entry'},
                                  '#1': {'type': 'Entry'},
                                  '#2': {'type': 'Entry'},
                                  '#3': {'type': 'Combo', 'values': ['shader = intrep', 'red', 'brown', 'blue', 'green', 'orange', 'pink', 'purple', 'yellow', 'shader = flat']},
                                  '#4': {'type': 'Entry'},
                                  '#5': {'type': 'Combo', 'values': ['surf', 'mesh', 'scatter', 'smooth']},
                                  '#6': {'type': 'Entry'},
                                  '#7': {'type': 'Combo', 'values': ['no marks', 'only marks']},
                                  },
                       command = self.unsave,
                       )

        self.lst.bind('<Delete>', self.remove)

        fr_grid = ttk.Frame(self)
        fr_grid.grid(row = 1, column = 0, sticky = 'nswe', padx = 5, pady = 5)

        self.grid = StringVar(value = '')
        self.grid.trace("w", self.unsave)
        self.axiseq = IntVar(value = 1)
        self.axiseq.trace("w", self.unsave)
        rd_both = ttk.Radiobutton(fr_grid, value = 'both', variable = self.grid, text = 'Grille double')
        rd_both.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'nswe')

        rd_major = ttk.Radiobutton(fr_grid, value = 'major', variable = self.grid, text = 'Grille majeure')
        rd_major.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'nswe')

        rd_none = ttk.Radiobutton(fr_grid, value = '', variable = self.grid, text = 'Pas de grille')
        rd_none.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = 'nswe')

        rd_axeeq = ttk.Checkbutton(fr_grid, text = 'Axes égaux', variable = self.axiseq, onvalue = 1, offvalue = 0)
        rd_axeeq.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = 'nswe', columnspan = 2)

        fr_axis = ttk.Frame(self)
        fr_axis.grid(row = 1, column = 1, sticky = 'nswe', padx = 5, pady = 5)
        fr_axis.columnconfigure(1, weight = 1)

        lb_xmin = ttk.Label(fr_axis, text = 'X_min')
        lb_xmin.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'e')
        lb_xmax = ttk.Label(fr_axis, text = 'X_max')
        lb_xmax.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'e')
        lb_ymin = ttk.Label(fr_axis, text = 'Y_min')
        lb_ymin.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = 'e')
        lb_ymax = ttk.Label(fr_axis, text = 'Y_max')
        lb_ymax.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = 'e')

        self.xmin = StringVar(value = '-1')
        self.xmax = StringVar(value = '1')
        self.ymin = StringVar(value = '-1')
        self.ymax = StringVar(value = '1')
        self.xmin.trace("w", self.unsave)
        self.xmax.trace("w", self.unsave)
        self.ymin.trace("w", self.unsave)
        self.ymax.trace("w", self.unsave)

        ent_xmin = ttk.Entry(fr_axis, textvariable = self.xmin)
        ent_xmin.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = 'nswe')
        ent_xmax = ttk.Entry(fr_axis, textvariable = self.xmax)
        ent_xmax.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'nswe')
        ent_ymin = ttk.Entry(fr_axis, textvariable = self.ymin)
        ent_ymin.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = 'nswe')
        ent_ymax = ttk.Entry(fr_axis, textvariable = self.ymax)
        ent_ymax.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = 'nswe')

        fr_global = ttk.Frame(self)
        fr_global.grid(row = 1, column = 2, padx = 5, pady = 5, sticky = 'nswe')
        fr_global.columnconfigure(1, weight = 1)

        lb_tt = ttk.Label(fr_global, text = 'Titre (figure)')
        lb_tt.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'e')
        lb_lg = ttk.Label(fr_global, text = 'Titre (legende)')
        lb_lg.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'e')

        self.title_caption = StringVar()
        self.title_legend = StringVar()
        self.title_caption.trace('w', self.unsave)
        self.title_legend.trace('w', self.unsave)
        self.legend = IntVar(value = 0)
        self.legend.trace('w', self.unsave)
        ent_tt = ttk.Entry(fr_global, textvariable = self.title_caption)
        ent_tt.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = 'nswe')

        ent_lg = ttk.Entry(fr_global, textvariable = self.title_legend)
        ent_lg.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'nswe')

        lg = ttk.Checkbutton(fr_global, text = 'Afficher la légende', onvalue = 1, offvalue = 0, variable = self.legend)
        lg.grid(row = 3, column = 0, columnspan = 2, padx = 5, pady = 5,sticky = 'w')

        self.lst.bind("<ButtonPress-1>",self.bDown)
        self.lst.bind("<ButtonRelease-1>",self.bUp, add='+')
        self.lst.bind("<B1-Motion>",self.bMove, add='+')
        self.lst.bind("<Shift-ButtonPress-1>",self.bDown_Shift, add='+')
        self.lst.bind("<Shift-ButtonRelease-1>",self.bUp_Shift, add='+')

        self.fig = Figure(figsize = (5, 5), dpi = 100)
        self.plot1 = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master = self)
        #self.canvas.get_tk_widget().grid(row = 0, column = 5, rowspan = 2)
        self.update_graph()

    def unsave(self, *args, **kwargs):
        self.unsave_extern_command()
        self.update_graph()

    def update_graph(self):
        lines = self.get_data()
        self.plot1.cla()
        #preview.Surface(lines, self.grid.get(), self.axiseq.get(),
        #                self.xmin.get(), self.xmax.get(), self.ymin.get(), self.ymax.get(),
        #                self.title_caption.get(), self.legend.get(), self.title_legend.get(), plot = self.plot1)

        self.canvas.draw()
        

    def bDown_Shift(self, event):
        tv = event.widget
        select = [tv.index(s) for s in tv.selection()]
        select.append(tv.index(tv.identify_row(event.y)))
        select.sort()
        for i in range(select[0],select[-1]+1,1):
            tv.selection_add(tv.get_children()[i])

    def bDown(self, event):
        tv = event.widget
        if tv.identify_row(event.y) not in tv.selection():
            tv.selection_set(tv.identify_row(event.y))    

    def bUp(self, event):
        tv = event.widget
        if tv.identify_row(event.y) in tv.selection():
            tv.selection_set(tv.identify_row(event.y))

        self.unsave()

    def bUp_Shift(self, event):
        self.unsave()

    def bMove(self, event):
        tv = event.widget
        moveto = tv.index(tv.identify_row(event.y))    
        for s in tv.selection():
            tv.move(s, '', moveto)

    def add(self):
        self.lst.insert('', 'end', text = 'x',
                        values = ['y', 'x', 'shader = interp', '-1:1;-1:1', 'mesh', 'Identité', 'no marks'])

        self.unsave()

    def remove(self, evt = None):
        sel = self.lst.selection()
        for iid in sel:
            self.lst.delete(iid)
        self.unsave()

    def see(self, name):
        viewer.give_tex(self.master, self.code(name))

    def tabify(self, text, n = 2):
        out = ''
        for line in text.split('\n'):
            out += n*' ' + line + '\n'

        return out[:-(1 + n)]

    def get_data(self):
        courbes = []
        for iid in self.lst.get_children():
            row = [self.lst.item(iid)['text']] + self.lst.item(iid)['values']
            courbes.append(row)

        return courbes

    def code(self, name):
        courbes = []
        for iid in self.lst.get_children():
            row = [self.lst.item(iid)['text']] + self.lst.item(iid)['values']
            line = tex.line_curb_2d(*row)
            courbes.append(line)

        arguments = {}
        arguments['xmin'] = self.xmin.get()
        arguments['ymin'] = self.ymin.get()
        arguments['xmax'] = self.xmax.get()
        arguments['ymax'] = self.ymax.get()
        arguments['grid'] = self.grid.get()
        title = self.title_caption.get()

        latex = tex.figure(courbes,
                           arguments,
                           title,
                           self.legend.get(),
                           self.title_legend.get(),
                           self.axiseq.get())

        code = '\\newcommand{\\' + str(name) + '}{\n'
        code += self.tabify(latex)
        code += '}\n'
        return code

    def save(self, arch, name):
        f = arch.open(name + '.surface', 'w')
        f.write(str(self.legend.get()).encode('utf-8'))
        f.write(str(self.axiseq.get()).encode('utf-8'))
        f.write(b'//\n')
        f.write(self.grid.get().encode('utf-8'))
        f.write(b'//\n')
        for v in [self.xmin.get(), self.xmax.get(), self.ymin.get(), self.ymax.get(),
                  self.title_caption.get(), self.title_legend.get()]:
            f.write(str(v).encode('utf-8'))
            f.write(b'//\n')

        for iid in self.lst.get_children():
            item = self.lst.item(iid)
            f.write(item['text'].encode('utf-8'))
            f.write(b'##')
            for v in item['values']:
                f.write(str(v).encode('utf-8'))
                f.write(b'##')

            f.write(b'//\n')

        f.close()

    def clear(self):
        for x in self.lst.get_children():
            self.lst.delete(x)

    def openfile(self, arch, nom):
        f = arch.open(nom, 'r')
        blocs = f.read().split(b'//\n')
        legend, axiseq = list(map(int, list(blocs[0].decode('utf-8'))))
        self.legend.set(legend)
        self.axiseq.set(axiseq)
        grid = blocs[1]
        self.grid.set(grid.decode('utf-8'))
        xmin, xmax, ymin, ymax, cap, leg = blocs[2:8]
        self.xmin.set(xmin.decode('utf-8'))
        self.xmax.set(xmax.decode('utf-8'))
        self.ymin.set(ymin.decode('utf-8'))
        self.ymax.set(ymax.decode('utf-8'))
        self.title_caption.set(cap.decode('utf-8'))
        self.title_legend.set(leg.decode('utf-8'))
        self.clear()
        for bloc in blocs[8:]:
            if not bloc:
                continue

            x, y, z, color, domain, style, name, line, _ = bloc.split(b'##')
            self.lst.insert('', 'end', text = x.decode('utf-8'), values = [y.decode('utf-8'),
                                                                           z.decode('utf-8'),
                                                                           color.decode('utf-8'),
                                                                           domain.decode('utf-8'),
                                                                           style.decode('utf-8'),
                                                                           name.decode('utf-8'),
                                                                           line.decode('utf-8')])

        f.close()
        self.update_graph()
