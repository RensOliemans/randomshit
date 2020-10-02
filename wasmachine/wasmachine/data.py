class Programme:
    def __init__(self, id, name, temperature, rpm):
        self.id = id
        self.name = name
        self.temperature = temperature
        self.rpm = rpm

    def __str__(self):
        return f"({self.name}, {self.temperature}, {self.rpm})"

    def __repr__(self):
        return f"Programme: {self.id}, {self.name}, {self.temperature}, {self.rpm}"


class Measurement:
    def __init__(self, programme, date, begin, end=None, vol=1):
        self.programme = programme
        self.date = date
        self.begin = begin
        self.end = end
        self.vol = vol
        if not 0.0 <= vol <= 1.0:
            raise ValueError('Vol must be between 0 and 1')
        if end < begin:
            raise ValueError("End must not be lower than start")

    @property
    def kwh(self):
        return self.end - self.begin

    def __repr__(self):
        return f"Measurement of programme {str(self.programme)}.\n" \
               f"Date: {self.date}, kWh: {self.kwh} ({self.end}-{self.begin})," \
               f"{int(self.vol * 100)}% filled."
