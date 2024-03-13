
import pyttsx3
engine=pyttsx3.init()
import threading
i=0
def say(text):
   voices = engine.getProperty('voices')
   engine.setProperty('voice', voices[1].id)
   engine.setProperty('rate', 200)
   engine.say(text)
   engine.runAndWait()

def thr(word):
   k=threading.Thread(target=say, args=(word,))
   k.start()
   #k.run()
   
f = open("1.txt", "r")
while(True):
   line=f.readline()
   if not line:
      break
   thr(line)
    
   #thr(f.read())
    

