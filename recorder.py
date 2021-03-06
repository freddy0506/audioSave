import pyaudio
import sqlite3
import wave
import threading
import time

con = sqlite3.connect("record.db")
cur = con.cursor()
cur.executescript(open("setup.sql", "r").read())

recBefore = 5
recAfter = 5
recMax = 600
rate = 44100
audio = pyaudio.PyAudio()
frames = [None]*int(rate / 1024 * recMax)
i = 0
recStop = False


def rec_thread_func():
    global i
    global recStop
    global frames
    global audio
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=rate, input=True, frames_per_buffer=1024)
    while not recStop:
        while i in range(0, int(rate / 1024 * recMax)):
            frames[i] = stream.read(1024)
            i+=1

    stream.close()


    


# Setup and start recording thread
rec_thread = threading.Thread(target=rec_thread_func)
rec_thread.start()



while True:
    input("Start")
    startFrame = i
    startTime = int(time.time())
    input("Stop")
    time.sleep(recAfter)
    #recStop = True
    endFrame = i
    endTime = int(time.time())

    outputFile = "out.wav"

    file = wave.open(outputFile, "wb")
    file.setnchannels(1)
    file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    file.setframerate(rate)
    if(startFrame == endFrame):
        print("Threading put")
    elif(startFrame < endFrame):
        startFrame = int(startFrame-(rate/1024*recBefore))
        cur.execute("INSERT INTO audio(startT, endT, len, freq, audio) VALUES (?,?,?,?,?);", (startTime, endTime, startTime-endTime, rate, b"".join(frames[startFrame:endFrame])))
        con.commit()
        file.writeframes(b"".join(frames[startFrame:endFrame]))
    elif(startFrame > endFrame):
        file.writeframes(b"".join(frames[startFrame-recBefore:int(rate / 1024 * recMax)]+frames[0:endFrame]))
    else:
        print("dafuq")

    file.close()

