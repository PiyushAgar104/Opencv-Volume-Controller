import cv2
import mediapipe as mp
import math
import time
import ctypes
from pycaw.pycaw import AudioUtilities

user32 = ctypes.WinDLL("user32", use_last_error=True)

VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF
KEYEVENTF_KEYUP = 0x0002


def press_volume_key(key):
    user32.keybd_event(key, 0, 0, 0)
    user32.keybd_event(key, 0, KEYEVENTF_KEYUP, 0)


devices = AudioUtilities.GetSpeakers()
volume = devices.EndpointVolume

min_db, max_db, _ = volume.GetVolumeRange()

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)

if not cap.isOpened():
    print("Camera open nahi ho raha!")
    exit()

current_volume = int(
    volume.GetMasterVolumeLevelScalar() * 100
)

target_volume = current_volume

last_update = 0
update_delay = 0.08

previous_time = 0

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    results = hands.process(rgb)

    if results.multi_hand_landmarks:

        hand = results.multi_hand_landmarks[0]

        h, w, _ = frame.shape

        thumb = hand.landmark[4]
        index = hand.landmark[8]

        thumb_x = int(thumb.x * w)
        thumb_y = int(thumb.y * h)

        index_x = int(index.x * w)
        index_y = int(index.y * h)

        distance = math.hypot(
            index_x - thumb_x,
            index_y - thumb_y
        )

        min_distance = 35
        max_distance = 220

        target_volume = (
            (distance - min_distance)
            / (max_distance - min_distance)
        ) * 100

        target_volume = int(
            max(0, min(100, target_volume))
        )

        now = time.time()

        if now - last_update >= update_delay:

            if abs(target_volume - current_volume) >= 2:

                if target_volume > current_volume:

                    press_volume_key(VK_VOLUME_UP)

                else:

                    press_volume_key(VK_VOLUME_DOWN)

                current_volume = target_volume

                scalar = current_volume / 100

                volume.SetMasterVolumeLevelScalar(
                    scalar,
                    None
                )

                last_update = now

        cv2.circle(
            frame,
            (thumb_x, thumb_y),
            12,
            (255, 0, 255),
            cv2.FILLED
        )

        cv2.circle(
            frame,
            (index_x, index_y),
            12,
            (255, 0, 255),
            cv2.FILLED
        )

        cv2.line(
            frame,
            (thumb_x, thumb_y),
            (index_x, index_y),
            (255, 0, 255),
            4
        )

        mp_draw.draw_landmarks(
            frame,
            hand,
            mp_hands.HAND_CONNECTIONS
        )

        cv2.putText(
            frame,
            f"Distance: {int(distance)}",
            (30, 560),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

    current_volume = int(
        volume.GetMasterVolumeLevelScalar() * 100
    )

    bar_x = 60
    bar_y = 170
    bar_width = 55
    bar_height = 350

    cv2.rectangle(
        frame,
        (bar_x, bar_y),
        (bar_x + bar_width, bar_y + bar_height),
        (255, 255, 255),
        3
    )

    filled_height = int(
        bar_height * current_volume / 100
    )

    cv2.rectangle(
        frame,
        (
            bar_x,
            bar_y + bar_height - filled_height
        ),
        (
            bar_x + bar_width,
            bar_y + bar_height
        ),
        (0, 220, 80),
        cv2.FILLED
    )

    cv2.putText(
        frame,
        f"PC Volume: {current_volume}%",
        (160, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.1,
        (0, 255, 0),
        3
    )

    cv2.putText(
        frame,
        f"Target: {target_volume}%",
        (160, 160),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "FINGER VOLUME CONTROLLER",
        (380, 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )

    if results.multi_hand_landmarks:

        cv2.putText(
            frame,
            "HAND DETECTED",
            (900, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    else:

        cv2.putText(
            frame,
            "SHOW YOUR HAND",
            (900, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 180, 255),
            2
        )

    current_time = time.time()

    fps = (
        1 / (current_time - previous_time)
        if previous_time != 0
        else 0
    )

    previous_time = current_time

    cv2.putText(
        frame,
        f"FPS: {int(fps)}",
        (1100, 680),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "Q = Exit",
        (950, 650),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )

    cv2.imshow(
        "Finger Volume Controller",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()