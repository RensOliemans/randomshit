import tkinter as tk
import sys


class Application(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.canvas = tk.Canvas(self.parent, height=300, width=1200)
        self.canvas.pack()

    def _set_title(self):
        self.parent.title("Wasmachineverbruikmeetapplicatie")

    def _setup_close(self):
        def close(_):
            self.parent.withdraw()
            sys.exit()

        self.parent.bind('<Escape>', close)


if __name__ == '__main__':
    root = tk.Tk()
    Application(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
