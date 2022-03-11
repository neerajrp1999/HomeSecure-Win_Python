from datetime import datetime
import time, threading
from tkinter import *
from tkinter import messagebox
from firebase import firebase
import cv2
from face_recognition_knn import *
import progress as prgs
import firebase_admin
from firebase_admin import credentials , firestore
import pusher
"""
pusher_client = pusher.Pusher(
 app_id = "",
key = "",
secret = "",
cluster = ""
)
"""

cre=credentials.Certificate("firebase_admin.json")
d_app=firebase_admin.initialize_app(cre)

db =firestore.client()

def requestCheckThread(cap,root1):
    root1.wm_withdraw()
    thread = threading.Thread(target = lambda:requestCheck(cap,root1))
    prgs.processingPleaseWait('wait it will take time....', lambda: time.sleep(5),thread)
    root1.wm_deiconify()
def requestCheck(cap,root):
    db_ref=db.collection(u'data').document(u'request')
    d=db_ref.get()
    di=d.to_dict()
    a=di['accepted']
    s=di['requested']
    if(a=='1'):
        db_ref.update({ u'accepted':'0',
                    u'requested':'0'
        })
        messagebox.showinfo("Done","Welcome Home")
        root.destroy()
        mainToStart()
    if(s=='1'):
        messagebox.showinfo("Request","Request already Sended Wait For Response")
    if(s=='0'):
        db_ref=db.collection(u'data').document(u'request')
        db_ref.update({
                    u'requested':'1'
        })
        #pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})
        i=0
        for i in range(2):
            ret, frame = cap.read()
            cv2.imshow('image', frame)
            cv2.imwrite('u.jpg', frame)
        uploadImage(0)   
        messagebox.showinfo("Done","Request Sended Wait For Response")

def changeImageLabelFromFirebaseFirestone(NewName):
    db_ref=db.collection(u'data').document(u'image')
    d=db_ref.get()
    di=d.to_dict()
    db_ref=db.collection(u'data').document(u'image')
    db_ref.update({ u'0':NewName,
                    u'1':di['0'],
                     u'2':di['1'],
                      u'3':di['2'],
                       u'4':di['3'],
                       u'5':di['4'],
                       u'6':di['5'],
                       u'7':di['6'],
                       u'8':di['7'],
                       u'9':di['8']
        })

def uploadImage(i):
    import pyrebase
    firebaseConfig = {
    "apiKey": "AIzaSyB5ARBZqqaGzNFndYF_Uh24kTApa60YW6o",
    "authDomain": "facetest-b0450.firebaseapp.com",
    "databaseURL": "https://facetest-b0450.firebaseio.com",
    "projectId": "facetest-b0450",
    "storageBucket": "facetest-b0450.appspot.com",
    "messagingSenderId": "3495503607",
    "appId": "1:3495503607:web:b081bbb6f3b2116e3995f2",
    "measurementId": "G-0257TRM471"
    }
    firebase=pyrebase.initialize_app(firebaseConfig)
    storage=firebase.storage()
    time=str(datetime.now())
    p_o_c=""
    p_l=""
    if(i==1):
        p_o_c="image/"+time+".jpg"
        p_l="3.jpg"
    else:
        p_o_c="image/requesterImage/"+time+".jpg"
        p_l="u.jpg"
        db_ref=db.collection(u'data').document(u'requestedImage')
        db_ref.update({ u'1':time+".jpg" })
    storage.child(p_o_c).put(p_l)
    changeImageLabelFromFirebaseFirestone(time+".jpg")

def check(password,root):
    passw= password.get()
    if (passw=="123"):
        messagebox.showinfo("Done","Welcome Home")
        root.destroy()
        mainToStart()
    else:
        messagebox.showerror("Error","Incorrect Password")  
def secondPass():
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Home security")
    password_lable = Label(main_screen, text="Password * ")
    password_lable.pack()

    password_entry = Entry(main_screen, show='*')
    password_entry.pack()
    Button(text="Check", height="2", width="30",command=lambda:check(password_entry,main_screen)).pack()
    main_screen.mainloop()
def start(cap,root):
    i=0
    for i in range(10):
            ret, frame = cap.read()
            cv2.imshow('image', frame)
            cv2.imwrite('1.jpg', frame)
            if i==1:
                cv2.imwrite('3.jpg', frame)
            predictions = predict('1.jpg', model_path="trained_knn_model.clf")
            name=""
            for name1, (top, right, bottom, left) in predictions:
                print("- Found {} at ({}, {})".format(name1, left, top))
                name=name1          
            try:
                if name in ['Neeraj','puvarsan','sumit','vandana']:
                        i=1
                        break
                else:
                        continue
            except UnboundLocalError:
                pass
    root.wm_withdraw()
    thread = threading.Thread(target = lambda:uploadImage(1))
    prgs.processingPleaseWait('wait it will take time....', lambda: time.sleep(5),thread)
    root.wm_deiconify()
    if(i!=1):
        messagebox.showinfo("info","Known Face not detected try again please")
    if(i==1):
        root.destroy()
        secondPass()
def mainToStart():
    cap = cv2.VideoCapture(0)
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Home security")
    
    Label(text="please click on 'scan' & look at the camera", bg="blue", width="300", height="2", font=("Calibri", 13)).pack() 
    Label(text="").pack()
    Button(text="Scan", height="2", width="30",command=lambda:start(cap,main_screen)).pack() 
    Label(text="").pack()
    Button(text="Request", height="2", width="30",command=lambda:requestCheckThread(cap,main_screen)).pack()
    main_screen.mainloop()
mainToStart()
