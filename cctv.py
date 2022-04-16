from flask import Flask, send_file, Response
import cv2
from datetime import datetime
import os
import glob

app = Flask(__name__)



def getNow() :
    now = datetime.now()     
    return now.strftime("%Y%m%d_%H%M%S")



def getFiles(path) :
    return [os.path.split(f)[-1]  for f in glob.glob(path) ] 

@app.route('/')
def hello():    
    
    html = """       
    
    
    자율주행 모니터링 시스템 <br>    
    
    <img src=/video  width=320 >
    
    """
    
    return html


@app.route('/image')
def image():    
    return send_file('static/donut.jpg', mimetype='image/jpg')

@app.route('/opencv')
def opencv():    
    
    return "hello"

_frame = {}


def gen_frames():  
    
    global _frame

    
    #cap = cv2.VideoCapture("video.mp4")
    cap = cv2.VideoCapture(0)
    
    
    
    
    while True:
        success, frame = cap.read()  # read the camera frame
        
        _frame = frame.copy()
        
        print("^^")
        if not success:
                break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
            
            

@app.route('/video')
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame') 


@app.route('/capture')
def capture():    
    
    cv2.imwrite('static/cctv/capture' + getNow() + '.jpg', _frame)    
    
    return "ok"

@app.route('/control')
def control():       
   
    res = getFiles('static/cctv/*')

    html = ""
    for fname in res :
        html += f"<img src=static/cctv/{fname} width=200 height=200>"
    
    return html

    
if __name__ == "__main__":
    app.run(debug=True)
