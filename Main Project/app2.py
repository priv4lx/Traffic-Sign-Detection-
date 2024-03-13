from threading import Thread

import pyttsx3

from ultralytics import YOLO
import cv2
import math

def say(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 200)
    engine.say(text)
    engine.runAndWait()
    

def thr(word):
    k = Thread(target=say, args=(word,))
    k.start()

cap=cv2.VideoCapture(0)
i=0
frame_width=int(cap.get(3))
frame_height = int(cap.get(4))

out=cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))

model=YOLO("traffic2.pt")
classNames = ["hump", "no entry", "no overtaking", "no stopping", "no u turn", "parking", "roadwork", "roundabout",
                  "speed limit 40", "stop"
                  ]

while True:
    success, img = cap.read()
    

    results=model(img,stream=True,conf=0.5)
    for r in results:
        boxes=r.boxes
        for box in boxes:
            i+=1
            x1,y1,x2,y2=box.xyxy[0]
            #print(x1, y1, x2, y2)
            x1,y1,x2,y2=int(x1), int(y1), int(x2), int(y2)
            print(x1,y1,x2,y2)
            cv2.rectangle(img, (x1,y1), (x2,y2), (255,0,255),3)
            #print(box.conf[0])
            conf=math.ceil((box.conf[0]*100))/100
            cls=int(box.cls[0])
            class_name=classNames[cls]
            label=f'{class_name}{conf}'
            name=f'{class_name}'
            
            t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
            #print(t_size)
            c2 = x1 + t_size[0], y1 - t_size[1] - 3
            cv2.rectangle(img, (x1,y1), c2, [255,0,255], -1, cv2.LINE_AA)  # filled
            cv2.putText(img, label, (x1,y1-2),0, 1,[255,255,255], thickness=1,lineType=cv2.LINE_AA)

            thr(name)

    out.write(img)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
out.release()
cap.release()
cv2.destroyAllWindows()
