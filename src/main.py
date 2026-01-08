from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.simpledialog import *

from celleditor import *
import tex
import zipfile as zp

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

class Graphic(ttk.Frame):
    def __init__(self, unsave):
        super().__init__()
        self.unsave = unsave

        self.rowconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.curbs = {}

        self.lst = ttk.Treeview(self, columns = ('#1', '#2', '#3', '#4', '#5', '#6'), height = 10)
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
                                  },
                       command = self.unsave,
                       )

        fr_grid = ttk.Frame(self)
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
        self.legend = IntVar(value = 0)
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
                        values = ['x', 'red', '-1:1', 'thick', 'Identité', '-'])

        self.unsave()

    def remove(self, evt = None):
        sel = self.lst.selection()
        for iid in sel:
            self.lst.delete(iid)
        self.unsave()

    def see(self, name):
        give_tex(self.master, self.code(name))

    def tabify(self, text, n = 2):
        out = ''
        for line in text.split('\n'):
            out += n*' ' + line + '\n'

        return out[:-(1 + n)]

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

        code = '\\newcommand{' + str(name) + '}{\n'
        code += self.tabify(latex)
        code += '}\n'
        return code

    def save(self, arch, name):
        f = arch.open(name, 'w')
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

            x, y, color, domain, style, name, line, _ = bloc.split(b'##')
            self.lst.insert('', 'end', text = x.decode('utf-8'), values = [y.decode('utf-8'),
                                                                           color.decode('utf-8'),
                                                                           domain.decode('utf-8'),
                                                                           style.decode('utf-8'),
                                                                           name.decode('utf-8'),
                                                                           line.decode('utf-8')])

        f.close()

