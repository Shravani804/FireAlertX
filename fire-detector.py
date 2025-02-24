import cv2
import numpy as np
import pygame
import time

Alarm_Status = False
Fire_Reported = 0

pygame.mixer.init()
pygame.mixer.music.load('alarm-sound.mp3')

def play_alarm_sound_function():
    pygame.mixer.music.play(-1) 
    time.sleep(1)


video = cv2.VideoCapture(0)

while True:
    grabbed, frame = video.read()
    if not grabbed:
        break
    
    blur = cv2.GaussianBlur(frame, (21, 21), 0)

    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    

    lower = [18, 50, 140]
    upper = [35, 255, 255]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    mask = cv2.inRange(hsv, lower, upper)
   
    output = cv2.bitwise_and(frame, hsv, mask=mask)

    no_red = cv2.countNonZero(mask)

    if int(no_red) > 10000:
        Fire_Reported = Fire_Reported + 1

    cv2.imshow("output", output)
    print(Fire_Reported)
    if Fire_Reported >= 1:

        if Alarm_Status == False:
            play_alarm_sound_function()
            # break        
            Alarm_Status = True
            print("Fire is Detected")
        else:
              Alarm_Status = False
              Fire_Reported = 0
              pygame.mixer.music.stop()
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cv2.destroyAllWindows()
video.release()
