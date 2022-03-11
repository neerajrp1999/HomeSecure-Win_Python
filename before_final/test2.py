"""
import firebase_admin
from firebase_admin import credentials , firestore#,storage
cre=credentials.Certificate("firebase_admin.json")
d_app=firebase_admin.initialize_app(cre)
db =firestore.client()
from google.cloud import storage

#response=getQuote()
def update():
    #firestore
    a="neeraj"
    b="rr"
    db_ref=db.collection(u'data').document(u'data')
    db_ref.update({ u'f':a,

                u'f1':b
        })
    d=db_ref.get()
    d=d.to_dict()
    print("{}".format(d['f']))
	
	
	
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder


import cv2
import numpy as np

img_path = 'u.jpg'
img = cv2.imread(img_path, 0)
print(img)
text_file = open("Output.txt", "w")
text_file.write("")
text_file.close()
i=0
text_file = open("Output.txt", "a")

for i in range (len(img)):
    #print(len(img))
    print(img[i])
    text_file.write(str(img[i]))
text_file.close()

"""


def uploadImage():
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
    p_o_c="image/requesterImage/"+time+".jpg"
    p_l="u.jpg"
    storage.child(p_o_c).put(p_l)
uploadImage()
