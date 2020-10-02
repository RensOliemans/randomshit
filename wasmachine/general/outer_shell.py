import tkinter as tk


class Application(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

    def add(self, child):
        child.register(self)


class Child:
    def __init__(self, master=None, cnf=None, **kw):
        self.master = master
        self.kw = kw
        self.cnf = cnf if cnf is not None else {}
        self.canvas = None
        self.parent = None

    def register(self, parent):
        self.parent = parent
        self.setup()

    def setup(self):
        raise TypeError("I don't have a setup method yet!")
