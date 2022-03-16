import pyaudio
import sqlite3
import time

con = sqlite3.connect("record.db")
cur = con.cursor()

pA = pyaudio.PyAudio()

for row in cur.execute("SELECT ID, startT, endT FROM audio;"):
    begin = time.ctime(row[1])
    #begin = time.strftime(" %H:%M:%S %j. %B", row[1])
    print(str(row[0]) + " " + begin)

num = input(": ")

audio = cur.execute("SELECT freq, audio FROM audio WHERE ID = ?", num).fetchone()

stream = pA.open(rate=audio[0], channels=1, format=pyaudio.paInt16, output=True)
stream.write(audio[1])