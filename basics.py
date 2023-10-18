# import cv2
# import mediapipe as mp
# import time


# # Initialisations
# capture = cv2.VideoCapture(0)
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands()
# mp_drawing = mp.solutions.drawing_utils
# cur_time = 0
# prev_time = 0

# while True:
#     success, img = capture.read()

#     img = cv2.flip(img, 1) 

#     imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(imgRGB)

#     cur_time = time.time()
#     fps = 1/(cur_time-prev_time)
#     prev_time = cur_time

#     img_heigh, img_width, imgc = img.shape

#     if results.multi_hand_landmarks:
#         for hand_lms in results.multi_hand_landmarks:
#             mp_drawing.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)
#             for id, lm in enumerate(hand_lms.landmark):
#                 if id == 4 :
#                     mark_point_x, mark_point_y = int(lm.x*img_width), int(lm.y*img_heigh)
                    
#                     cv2.circle(img, (mark_point_x, mark_point_y), 10, (255, 0, 0), cv2.FILLED)

#     cv2.putText(img, str(int(fps)), (10,70), 
#                 cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0), 3)

#     # Displaying Image
#     cv2.imshow("Image", img)
#     cv2.waitKey(1)

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


def win_volume_control(volume_size):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    #volume.GetMute()
    #volume.GetMasterVolumeLevel()
    min_vol, max_vol = volume.GetVolumeRange()
    volume.SetMasterVolumeLevel(volume_size, None)

if __name__=="__main__":
    win_volume_control(-20)