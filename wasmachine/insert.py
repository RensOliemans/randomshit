import datetime
import sys

import tkinter as tk
import tkcalendar as tkc

from sql import get_programmes, get_programme, get_amount_measurements, insert_measurement, get_averages
from wasmachine import Measurement


def setup_close(root):
    def close(_):
        root.withdraw()
        sys.exit()

    root.bind('<Escape>', close)


def setup_canvases(root):
    input_canvas = tk.Canvas(root, height=300, width=1200)
    input_canvas.pack()

    results_canvas = tk.Canvas(root, height=300, width=1200)
    results_canvas.pack()
    return input_canvas, results_canvas


def setup_results(canvas):
    tk.Label(canvas, text='Naam', font=16).grid(row=0, column=0)
    tk.Label(canvas, text='Temp', font=16).grid(row=0, column=1)
    tk.Label(canvas, text='kWh', font=16).grid(row=0, column=2)
    tk.Label(canvas, text='Metingen', font=16).grid(row=0, column=3)


def setup_programmes(canvas, programme_variable, programmes):
    tk.OptionMenu(canvas, programme_variable, *programmes).place(relx=0.05, rely=0.15)


def setup_calendar(canvas, date_variable):
    tkc.Calendar(canvas, textvariable=date_variable, date_pattern='dd/mm/yy').place(relx=0.25, rely=.15)


def setup_input(canvas):
    setup_labels(canvas)
    return setup_inputs(canvas)


def setup_labels(canvas):
    tk.Label(canvas, text="Programma").place(relx=0.05, rely=0.05)
    tk.Label(canvas, text="Datum").place(relx=0.25, rely=0.05)
    tk.Label(canvas, text="Begin (kWh)").place(relx=0.50, rely=0.05)
    tk.Label(canvas, text="Eind (kWh)").place(relx=0.60, rely=0.05)
    tk.Label(canvas, text="Vol (0-1)").place(relx=0.70, rely=0.05)


def setup_inputs(canvas):
    begin = tk.Entry(canvas)
    begin.place(relx=0.50, rely=.15, width=100)
    end = tk.Entry(canvas)
    end.place(relx=0.60, rely=.15, width=100)
    vol = tk.Entry(canvas)
    vol.place(relx=.70, rely=.15, width=100)
    return begin, end, vol


def update(results_canvas):
    averages = get_averages()
    for i, a in enumerate(averages):
        name = tk.Label(results_canvas, text=a[0])
        temp = tk.Label(results_canvas, text=a[1])
        kwh = tk.Label(results_canvas, text=a[2])
        count = tk.Label(results_canvas, text=a[3])

        name.grid(row=i + 1, column=0)
        temp.grid(row=i + 1, column=1)
        kwh.grid(row=i + 1, column=2)
        count.grid(row=i + 1, column=3)


def setup_variables(canvas, programmes):
    programme_variable = tk.StringVar(canvas)
    programme_variable.set(programmes[0])
    date_variable = tk.StringVar(canvas)
    date_variable.set(str(datetime.date.strftime(datetime.date.today(), '%d/%m/%y')))
    return programme_variable, date_variable


def submit(canvas, pv, dv, b, e, v, ev, sv, callback):
    error, success = setup_error(canvas, ev, sv)
    try:
        programme = convert_programme(pv)
        date = datetime.datetime.strptime(dv, '%d/%m/%y')
        b = float(b)
        e = float(e)
        v = float(v)
        insert_measurement(Measurement(programme, date, b, e, v))
        ev.set('')
        sv.set(f'Gelukt, dit was de {get_amount_measurements()}e meting!')
        success.place(relx=.5, rely=.5)
        callback()
    except ValueError as e:
        ev.set(f'Error {e}')
        error.place(relx=0.5, rely=.5)


def setup_error(canvas, ev, sv):
    error = tk.Label(canvas, textvar=ev, bg="red")
    success = tk.Label(canvas, textvar=sv, bg="#51d0de")
    return error, success


def fancy_input():
    root = tk.Tk()
    setup_close(root)
    input_canvas, results_canvas = setup_canvases(root)

    programmes = list(get_programmes())
    pv, dv = setup_variables(input_canvas, programmes)

    setup_programmes(input_canvas, pv, programmes)
    setup_calendar(input_canvas, dv)
    begin, end, vol = setup_input(input_canvas)

    setup_results(results_canvas)
    update(results_canvas)

    def get_variables():
        def c():
            update(results_canvas)
        return input_canvas, pv.get(), dv.get(), begin.get(), end.get(), vol.get(), ev, sv, c

    ev = tk.StringVar(input_canvas)
    sv = tk.StringVar(input_canvas)

    begin.bind('<Return>', func=lambda _: submit(*get_variables()))
    end.bind('<Return>', func=lambda _: submit(*get_variables()))
    vol.bind('<Return>', func=lambda _: submit(*get_variables()))

    button = tk.Button(input_canvas, text='Submit', command=lambda: submit(*get_variables()))
    button.place(relx=.8, rely=.12)

    tk.mainloop()


def convert_programme(pv):
    pv = pv[1:-1]
    name, temp = pv.split(', ')
    return get_programme(name, temp)


if __name__ == '__main__':
    fancy_input()
