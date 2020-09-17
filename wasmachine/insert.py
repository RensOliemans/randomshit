import datetime

import tkinter as tk
import tkcalendar as tkc

from sql import get_programmes, get_programme, get_amount_measurements, insert_measurement, get_averages
from wasmachine import Measurement


def fancy_input():
    root = tk.Tk()
    input_canvas = tk.Canvas(root, height=300, width=1200)
    input_canvas.pack()

    results_canvas = tk.Canvas(root, height=300, width=1200)
    results_canvas.pack()

    tk.Label(results_canvas, text='Naam', font=16).grid(row=0, column=0)
    tk.Label(results_canvas, text='Temp', font=16).grid(row=0, column=1)
    tk.Label(results_canvas, text='kWh', font=16).grid(row=0, column=2)
    tk.Label(results_canvas, text='Metingen', font=16).grid(row=0, column=3)

    def update():
        averages = get_averages()
        for i, a in enumerate(averages):
            name = tk.Label(results_canvas, text=a[0])
            temp = tk.Label(results_canvas, text=a[1])
            kwh = tk.Label(results_canvas, text=a[2])
            count = tk.Label(results_canvas, text=a[3])

            name.grid(row=i+1, column=0)
            temp.grid(row=i+1, column=1)
            kwh.grid(row=i+1, column=2)
            count.grid(row=i+1, column=3)

    programmes = list(get_programmes())
    programme_variable = tk.StringVar(root)
    programme_variable.set(programmes[0])
    date_variable = tk.StringVar(root)
    date_variable.set(str(datetime.date.strftime(datetime.date.today(), '%d/%m/%y')))

    tk.Label(input_canvas, text="Programma").place(relx=0.05, rely=0.05)
    tk.Label(input_canvas, text="Datum").place(relx=0.25, rely=0.05)
    tk.Label(input_canvas, text="Begin (kWh)").place(relx=0.50, rely=0.05)
    tk.Label(input_canvas, text="Eind (kWh)").place(relx=0.60, rely=0.05)
    tk.Label(input_canvas, text="Vol (0-1)").place(relx=0.70, rely=0.05)

    tk.OptionMenu(input_canvas, programme_variable, *programmes).place(relx=0.05, rely=0.15)
    tkc.Calendar(input_canvas, textvariable=date_variable, date_pattern='dd/mm/yy').place(relx=0.25, rely=.15)

    begin = tk.Entry(input_canvas)
    begin.place(relx=0.50, rely=.15, width=100)
    end = tk.Entry(input_canvas)
    end.place(relx=0.60, rely=.15, width=100)
    vol = tk.Entry(input_canvas)
    vol.place(relx=.70, rely=.15, width=100)

    ev = tk.StringVar(input_canvas)
    sv = tk.StringVar(input_canvas)

    def test(pv, dv, b, e, v, ev2, sv2):
        error = tk.Label(input_canvas, textvar=ev2, bg="red")
        success = tk.Label(input_canvas, textvar=sv2, bg="#51d0de")
        try:
            programme = convert_programme(pv)
            date = datetime.datetime.strptime(dv, '%d/%m/%y')
            b = float(b)
            e = float(e)
            v = float(v)
            insert_measurement(Measurement(programme, date, b, e, v))
            ev2.set('')
            sv2.set(f'Gelukt, dit was de {get_amount_measurements()}e meting!')
            success.place(relx=.5, rely=.5)
            update()
        except ValueError as e:
            ev2.set(f'Error {e}')
            error.place(relx=0.5, rely=.5)

    begin.bind('<Return>', func=lambda _: test(programme_variable.get(), date_variable.get(), begin.get(), end.get(), vol.get(), ev, sv))
    end.bind('<Return>', func=lambda _: test(programme_variable.get(), date_variable.get(), begin.get(), end.get(), vol.get(), ev, sv))
    vol.bind('<Return>', func=lambda _: test(programme_variable.get(), date_variable.get(), begin.get(), end.get(), vol.get(), ev, sv))

    button = tk.Button(input_canvas, text='Submit', command=lambda: test(
        programme_variable.get(),
        date_variable.get(),
        begin.get(),
        end.get(),
        vol.get(),
        ev,
        sv))
    button.place(relx=.8, rely=.12)

    update()

    tk.mainloop()


def convert_programme(pv):
    pv = pv[1:-1]
    name, temp = pv.split(', ')
    return get_programme(name, temp)


if __name__ == '__main__':
    fancy_input()
