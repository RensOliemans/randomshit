import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


def plot_peaks(filename):
    df = pd.read_csv(filename)
    y = df[' Ct']
    peaks, properties = find_peaks(y, prominence=(50, None))
    print(properties['prominences'])

    plt.plot(y)
    plt.plot(peaks, y[peaks], "x")
    [plt.annotate(str(y[i].round(2)), xy=(i, y[i])) for i in peaks]
    plt.savefig(filename + '.png')


def get_values(filename, r):
    df = pd.read_csv(filename)
    y = df[' Ct']

    peaks, properties = find_peaks(y, prominence=(50, None))

    if len(peaks) != 5:
        print(f"Bestand {filename} heeft geen 5 pieken, zie {filename}.png")
        plot_peaks(filename)
        return

    y_vals = [round(i, r) for i in y[peaks]]

    print(f"Bestand: {filename}")
    print(f"x-waarden van pieken: {peaks}")
    print(f"y-waarden:            {y_vals}\n")


def main(r=6):
    excel_files = [f for f in os.listdir() if f[-4:] == '.csv']
    for file in excel_files:
        get_values(file, r)


if __name__ == '__main__':
    main()
