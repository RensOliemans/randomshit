import sqlite3

from wasmachine import Programme, Measurement

conn = sqlite3.connect('/home/rens/Projects/randomshit/wasmachine/wasmachine.db')
c = conn.cursor()


def get_programme(name, temperature, rpm):
    c.execute('SELECT id,name,temperature, rpm FROM programme WHERE name=? AND temperature=? AND rpm=?',
              (name, temperature, rpm))
    results = c.fetchone()
    return Programme(results[0], results[1], results[2], results[3])


def get_programmes(sort=True):
    string = 'SELECT id,name,temperature, rpm FROM programme'
    if sort:
        string += ' ORDER BY name,temperature'
    c.execute(string)
    return (Programme(p[0], p[1], p[2], p[3]) for p in c.fetchall())


def get_measurements():
    c.execute('SELECT programme.id, programme.name, programme.temperature, '
              'measurement.date, measurement.begin, '
              'measurement.end, measurement.vol '
              'FROM programme, measurement '
              'WHERE programme.id = measurement.pid')
    for r in c.fetchall():
        p = Programme(r[0], r[1], r[2])
        yield Measurement(p, r[3], r[4], r[5], r[6])


def get_amount_measurements():
    c.execute('SELECT count(*) FROM measurement')
    return c.fetchone()[0]


def get_averages():
    c.execute('SELECT programme.name, programme.temperature,'
              'round(avg(measurement.end - measurement.begin),3),'
              'programme.rpm, count(measurement.pid) '
              'FROM programme, measurement '
              'WHERE programme.id = measurement.pid '
              'GROUP BY programme.id')
    return c.fetchall()


def insert_measurement(measurement):
    c.execute('SELECT max(id) FROM measurement')
    max_id = c.fetchone()[0] or 0
    c.execute('INSERT INTO measurement (id, date, vol, begin, end, pid) VALUES'
              '(?, ?, ?, ?, ?, ?)',
              (max_id + 1, str(measurement.date), measurement.vol, measurement.begin,
               measurement.end, measurement.programme.id))
    conn.commit()
