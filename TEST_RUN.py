import pygame
import random
import sys
import cv2
import mediapipe as mp
import time

from button import Button
from combined_game_environment import Obstacle, spawn_obstacle, obs_imgs, LANES, scroll_bg, get_background
from loosing_screen import check_for_collision
from player import Player

# ------------------ INITIAL SETUP ------------------
pygame.init()

# SCREEN & FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

# COLORS
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)

# Pygame objects
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Penguin Surf")

# LOAD IMAGES
menu_bg = pygame.image.load("images/babyblue.png")
menu_bg = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

BG_IMAGE = pygame.image.load("images/background.png").convert()
BG_IMAGE = pygame.transform.scale(BG_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
BG_HEIGHT = BG_IMAGE.get_height()

BUTTON_IMG = pygame.image.load("images/button.png").convert()
BUTTON_IMG = pygame.transform.scale(BUTTON_IMG, (150, 75))

# FONTS
font_small = pygame.font.SysFont('Lucida Sans', 20)
font_big = pygame.font.SysFont('Lucida Sans', 24)

# BACKGROUND
bg = get_background()

# ------------------ GESTURE SETUP ------------------
PAUSE_EVENT = pygame.USEREVENT + 1
RESUME_EVENT = pygame.USEREVENT + 2
LEFT_EVENT = pygame.USEREVENT + 3
RIGHT_EVENT = pygame.USEREVENT + 4

gesture_buffer = []
BUFFER_FRAMES = 10

def get_gesture(handLms):
    TH = mp.solutions.hands.HandLandmark
    tips = [handLms.landmark[i] for i in [
        TH.THUMB_TIP, TH.INDEX_FINGER_TIP, TH.MIDDLE_FINGER_TIP,
        TH.RING_FINGER_TIP, TH.PINKY_TIP
    ]]
    wrist = handLms.landmark[TH.WRIST]
    index_tip = tips[1]

    THRESH = 0.12
    if index_tip.x < wrist.x - THRESH:
        return "right"
    if index_tip.x > wrist.x + THRESH:
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

# ------------------ UTILITY FUNCTIONS ------------------
def print_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def show_game_over_screen(current_score):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                cv2.destroyAllWindows()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

        screen.fill(BLACK)
        print_text('GAME OVER', font_big, WHITE, 200)
        print_text('SCORE: ' + str(current_score) + ' m', font_big, WHITE, 250)
        print_text('PRESS SPACE TO PLAY AGAIN', font_big, WHITE, 300)
        pygame.display.flip()
        clock.tick(FPS)

# ------------------ GAME LOOP ------------------
def play():
    score = 0
    scroll = 0
    spawn_timer = 0
    obstacles = []
    collisions = 0
    damage_cooldown = 0.0
    is_game_over = False
    game_start_time = pygame.time.get_ticks()

    penguin = Player()

    # Gesture setup
    mp_draw = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1)

    # initialize camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    running = True
    while running:
        dt = clock.tick(FPS) / 1000
        if damage_cooldown > 0:
            damage_cooldown -= dt

        # --- Handle keyboard & gesture events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    penguin.move_left()
                elif event.key == pygame.K_RIGHT:
                    penguin.move_right()
            elif event.type == LEFT_EVENT:
                penguin.move_left()
            elif event.type == RIGHT_EVENT:
                penguin.move_right()

        # --- Camera gesture detection ---
        ret, frame = cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)
            gesture = None
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                gesture = smooth_gesture(get_gesture(results.multi_hand_landmarks[0]))
            if gesture == "left":
                pygame.event.post(pygame.event.Event(LEFT_EVENT))
            elif gesture == "right":
                pygame.event.post(pygame.event.Event(RIGHT_EVENT))

            cv2.imshow("Gesture Camera", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                running = False

        # --- Background scrolling ---
        scroll = scroll_bg(screen, bg, scroll, 5)

        # --- Update penguin ---
        penguin.update(dt)
        penguin.draw(screen)

        # --- Spawn obstacles ---
        if not is_game_over:
            spawn_timer += 1
            if spawn_timer > 90:
                obstacles.append(spawn_obstacle(5))
                spawn_timer = 0

            for obs in obstacles[:]:
                obs.update()
                obs.draw(screen)
                if damage_cooldown <= 0 and check_for_collision(penguin, obs):
                    collisions += 1
                    damage_cooldown = 1.0
                    obstacles.remove(obs)
                    if collisions >= 3:
                        is_game_over = True
                        break
            obstacles = [obs for obs in obstacles if obs.rect.top <= SCREEN_HEIGHT]
        else:
            survival_time = (pygame.time.get_ticks() - game_start_time) / 1000.0
            score = int(survival_time * 15)
            show_game_over_screen(score)
            # Reset game state
            score = 0
            scroll = 0
            obstacles.clear()
            collisions = 0
            is_game_over = False
            game_start_time = pygame.time.get_ticks()

        pygame.display.flip()

    # Release camera when quitting
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()
    sys.exit()

# ------------------ MENU ------------------
def menu():
    while True:
        screen.blit(menu_bg, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BUTTON = Button(image=BUTTON_IMG, x_pos=400, y_pos=250, text_input="PLAY")
        QUIT_BUTTON = Button(image=BUTTON_IMG, x_pos=400, y_pos=350, text_input="QUIT")

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                cv2.destroyAllWindows()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    cv2.destroyAllWindows()
                    sys.exit()

        pygame.display.update()

# ------------------ RUN ------------------
menu()

