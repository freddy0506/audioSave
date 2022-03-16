CREATE TABLE IF NOT EXISTS audio(
    ID INT,
    StartTime INT,
    EndTime INT,
    length LONGINT,
    freq INT,
    audio BLOB
);