class Application:
    def __init__(self):
        self.master = Tk()
        icon = PhotoImage(file = './image.png')
        self.master.iconphoto(True, icon)
        self.master.title('Tikz assistant')
        self.master.rowconfigure(0, weight = 1)
        self.master.columnconfigure(0, weight = 1)
        self.master.minsize(800, 500)

        self.PATH = None
        self.EXPORT = None
        self.SAVED = False
        self.EXPORTED = False
        self.graphs = {}

        self.notebook = ttk.Notebook(self.master)
        self.notebook.enable_traversal()
        self.notebook.grid(row = 0, column = 0, sticky = 'nswe')
        self.notebook.bind('<Double-Button-1>', self.rename)

        self.newgraph()

        menubar = Menu(self.master)
        self.master['menu'] = menubar
        menufile = Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = 'Fichier', menu = menufile)
        menufile.add_command(label = 'Ouvrir', command = self.openfile)
        menufile.add_command(label = 'Enregistrer', command = self.save)
        menufile.add_command(label = 'Enregistrer et exporter', command = self.saveandexport)
        menufile.add_command(label = 'Enregistrer sous', command = self.saveas)
        menufile.add_command(label = 'Fermer', command = self.closeall)

        menuexporter = Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = 'Exporter', menu = menuexporter)
        menuexporter.add_command(label = 'Exporter', command = self.export)
        menuexporter.add_command(label = 'Exporter sous', command = self.exportas)
        menuexporter.add_separator()
        menuexporter.add_command(label = 'Copier ce code', command = self.copycode)
        menuexporter.add_command(label = 'Copier tout le code', command = self.copyallcode)

        menuview = Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = 'Voir', menu = menuview)
        menuview.add_command(label = 'Voir ce code', command = self.seecode)
        menuview.add_command(label = 'Voir tout le code', command = self.seeallcode)

        menubar.add_command(label = 'Ajouter', command = self.add)
        menubar.add_command(label = 'Retirer', command = self.remove)

        menubar.add_command(label = 'Nouveau graphique', command = self.newgraph)
        menubar.add_command(label = 'Supprimer le graphique', command = self.delgraph)

    def update_title(self):
        p = self.PATH if self.PATH is not None else 'sanstitre.tikz'
        exported = ' ✔' if self.EXPORTED else ''
        bords = ('* ', ' *') if not self.SAVED else ('', '')
        self.master.title(bords[0] + 'Tikz Assistant - ' + p + bords[1] + exported)

    def setsaved(self):
        self.SAVED = True
        self.update_title()

    def unsave(self):
        self.SAVED = False
        self.unexport()

    def setexported(self):
        self.EXPORTED = True
        self.update_title()

    def unexport(self):
        self.EXPORTED = False
        self.update_title()

    @property
    def thenote(self):
        me = self.notebook.select()
        return self.graphs[me][1]

    @property
    def thename(self):
        me = self.notebook.select()
        return self.graphs[me][0]

    @property
    def me(self):
        return self.notebook.select()

    def export(self, evt = None):
        if self.EXPORT is not None:
            f = open(self.EXPORT, 'w', encoding = 'utf-8')
            f.write(self.allcode)
            f.close()
            self.setexported()

        else:
            self.exportas()

    def exportas(self, evt = None):
        path = asksaveasfilename(title = 'Exporter sous',
                                 filetypes = [('Fichier TeX', '*.tex *.latex')])
        if not path:
            return

        f = open(path, 'w', encoding = 'utf-8')
        f.write(self.allcode)
        f.close()
        self.EXPORT = path
        self.setexported()

    def add(self, evt = None):
        self.thenote.add()
        self.unexport()
        self.unsave()

    def remove(self, evt = None):
        self.thenote.remove()
        self.unexport()
        self.unsave()

    def save(self, evt = None):
        if self.PATH is not None:
            z = zp.ZipFile(self.PATH, 'w')
            for tab in self.notebook.tabs():
                nom, graph = self.graphs[tab]
                graph.save(z, nom)

            z.close()
            self.setsaved()

        else:
            self.saveas()

    def saveas(self, evt = None):
        path = asksaveasfilename(title = 'Enregistrer sous', filetypes = [('Paramétrage tikz', '*.tikz')])
        if not path:
            return

        z = zp.ZipFile(path, 'w')
        for tab in self.notebook.tabs():
            nom, graph = self.graphs[tab]
            graph.save(z, nom)

        z.close()
        self.PATH = path
        self.setsaved()

    def closeall(self, evt = None):
        self.setsaved()
        self.PATH = None
        for tab in self.notebook.tabs():
            self.notebook.forget(tab)

        self.graphs.clear()

    def openfile(self, evt = None):
        path = askopenfilename(title = 'Ouvrir', filetypes = [('Paramétrages tikz', '*.tikz')])
        if not path:
            return

        self.closeall()

        z = zp.ZipFile(path, 'r')
        for nom in z.namelist():
            graph = self.newgraph(nom = nom)
            graph.openfile(z, nom)

        z.close()
        self.PATH = path
        self.setsaved()

    def copycode(self, evt = None):
        pass

    def copyallcode(self, evt = None):
        pass

    def seecode(self, evt = None):
        self.thenote.see(self.thename)

    @property
    def allcode(self, evt = None):
        code = '% Entête conseillé\n'
        f = open('header.tex', 'r', encoding = 'utf-8')
        code += f.read()
        f.close()

        code += '\n\n% Début des commandes\n'
        for tab in self.notebook.tabs():
            code += self.graphs[tab][1].code(self.thename)

        return code

    def saveandexport(self, evt = None):
        self.save()
        self.export()

    def seeallcode(self, evt = None):
        code = self.allcode
        give_tex(self.master, code)

    @property
    def allNoms(self):
        return map(lambda k: k[0], self.graphs.values())

    def newgraph(self, evt = None, nom = None):
        fr = Graphic(self.unsave)
        if nom is not None:
            pass
        else:
            nom = 'commande_1'
            while nom in self.allNoms:
                nom = nom[:-1] + str(int(nom[-1]) + 1)

        self.notebook.add(text = nom, child = fr)
        me = self.notebook.tabs()[-1]
        self.notebook.select(me)
        self.graphs[me] = [nom, fr]
        
        self.unexport()
        self.unsave()

        return fr

    def delgraph(self, evt = None):
        me = self.me
        self.notebook.forget(me)
        del self.graphs[me]

    def rename(self, evt = None):
        graph = self.notebook.select()
        nom, fr = self.graphs[graph]
        newname = askstring('Renommer',
                            'Veuillez entrer le nouveau nom de la commande.\nCelle ci sera accessible dans TeX via \\nom',
                            initialvalue = nom)

        if newname == nom:
            return

        if newname in self.allNoms:
            showerror('Renommer', 'Ce nom est déjà occupé')
            return

        self.graphs[graph][0] = newname
        self.notebook.tab(graph, text = newname)

        self.unexport()
        self.unsave()


if __name__ == '__main__':
    app = Application()
    app.master.mainloop()
