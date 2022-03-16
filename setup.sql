CREATE TABLE IF NOT EXISTS audio(
    ID INTEGER PRIMARY KEY,
    startT INT,
    endT INT,
    len LONGINT,
    freq INT,
    audio BLOB
);