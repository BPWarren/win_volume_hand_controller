import cv2
import mediapipe
import numpy as np
import time
import math
import hand_tracking_module as htm

import pyautogui

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


def win_volume_control(volume):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    #volume.GetMute()
    #volume.GetMasterVolumeLevel()
    print(volume.GetVolumeRange())
    volume.SetMasterVolumeLevel(volume, None)

def linux_volume_control(volume):

    pass

# Initialisations
cap = cv2.VideoCapture(0)
detector = htm.HandDetector()

cur_time = 0
prev_time = 0








while True:
    success, img =  cap.read()
    if not success:
        print("ERROR : VIDEO CAN'T BE RESOLVE")
        break

    img = cv2.flip(img, 1)
    cur_time = time.time()
    fps = 1/(cur_time-prev_time)
    prev_time = cur_time

    img = detector.detect_hands(img)

    lm_list = detector.landmarks_coordinate(img, show_pointer=False)
    if len(lm_list) !=0:
        #print(lm_list[4], lm_list[8])
        # Controling landmarks
        clm4_x, clm4_y= lm_list[4][1], lm_list[4][2]
        clm8_x, clm8_y = lm_list[8][1], lm_list[8][2]

        cv2.circle(img, (clm4_x, clm4_y), 11, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (clm8_x, clm8_y), 11, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (clm4_x, clm4_y), (clm8_x, clm8_y), (255,0, 0), 2)
        cv2.circle(img, ((clm4_x+clm8_x)//2, (clm4_y+clm8_y)//2), 7, (255,0, 0), cv2.FILLED)

        control_lenth = math.hypot(clm4_x-clm8_x, clm4_y-clm8_y)
        print(control_lenth)

        if control_lenth<18:
            cv2.circle(img, ((clm4_x+clm8_x)//2, (clm4_y+clm8_y)//2), 7, (48, 79, 254), cv2.FILLED)
        
        elif control_lenth>160:
            cv2.circle(img, ((clm4_x+clm8_x)//2, (clm4_y+clm8_y)//2), 7, (0, 200, 83), cv2.FILLED)



    cv2.putText(img, "FPS : {}".format(str(int(fps))), (10,30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF==ord("q"):
        break