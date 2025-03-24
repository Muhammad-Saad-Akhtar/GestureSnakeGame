import cvzone
import cv2
import numpy as np
import math
import random
import time
import pygame  # For playing sounds
from cvzone.HandTrackingModule import HandDetector

# Initializing pygame mixer for sound effects
pygame.mixer.init()

# Loading sound files
food_eat_sound = pygame.mixer.Sound(r"C:\Users\HP\Desktop\Others\GestureSnakeGame\food eating.mp3")
poison_eat_sound = pygame.mixer.Sound(r"C:\Users\HP\Desktop\Others\GestureSnakeGame\posion eating.mp3")

# Constants for dimensions
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

detector = HandDetector(detectionCon=0.8, maxHands=1)

class SnakeGame:
    def __init__(self, food_path, bonus_food_path, poison_food_path):
        self.points = []
        self.lengths = []
        self.current_length = 0
        self.total_allowed_length = 150
        self.head_previous = (0, 0)
        self.score = 0
        self.game_over = False

        # Loading food images
        self.food_img = cv2.imread(food_path, cv2.IMREAD_UNCHANGED)
        self.bonus_food_img = cv2.imread(bonus_food_path, cv2.IMREAD_UNCHANGED)
        self.poison_food_img = cv2.imread(poison_food_path, cv2.IMREAD_UNCHANGED)

        # Getting food dimensions
        self.food_height, self.food_width, _ = self.food_img.shape
        self.bonus_food_height, self.bonus_food_width, _ = self.bonus_food_img.shape
        self.poison_food_height, self.poison_food_width, _ = self.poison_food_img.shape

        # Initializing food locations
        self.food_location = (0, 0)
        self.bonus_food_location = (0, 0)
        self.poison_food_location = (0, 0)
        self.randomize_food()

        # Poison food timing setter
        self.poison_appeared_time = time.time()
        self.poison_visible = False

    def randomize_food(self):
        self.food_location = (random.randint(100, 1000), random.randint(100, 600))
        self.bonus_food_location = (random.randint(100, 1000), random.randint(100, 600))
        self.poison_food_location = (random.randint(100, 1000), random.randint(100, 600))
        self.poison_appeared_time = time.time()
        self.poison_visible = True

    def update(self, frame, hand_pos):
        if self.game_over:
            cvzone.putTextRect(frame, "Game Over", (300, 350), scale=8, thickness=4, colorT=(255, 255, 255), colorR=(0, 0, 255), offset=20)
            cvzone.putTextRect(frame, f'Score: {self.score}', (400, 500), scale=6, thickness=5, colorT=(255, 255, 255), colorR=(0, 0, 255), offset=20)
        else:
            prev_x, prev_y = self.head_previous
            curr_x, curr_y = hand_pos
            self.points.append((curr_x, curr_y))
            dist = math.hypot(curr_x - prev_x, curr_y - prev_y)
            self.lengths.append(dist)
            self.current_length += dist
            self.head_previous = curr_x, curr_y

            # Reducing length if exceeded
            while self.current_length > self.total_allowed_length:
                self.current_length -= self.lengths.pop(0)
                self.points.pop(0)

            # Checking boundary collision
            if curr_x <= 0 or curr_x >= WINDOW_WIDTH or curr_y <= 0 or curr_y >= WINDOW_HEIGHT:
                self.game_over = True
                self.reset_game()

            # Checking if snake eats food
            food_x, food_y = self.food_location
            if (food_x - self.food_width // 2 < curr_x < food_x + self.food_width // 2 and
                    food_y - self.food_height // 2 < curr_y < food_y + self.food_height // 2):
                self.randomize_food()
                self.total_allowed_length += 50
                self.score += 1
                pygame.mixer.Sound.play(food_eat_sound)

            # Checking if snake eats bonus food
            bonus_x, bonus_y = self.bonus_food_location
            if (bonus_x - self.bonus_food_width // 2 < curr_x < bonus_x + self.bonus_food_width // 2 and
                    bonus_y - self.bonus_food_height // 2 < curr_y < bonus_y + self.bonus_food_height // 2):
                self.randomize_food()
                self.total_allowed_length += 100
                self.score += 2
                pygame.mixer.Sound.play(food_eat_sound)

            # Checking if snake eats poison food
            poison_x, poison_y = self.poison_food_location
            if self.poison_visible and (poison_x - self.poison_food_width // 2 < curr_x < poison_x + self.poison_food_width // 2 and
                                        poison_y - self.poison_food_height // 2 < curr_y < poison_y + self.poison_food_height // 2):
                self.poison_visible = False
                self.score -= 2
                pygame.mixer.Sound.play(poison_eat_sound)

            # Hiding poison food after 5 seconds
            if self.poison_visible and time.time() - self.poison_appeared_time > 5:
                self.poison_visible = False

            # Drawing snake
            for i in range(1, len(self.points)):
                cv2.line(frame, self.points[i - 1], self.points[i], (0, 0, 255), 15)
            if self.points:
                cv2.circle(frame, self.points[-1], 20, (200, 0, 200), cv2.FILLED)

            # Drawing foods
            frame = cvzone.overlayPNG(frame, self.food_img, (food_x - self.food_width // 2, food_y - self.food_height // 2))
            frame = cvzone.overlayPNG(frame, self.bonus_food_img, (bonus_x - self.bonus_food_width // 2, bonus_y - self.bonus_food_height // 2))
            if self.poison_visible:
                frame = cvzone.overlayPNG(frame, self.poison_food_img, (poison_x - self.poison_food_width // 2, poison_y - self.poison_food_height // 2))

            # Showing score
            cvzone.putTextRect(frame, f'Score: {self.score}', (50, 80), scale=3, thickness=3, offset=10)
        return frame

    def reset_game(self):
        self.points.clear()
        self.lengths.clear()
        self.current_length = 0
        self.total_allowed_length = 150
        self.head_previous = (0, 0)
        self.score = 0
        self.game_over = False
        self.randomize_food()

def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, WINDOW_WIDTH)
    cap.set(4, WINDOW_HEIGHT)
    game = SnakeGame(r"normal.png", r"bonus.png", r"poison.png")
    while True:
        success, img = cap.read()
        if not success:
            break
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False)
        if hands:
            hand_pos = hands[0]['lmList'][8][:2]
            img = game.update(img, hand_pos)
        cv2.imshow("Snake Game", img)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
