# import fns
import cv2  # for the camera
import mediapipe as mp  # for the hand detection
import pygame  # to send the outputs
import numpy as np

pygame.init()  # to use the .events

screen = pygame.display.set_mode((100, 100))
pygame.display.set_caption("penguin surf")

# my gesture events for the game
PAUSE_EVENT = pygame.USEREVENT + 1
RESUME_EVENT = pygame.USEREVENT + 2
LEFT_EVENT = pygame.USEREVENT + 3
RIGHT_EVENT = pygame.USEREVENT + 4

mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(max_num_hands=1)

cap = cv2.VideoCapture(0)

# ---------------------------
# FIXED CAMERA WINDOW (150x150)
# ---------------------------
WINDOW_NAME = "Camera Feed"
display_width = 500
display_height = 300

cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

# macOS fix: show 1 resized frame BEFORE resizing window
ret, frame = cap.read()
if ret:
    frame = cv2.resize(frame, (display_width, display_height))
    cv2.imshow(WINDOW_NAME, frame)
    cv2.waitKey(1)

# Now resize window
cv2.resizeWindow(WINDOW_NAME, display_width, display_height)

# ---------------------------
# GESTURE BUFFER + FUNCTIONS
# ---------------------------
gesture_buffer = []
BUFFER_FRAMES = 15


def get_gesture(handLms):
    TH = mp_hands.HandLandmark
    tips = [handLms.landmark[i] for i in [TH.THUMB_TIP, TH.INDEX_FINGER_TIP, TH.MIDDLE_FINGER_TIP,
                                          TH.RING_FINGER_TIP, TH.PINKY_TIP]]
    wrist = handLms.landmark[TH.WRIST]

    if all(tip.y > wrist.y for tip in tips):
        return "fist"

    if all(tip.y < wrist.y for tip in tips):
        return "palm_up"

    index_tip = tips[1]
    other_tips = [tips[i] for i in [0, 2, 3, 4]]
    if index_tip.y < wrist.y or all(t.y > wrist.y for t in other_tips):
        if index_tip.x < wrist.x - 0.3:
            return "right"
        elif index_tip.x > wrist.x + 0.3:
            return "left"
    return None


def smooth_gesture(g):
    global gesture_buffer
    if g is None:
        gesture_buffer = []
        return None

    gesture_buffer.append(g)
    if len(gesture_buffer) > BUFFER_FRAMES:
        gesture_buffer.pop(0)

    if len(gesture_buffer) == BUFFER_FRAMES and len(set(gesture_buffer)) == 1:
        gesture_buffer.clear()
        return g
    return None


# ---------------------------
# MAIN LOOP
# ---------------------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == PAUSE_EVENT:
            print("PAUSE event fired")
        if event.type == RESUME_EVENT:
            print("RESUME event fired")
        if event.type == LEFT_EVENT:
            print("LEFT event fired")
        if event.type == RIGHT_EVENT:
            print("RIGHT event fired")

    ret, frame = cap.read()
    if not ret:
        continue

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    gesture = None

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )
        gesture = smooth_gesture(get_gesture(results.multi_hand_landmarks[0]))

    if gesture == "palm_up":
        pygame.event.post(pygame.event.Event(PAUSE_EVENT))
    elif gesture == "fist":
        pygame.event.post(pygame.event.Event(RESUME_EVENT))
    elif gesture == "left":
        pygame.event.post(pygame.event.Event(LEFT_EVENT))
    elif gesture == "right":
        pygame.event.post(pygame.event.Event(RIGHT_EVENT))

    # Show webcam in the fixed-size window
    display_frame = cv2.resize(frame, (display_width, display_height))
    cv2.imshow(WINDOW_NAME, display_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        running = False

cap.release()
cv2.destroyAllWindows()
pygame.quit()
