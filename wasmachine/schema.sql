CREATE TABLE IF NOT EXISTS "programme"
(
    id int
          primary key,
    name text not null,
    temperature int not null,
    rpm int not null,
    unique (name, temperature, rpm)
);
CREATE TABLE IF NOT EXISTS "measurement"
(
    id    INT
        primary key,
    date  text NOT NULL,
    vol   REAL DEFAULT 1,
    begin REAL NOT NULL,
    end   REAL,
    pid   INT
        references programme
    CHECK (vol <= 1.0)
    CHECK (vol >= 0.0)
);
