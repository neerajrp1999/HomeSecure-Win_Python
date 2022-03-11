from datetime import datetime
import time, threading
from tkinter import *
from tkinter import messagebox
from firebase import firebase
import cv2
from face_recognition_knn import *
import progress as prgs
def requestCheckThread(cap,root1):
    root1.wm_withdraw()
    thread = threading.Thread(target = lambda:requestCheck(cap,root1))
    prgs.processingPleaseWait('wait it will take time....', lambda: time.sleep(5),thread)
    root1.wm_deiconify()
def requestCheck(cap,root):
    from firebase import firebase
    firebase = firebase.FirebaseApplication('https://facetest-b0450.firebaseio.com/', None)
    data = firebase.get('/request/', None)
    a=data[list(data.keys())[0]]
    s=data[list(data.keys())[1]]
    if(a=='1'):
        firebase.put('/request/','accepted','0')
        firebase.put('/request/','sended','0')
        messagebox.showinfo("Done","Welcome Home")
        root.destroy()
        mainToStart()
    if(s=='1'):
        messagebox.showinfo("Request","Request already Sended Wait For Response")
    if(s=='0'):
        firebase.put('/request/','sended','1')
        i=0
        for i in range(2):
            ret, frame = cap.read()
            cv2.imshow('image', frame)
            cv2.imwrite('u.jpg', frame)
        uploadImage(0)   
        messagebox.showinfo("Done","Request Sended Wait For Response")
def changeImageLabelFromFirebase(NewName):
    from firebase import firebase
    firebase = firebase.FirebaseApplication('https://facetest-b0450.firebaseio.com/', None)
    result = firebase.get('/images/', None)
    #print(result[list(result.keys())[0]])#*******
    firebase.put('/images/','0',NewName)
    firebase.put('/images/','1',result[0])
    firebase.put('/images/','2',result[1])
    firebase.put('/images/','3',result[2])
    firebase.put('/images/','4',result[3])
    firebase.put('/images/','5',result[4])
    firebase.put('/images/','6',result[5])
    firebase.put('/images/','7',result[6])
    firebase.put('/images/','8',result[7])
    firebase.put('/images/','9',result[8])

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
        from firebase import firebase
        firebase = firebase.FirebaseApplication('https://facetest-b0450.firebaseio.com/', None)
        firebase.put('/requesterImage/','0',time+".jpg")
    storage.child(p_o_c).put(p_l)
    changeImageLabelFromFirebase(time+".jpg")

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
