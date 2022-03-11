import tkinter, time, threading
from tkinter import *
def processingPleaseWait(text, function,thread):
    window = Tk()
    window.geometry("300x250")
    window.title("Home security")
    label = Label(window, text = text)
    label.pack()
    done = []
#    thread = threading.Thread(target = lambda:call(3))
    thread.start() 
    while thread.is_alive():
        window.update()
        time.sleep(0.001)
    window.destroy()
#thread = threading.Thread(target = lambda:call(3))
#processingPleaseWait('waiting 2 seconds...', lambda: time.sleep(5),thread)
