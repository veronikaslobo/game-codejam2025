#import fns
import cv2   #for the camera
import mediapipe as mp   #for the hand detection
import pygame   # to send the outputs

pygame.init()  #to use the .events

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("penguin surf")

# my gesture events for the game
PAUSE_EVENT = pygame.USEREVENT + 1
RESUME_EVENT = pygame.USEREVENT + 2
LEFT_EVENT = pygame.USEREVENT + 3
RIGHT_EVENT = pygame.USEREVENT + 4

mp_draw = mp.solutions.drawing_utils #to draw dots and lines on the hand landmarks.
mp_hands = mp.solutions.hands  # Loads the MediaPipe Hand
# -----MEDIAPIPE-----
# MediaPipes model.
hands = mp_hands.Hands(max_num_hands=1) # cuz we only need one

# use cap to start the camera
cap = cv2.VideoCapture(0)  # usually 0 for default camera

#create a gesture buffer so that
gesture_buffer = []
BUFFER_FRAMES = 15

#gesture detection function
def get_gesture(handLms):
    TH = mp_hands.HandLandmark
    tips = [handLms.landmark[i] for i in [TH.THUMB_TIP, TH.INDEX_FINGER_TIP, TH.MIDDLE_FINGER_TIP,
                                          TH.RING_FINGER_TIP, TH.PINKY_TIP ]]
    wrist = handLms.landmark[TH.WRIST]

    # for the fist
    if all(tip.y > wrist.y for tip in tips):
        return "fist"
    #palm up
    if all(tip.y < wrist.y for tip in tips):
        return "palm_up"
    #left and right
    index_tip = tips[1] #for detecting a point
    other_tips = [tips[i] for i in [0,2,3,4]]
    if index_tip.y < wrist.y or all(t.y > wrist.y for t in other_tips):
        if index_tip.x < wrist.x - 0.3:
            return "right"
        elif index_tip.x > wrist.x + 0.3:
            return "left"
    return None  # if no gesture matches

# clearing buffer if no gesture
def smooth_gesture(g):
    global gesture_buffer
    if g is None:
        gesture_buffer = []
        return None

    gesture_buffer.append(g)
    if len(gesture_buffer) > BUFFER_FRAMES:
        gesture_buffer.pop(0)

    # firing event/signal once it works
    if len(gesture_buffer) == BUFFER_FRAMES and len(set(gesture_buffer)) == 1:
        gesture_buffer.clear()
        return g
    return None

# ----main loop----
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

    # the camera detection
    ret, frame = cap.read()
    if not ret:
        continue
    # Convert BGR → RGB cuz media pipe needs rgb
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    gesture = None
    # to show the lines on the hands
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw the hand landmarks and connections on the frame
            mp_draw.draw_landmarks(
                frame,  # the frame you want to draw on
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS  # draw lines between landmarks
            )
        gesture = smooth_gesture(get_gesture(results.multi_hand_landmarks[0]))

    # sending the signals for game response
    if gesture == "palm_up":
        pygame.event.post(pygame.event.Event(PAUSE_EVENT))
    elif gesture == "fist":
        pygame.event.post(pygame.event.Event(RESUME_EVENT))
    elif gesture == "left":
        pygame.event.post(pygame.event.Event(LEFT_EVENT))
    elif gesture == "right":
        pygame.event.post(pygame.event.Event(RIGHT_EVENT))

    # to show the webcam (after drawing landmarks!)
    cv2.imshow("Gesture Camera", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        running = False

# to finish
cap.release()
cv2.destroyAllWindows()
pygame.quit() #might not need
