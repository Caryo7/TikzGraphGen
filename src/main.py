from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter.filedialog import *
from tkinter.messagebox import *

from celleditor import *
import tex

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

class Application:
    def __init__(self):
        self.master = Tk()
        self.master.title('PgfPlots assistant')
        self.master.rowconfigure(0, weight = 1)
        self.master.columnconfigure(1, weight = 1)
        self.master.columnconfigure(2, weight = 1)

        menubar = Menu(self.master)
        self.master['menu'] = menubar
        menubar.add_command(label = 'Exporter', command = self.export)
        menubar.add_command(label = 'Ajouter', command = self.add)
        menubar.add_command(label = 'Retirer', command = self.remove)
        menubar.add_command(label = 'Enregistrer', command = self.save)
        menubar.add_command(label = 'Ouvrir', command = self.openfile)

        self.curbs = {}

        self.lst = ttk.Treeview(self.master, columns = ('#1', '#2', '#3', '#4', '#5', '#6'), height = 10)
        self.lst.grid(row = 0, column = 0, pady = 5, padx = 5, sticky = 'nswe', columnspan = 3)
        self.lst.heading('#0', text = 'Abscisse f1(x)')
        self.lst.heading('#1', text = 'Ordonées f2(x)')
        self.lst.heading('#2', text = 'Couleur')
        self.lst.heading('#3', text = 'Domaine a:b')
        self.lst.heading('#4', text = 'style')
        self.lst.heading('#5', text = 'Légende')
        self.lst.heading('#6', text = '--')
        self.lst.column('#0', width=150)
        self.lst.column('#1', width=150)
        self.lst.column('#2', width=80)
        self.lst.column('#3', width=90)
        self.lst.column('#4', width=70)
        self.lst.column('#5', width=150)
        self.lst.column('#6', width = 30)
        r = CellEditor(self.lst,
                       actions = {'#0': {'type': 'Entry'},
                                  '#1': {'type': 'Entry'},
                                  '#2': {'type': 'Combo', 'values': ['red', 'brown', 'blue', 'green', 'orange', 'pink', 'purple', 'yellow']},
                                  '#3': {'type': 'Entry'},
                                  '#4': {'type': 'Combo', 'values': ['dashed', 'thick', 'double']},
                                  '#5': {'type': 'Entry'},
                                  '#6': {'type': 'Combo', 'values': ['-', '->', '<->', '<-']},
                                  }
                       )

        fr_grid = ttk.Frame(self.master)
        fr_grid.grid(row = 1, column = 0, sticky = 'nswe', padx = 5, pady = 5)

        self.grid = StringVar(value = '')
        self.axiseq = IntVar(value = 1)
        rd_both = ttk.Radiobutton(fr_grid, value = 'both', variable = self.grid, text = 'Grille double')
        rd_both.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'nswe')

        rd_major = ttk.Radiobutton(fr_grid, value = 'major', variable = self.grid, text = 'Grille majeure')
        rd_major.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'nswe')

        rd_none = ttk.Radiobutton(fr_grid, value = '', variable = self.grid, text = 'Pas de grille')
        rd_none.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = 'nswe')

        rd_axeeq = ttk.Checkbutton(fr_grid, text = 'Axes égaux', variable = self.axiseq, onvalue = 1, offvalue = 0)
        rd_axeeq.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = 'nswe', columnspan = 2)

        fr_axis = ttk.Frame(self.master)
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

        ent_xmin = ttk.Entry(fr_axis, textvariable = self.xmin)
        ent_xmin.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = 'nswe')
        ent_xmax = ttk.Entry(fr_axis, textvariable = self.xmax)
        ent_xmax.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'nswe')
        ent_ymin = ttk.Entry(fr_axis, textvariable = self.ymin)
        ent_ymin.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = 'nswe')
        ent_ymax = ttk.Entry(fr_axis, textvariable = self.ymax)
        ent_ymax.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = 'nswe')

        fr_global = ttk.Frame(self.master)
        fr_global.grid(row = 1, column = 2, padx = 5, pady = 5, sticky = 'nswe')
        fr_global.columnconfigure(1, weight = 1)

        lb_tt = ttk.Label(fr_global, text = 'Titre (figure)')
        lb_tt.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'e')
        lb_lg = ttk.Label(fr_global, text = 'Titre (legende)')
        lb_lg.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'e')

        self.title_caption = StringVar()
        self.title_legend = StringVar()
        self.legend = IntVar(value = 0)
        ent_tt = ttk.Entry(fr_global, textvariable = self.title_caption)
        ent_tt.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = 'nswe')

        ent_lg = ttk.Entry(fr_global, textvariable = self.title_legend)
        ent_lg.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'nswe')

        lg = ttk.Checkbutton(fr_global, text = 'Afficher la légende', onvalue = 1, offvalue = 0, variable = self.legend)
        lg.grid(row = 3, column = 0, columnspan = 2, padx = 5, pady = 5,sticky = 'w')

    def add(self):
        self.lst.insert('', 'end', text = 'x',
                        values = ['x', 'red', '-1:1', 'thick', 'Identité', '-'])

    def remove(self, evt = None):
        sel = self.lst.selection()
        for iid in sel:
            self.lst.delete(iid)

    def export(self):
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

        code = tex.figure(courbes,
                          arguments,
                          title,
                          self.legend.get(),
                          self.title_legend.get(),
                          self.axiseq.get())

        give_tex(self.master, code)

    def save(self):
        path = asksaveasfilename(title = 'Enregistrer sous', filetypes = [('Paramétrages tikz', '*.tikz')])
        if not path:
            return

        f = open(path, 'w')
        f.write(str(self.legend.get()))
        f.write(str(self.axiseq.get()))
        f.write('//\n')
        f.write(self.grid.get())
        f.write('//\n')
        for v in [self.xmin.get(), self.xmax.get(), self.ymin.get(), self.ymax.get(),
                  self.title_caption.get(), self.title_legend.get()]:
            f.write(v)
            f.write('//\n')

        for iid in self.lst.get_children():
            item = self.lst.item(iid)
            f.write(item['text'])
            f.write('##')
            for v in item['values']:
                f.write(v)
                f.write('##')

            f.write('//\n')

        f.close()

    def clear(self):
        for x in self.lst.get_children():
            self.lst.delete(x)

    def openfile(self):
        path = askopenfilename(title = 'Ouvrir', filetypes = [('Paramétrages tikz', '*.tikz')])
        if not path:
            return

        f = open(path, 'r')
        blocs = f.read().split('//\n')
        legend, axiseq = list(map(int, list(blocs[0])))
        self.legend.set(legend)
        self.axiseq.set(axiseq)
        grid = blocs[1]
        xmin, xmax, ymin, ymax, cap, leg = blocs[2:8]
        self.xmin.set(xmin)
        self.xmax.set(xmax)
        self.ymin.set(ymin)
        self.ymax.set(ymax)
        self.title_caption.set(cap)
        self.title_legend.set(leg)
        self.clear()
        for bloc in blocs[8:]:
            if not bloc:
                continue

            x, y, color, domain, style, name, line, _ = bloc.split('##')
            self.lst.insert('', 'end', text = x, values = [y, color, domain, style, name, line])

        f.close()


if __name__ == '__main__':
    app = Application()
    app.master.mainloop()
