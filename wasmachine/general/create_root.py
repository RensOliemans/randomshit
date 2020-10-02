import sys
sys.path.insert(0, '/home/rens/Projects/randomshit/wasmachine')

import tkinter as tk

from general.outer_shell import Application, Child
from wasmachine.gui import Wasmachine


def create_root(children):
    root = tk.Tk()
    app = Application(root)
    app.pack(side='top', fill='both', expand=True)
    for child in children:
        app.add(child)
    root.mainloop()
    return app


if __name__ == '__main__':
    c = Child(height=300, width=1200)
    w = Wasmachine()
    create_root([w])
