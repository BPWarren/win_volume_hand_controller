import cv2
import mediapipe
import numpy as np
import time
import math
import hand_tracking_module as htm


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


# Initialisations
cap = cv2.VideoCapture(0)
detector = htm.HandDetector()

cur_time = 0
prev_time = 0

# Limite size
min_hand = 18
max_hand = 160

# Volume
min_vol = -65
max_vol = 0

# indicator
vol_indicator = 0
vol_percent = 0
while True:
    success, img = cap.read()
    if not success:
        print("ERROR : VIDEO CAN'T BE RESOLVE")
        break

    img = cv2.flip(img, 1)
    cur_time = time.time()
    fps = 1 / (cur_time - prev_time)
    prev_time = cur_time

    img = detector.detect_hands(img)

    lm_list = detector.landmarks_coordinate(img, show_pointer=False)
    if len(lm_list) != 0:
        # print(lm_list[4], lm_list[8])
        # Controling landmarks
        clm4_x, clm4_y = lm_list[4][1], lm_list[4][2]
        clm8_x, clm8_y = lm_list[8][1], lm_list[8][2]

        cv2.circle(img, (clm4_x, clm4_y), 11, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (clm8_x, clm8_y), 11, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (clm4_x, clm4_y), (clm8_x, clm8_y), (255, 0, 0), 2)
        cv2.circle(
            img,
            ((clm4_x + clm8_x) // 2, (clm4_y + clm8_y) // 2),
            7,
            (255, 0, 0),
            cv2.FILLED,
        )

        control_lenth = math.hypot(clm4_x - clm8_x, clm4_y - clm8_y)

        volume_size = np.interp(control_lenth, [min_hand, max_hand], [min_vol, max_vol])
        win_volume_control(volume_size)

        if control_lenth < 18:
            cv2.circle(
                img,
                ((clm4_x + clm8_x) // 2, (clm4_y + clm8_y) // 2),
                7,
                (48, 79, 254),
                cv2.FILLED,
            )

        elif control_lenth > 160:
            cv2.circle(
                img,
                ((clm4_x + clm8_x) // 2, (clm4_y + clm8_y) // 2),
                7,
                (0, 200, 83),
                cv2.FILLED,
            )

        cv2.rectangle(img, (50, 300), (80, 100), (255, 0, 0), 3)
        vol_indicator = np.interp(control_lenth, [min_hand, max_hand], [300, 100])

        cv2.rectangle(img, (50, 300), (80, int(vol_indicator)), (255, 0, 0), cv2.FILLED)

        vol_percent = np.interp(control_lenth, [min_hand, max_hand], [0, 100])
        cv2.putText(
            img,
            "{}%".format(str(int(vol_percent))),
            (30, 350),
            cv2.FONT_HERSHEY_COMPLEX,
            1,
            (255, 0, 0),
            1,
        )

    cv2.putText(
        img,
        "FPS : {}".format(str(int(fps))),
        (10, 30),
        cv2.FONT_HERSHEY_COMPLEX,
        1,
        (255, 0, 0),
        3,
    )

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
