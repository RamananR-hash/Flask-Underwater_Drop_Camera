
from calendar import c
from flask import Flask, render_template, Response, request,flash,redirect
from flask import Flask, flash, redirect, render_template,request, url_for
import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread
import webbrowser

global capture,rec_frame, grey, switch, neg, face, rec, out 
capture=0
grey=0
neg=0
face=0
switch=0
rec=0
chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
c=0
data=0
#make shots directory to save pics
try:
    os.mkdir('./shots')
except OSError as error:
    pass

#instatiate flask app  
app = Flask(__name__, template_folder='./template')


camera = cv2.VideoCapture(0)

def record(out):
    global rec_frame
    while(rec):
        time.sleep(0.05)
        out.write(rec_frame)



 

def gen_frames():  # generate frame by frame from camera
    global out, capture,rec_frame,data
    while True:
        success, frame = camera.read() 
        if success:
            if(rec):
                rec_frame=frame
                frame= cv2.putText(cv2.flip(frame,1),".", (70,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),40)
                frame=cv2.flip(frame,1)
            if(data==1):
                rec_frame=frame
                frame= cv2.putText(cv2.flip(frame,1),".", (600,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),40)
                frame=cv2.flip(frame,1) 
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
                
        else:
            pass


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/requests',methods=['POST','GET'])
def tasks():
    global switch,camera,c,data
    if request.method == 'POST':
       if  request.form.get('stop') == 'ON/OFF':
                c+=1
                if(c%2==0):
                    print("ON")
                    data=1
                else:
                    data=0
                    print("OFF")
       elif  request.form.get('rec') == 'START/STOP RECORDING':
            global rec, out
            rec= not rec
            if(rec):
                now=datetime.datetime.now() 
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(str("shots//")+'vid_{}.avi'.format(str(now).replace(":",'')), fourcc, 20.0, (640, 480))
                thread = Thread(target = record, args=[out,])
                thread.start()
            elif(rec==False):
                out.release()
       elif  request.form.get('Download') == 'DOWNLOAD':
            print("Download Called ") 
            #return redirect('localhost')

                          
                 
    elif request.method=='GET':
        return render_template('index.html')
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
    
camera.release()
cv2.destroyAllWindows()     

