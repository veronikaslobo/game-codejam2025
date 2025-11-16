import pygame
import os
# import mediapipe as mp

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
BUFFER_FRAMES = 5

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
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#         if event.type == PAUSE_EVENT:
#             print("PAUSE event fired")
#         if event.type == RESUME_EVENT:
#             print("RESUME event fired")
#         if event.type == LEFT_EVENT:
#             print("LEFT event fired")
#         if event.type == RIGHT_EVENT:
#             print("RIGHT event fired")
#
#     # the camera detection
#     ret, frame = cap.read()
#     if not ret:
#         continue
#     # Convert BGR → RGB cuz media pipe needs rgb
#     frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     results = hands.process(frame_rgb)
#
#     gesture = None
#     # to show the lines on the hands
#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             # Draw the hand landmarks and connections on the frame
#             mp_draw.draw_landmarks(
#                 frame,  # the frame you want to draw on
#                 hand_landmarks,
#                 mp_hands.HAND_CONNECTIONS  # draw lines between landmarks
#             )
#         gesture = smooth_gesture(get_gesture(results.multi_hand_landmarks[0]))
#
#     # sending the signals for game response
#     if gesture == "palm_up":
#         pygame.event.post(pygame.event.Event(PAUSE_EVENT))
#     elif gesture == "fist":
#         pygame.event.post(pygame.event.Event(RESUME_EVENT))
#     elif gesture == "left":
#         pygame.event.post(pygame.event.Event(LEFT_EVENT))
#     elif gesture == "right":
#         pygame.event.post(pygame.event.Event(RIGHT_EVENT))
#
#     # to show the webcam (after drawing landmarks!)
#     cv2.imshow("Gesture Camera", frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         running = False


# Test window for car
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Movement")
timer = pygame.time.Clock()
fps = 60
LEFT_LANE_POSITION = 140
MIDDLE_LANE_POSITION = 350
RIGHT_LANE_POSITION = 600

# Class of our car (can be smt else, decide later)
class Player:
    def __init__(self):
        self.y_axis_position = 8.7 * HEIGHT / 10 # to see with the UI
        self.width = 75
        self.height = 75
        self.lane_width = WIDTH // 3
        self.current_lane = 1
        self.lane_positions = [LEFT_LANE_POSITION, MIDDLE_LANE_POSITION, RIGHT_LANE_POSITION]
        self.x_axis_position = self.lane_positions[self.current_lane]
        self.target_x = self.x_axis_position
        self.slide_speed = 0.07 # pixels/movement
        self.is_moving = False

        image_path = "player/penguin_image1.png"

        #Checks for filenotfound
        if not os.path.exists(image_path):
            print(f"Error: Could not find {image_path}")
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 0))
        else:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

    # Drawing itself on the map
    def draw(self, surface):
        surface.blit(self.image, (self.x_axis_position, self.y_axis_position))



    def move_right(self):
        if self.current_lane < 2 and not self.is_moving:
            self.current_lane += 1
            self.target_x = self.lane_positions[self.current_lane]
            self.is_moving = True


    def move_left(self):
        if self.current_lane > 0:
            self.current_lane -= 1
            self.target_x = self.lane_positions[self.current_lane]
            self.is_moving = True

    def update(self):
        self.x_axis_position += (self.target_x - self.x_axis_position) * self.slide_speed

        if abs(self.target_x - self.x_axis_position) < 0.5:
            self.x_axis_position = self.target_x
            self.is_moving = False


    # def accelerate(self):



def player_move(penguin):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.key == pygame.K_RIGHT:
            penguin.move_right()
        if event.key == pygame.K_LEFT:
            penguin.move_left()
    return False



# main game
def main():

   peng = Player()
   game_over = False

# closes the game if the user presses on X
   run = True


   while run:
       for event in pygame.event.get():
            if event.type == pygame.QUIT:
               run = False
            if event.type == PAUSE_EVENT:
                peng.move_right()
            if event.type == LEFT_EVENT:
               peng.move_left()
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
       peng.update()
       screen.fill((250,250,204))
       peng.draw(screen)
       pygame.display.flip()

main()

# to finish
cap.release()
cv2.destroyAllWindows()
pygame.quit()


