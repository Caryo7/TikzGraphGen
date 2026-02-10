from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.simpledialog import *

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

from widgets.celleditor import *
from viewer import *
import zipfile as zp
import preview
import graphs.courbe as courbe
import graphs.surface as surface

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

        self.new_courbe()

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

        menuadd = Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = 'Ajouter', menu = menuadd)
        menuadd.add_command(label = 'Nouvel élément', command = self.add)
        menuadd.add_separator()
        menuadd.add_command(label = 'Courbe paramétrée', command = self.new_courbe)
        menuadd.add_command(label = 'Surface paramétrée', command = self.new_surface)
        menuadd.add_command(label = 'Supprimer le graphique', command = self.delgraph)

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

    def newgraph(self, nom):
        if nom.endswith('.surface'):
            return self.new_surface(nom.replace('.surface', ''))
        elif nom.endswith('.courbe'):
            return self.new_surface(nom.replace('.courbe', ''))

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

    def new_courbe(self, evt = None, nom = None):
        fr = courbe.GraphicCurb(self.unsave)
        if nom is not None:
            pass

        else:
            nom = 'courbe1'
            while nom in self.allNoms:
                nom = nom[:-1] + str(int(nom[-1]) + 1)

        self.notebook.add(text = nom, child = fr)
        me = self.notebook.tabs()[-1]
        self.notebook.select(me)
        self.graphs[me] = [nom, fr]
        
        self.unexport()
        self.unsave()

        return fr

    def new_surface(self, evt = None, nom = None):
        fr = surface.GraphicSurface(self.unsave)
        if nom is not None:
            pass

        else:
            nom = 'surface1'
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


def view():
    os.system('rm main.dvi')
    os.system('rm file.png')
    os.system('latex main.tex')
    os.system('dvipng -bg Transparent -D 100 -T tight -o file.png main.dvi')
    os.popen('file.png')

#view()



if __name__ == '__main__':
    pass
    app = Application()
    app.master.mainloop()
