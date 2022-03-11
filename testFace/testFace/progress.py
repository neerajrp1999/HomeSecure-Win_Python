import tkinter, time, threading
from tkinter import *
def processingPleaseWait(text, function,thread):
    window = Tk()
    window.geometry("300x250")
    window.title("Home security")
    label = Label(window, text = text)
    label.pack()
    done = []
    thread.start() 
    while thread.is_alive():
        window.update()
        time.sleep(0.001)
    window.destroy()