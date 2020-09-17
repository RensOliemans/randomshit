import datetime
import sys

import tkinter as tk
import tkcalendar as tkc

from sql import get_programmes, get_programme, get_amount_measurements, insert_measurement, get_averages
from wasmachine import Measurement


class Application(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self._setup_close()
        self._setup_canvases()
        self._setup_variables()

        self._setup_programmes()
        self._setup_calendar()
        self._setup_input()

        self._setup_results()
        self._update()

        self._setup_submit_button()

        self._bind_returns()

    def _setup_close(self):
        def close(_):
            self.parent.withdraw()
            sys.exit()

        self.parent.bind('<Escape>', close)

    def _setup_canvases(self):
        self.input_canvas = tk.Canvas(self.parent, height=300, width=1200)
        self.input_canvas.pack()

        self.results_canvas = tk.Canvas(self.parent, height=300, width=1200)
        self.results_canvas.pack()

    def _setup_variables(self):
        self._programmes = list(get_programmes())
        self._pv = tk.StringVar(self.input_canvas)
        self._pv.set(self._programmes[0])
        self._dv = tk.StringVar(self.input_canvas)
        self._dv.set(str(datetime.date.strftime(datetime.date.today(), '%d/%m/%y')))

        self._ev = tk.StringVar(self.input_canvas)
        self._sv = tk.StringVar(self.input_canvas)

    def _setup_programmes(self):
        tk.OptionMenu(self.input_canvas, self._pv, *self._programmes).place(relx=0.05, rely=0.15)

    def _setup_calendar(self):
        tkc.Calendar(self.input_canvas, textvariable=self._dv,
                     date_pattern='dd/mm/yy').place(relx=0.25, rely=.15)

    def _setup_input(self):
        self._setup_labels()
        self._setup_inputs()

    def _setup_labels(self):
        tk.Label(self.input_canvas, text="Programma").place(relx=0.05, rely=0.05)
        tk.Label(self.input_canvas, text="Datum").place(relx=0.25, rely=0.05)
        tk.Label(self.input_canvas, text="Begin (kWh)").place(relx=0.50, rely=0.05)
        tk.Label(self.input_canvas, text="Eind (kWh)").place(relx=0.60, rely=0.05)
        tk.Label(self.input_canvas, text="Vol (0-1)").place(relx=0.70, rely=0.05)

    def _setup_inputs(self):
        self._begin = tk.Entry(self.input_canvas)
        self._begin.place(relx=0.50, rely=.15, width=100)
        self._end = tk.Entry(self.input_canvas)
        self._end.place(relx=0.60, rely=.15, width=100)
        self._vol = tk.Entry(self.input_canvas)
        self._vol.place(relx=.70, rely=.15, width=100)

    def _setup_results(self):
        tk.Label(self.results_canvas, text='Naam', font=16).grid(row=0, column=0)
        tk.Label(self.results_canvas, text='Temp', font=16).grid(row=0, column=1)
        tk.Label(self.results_canvas, text='kWh', font=16).grid(row=0, column=2)
        tk.Label(self.results_canvas, text='Metingen', font=16).grid(row=0, column=3)

    def _update(self):
        averages = get_averages()
        for i, a in enumerate(averages):
            name = tk.Label(self.results_canvas, text=a[0])
            temp = tk.Label(self.results_canvas, text=a[1])
            kwh = tk.Label(self.results_canvas, text=a[2])
            count = tk.Label(self.results_canvas, text=a[3])

            name.grid(row=i + 1, column=0)
            temp.grid(row=i + 1, column=1)
            kwh.grid(row=i + 1, column=2)
            count.grid(row=i + 1, column=3)

    def _bind_returns(self):
        self._begin.bind('<Return>', func=lambda _: self._submit())
        self._end.bind('<Return>', func=lambda _: self._submit())
        self._vol.bind('<Return>', func=lambda _: self._submit())

    def _setup_submit_button(self):
        button = tk.Button(self.input_canvas, text='Submit', command=lambda: self._submit())
        button.place(relx=.8, rely=.12)

    def _submit(self):
        self._setup_error()
        try:
            programme = self._convert_programme(self._pv.get())
            date = datetime.datetime.strptime(self._dv.get(), '%d/%m/%y')
            b = float(self._begin.get())
            e = float(self._end.get())
            v = float(self._vol.get())
            insert_measurement(Measurement(programme, date, b, e, v))
            self._ev.set('')
            self._sv.set(f'Gelukt, dit was de {get_amount_measurements()}e meting!')
            self._success.place(relx=.5, rely=.5)
            self._update()
        except ValueError as e:
            self._ev.set(f'Error {e}')
            self._error.place(relx=0.5, rely=.5)

    def _setup_error(self):
        self._error = tk.Label(self.input_canvas, textvar=self._ev, bg="red")
        self._success = tk.Label(self.input_canvas, textvar=self._sv, bg="#51d0de")

    @staticmethod
    def _convert_programme(pv):
        pv = pv[1:-1]
        name, temp = pv.split(', ')
        return get_programme(name, temp)


if __name__ == '__main__':
    root = tk.Tk()
    Application(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
