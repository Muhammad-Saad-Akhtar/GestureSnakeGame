import cvzone
import cv2
import numpy as np
import math
import random
from cvzone.HandTrackingModule import HandDetector

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

# Initialize Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

class SnakeGame:
    def __init__(self, food_path):
        self.points = []  # Snake body points
        self.lengths = []  # Distances between points
        self.current_length = 0  # Total snake length
        self.total_allowed_length = 150  # Maximum allowed length
        self.head_previous = (0, 0)

        # Food setup
        self.food_img = cv2.imread(food_path, cv2.IMREAD_UNCHANGED)
        self.food_height, self.food_width, _ = self.food_img.shape
        self.food_location = (0, 0)
        self.randomize_food()
        
        self.score = 0
        self.game_over = False

    def randomize_food(self):
        # Ensure food is in a new random position
        self.food_location = random.randint(100, 1000), random.randint(100, 600)

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

            # Reduce length if exceeded
            if self.current_length > self.total_allowed_length:
                while self.current_length > self.total_allowed_length:
                    self.current_length -= self.lengths.pop(0)
                    self.points.pop(0)
            
            # Check if snake eats food
            food_x, food_y = self.food_location
            if (food_x - self.food_width // 2 < curr_x < food_x + self.food_width // 2 and
                    food_y - self.food_height // 2 < curr_y < food_y + self.food_height // 2):
                self.randomize_food()  # Randomize the food position
                self.total_allowed_length += 50  # Increase snake's allowed length
                self.score += 1  # Increase score

            # Draw snake with red color (changed from green to red)
            for i in range(1, len(self.points)):
                cv2.line(frame, self.points[i - 1], self.points[i], (0, 0, 255), 15)  # Red color (BGR)

            # Only draw the circle if there are points in the list
            if self.points:
                cv2.circle(frame, self.points[-1], 20, (200, 0, 200), cv2.FILLED)

            # Collision check (snake collides with itself)
            poly_points = np.array(self.points[:-2], np.int32).reshape((-1, 1, 2))
            min_dist = cv2.pointPolygonTest(poly_points, (curr_x, curr_y), True)
            if -1 <= min_dist <= 1:
                self.game_over = True
                self.reset_game()

            # Draw food
            frame = cvzone.overlayPNG(frame, self.food_img, (food_x - self.food_width // 2, food_y - self.food_height // 2))
            
            # Show score
            cvzone.putTextRect(frame, f'Score: {self.score}', (50, 80), scale=3, thickness=3, offset=10)
        
        return frame
    
    def reset_game(self):
        # Reset game state
        self.points.clear()
        self.lengths.clear()
        self.current_length = 0
        self.total_allowed_length = 150
        self.head_previous = (0, 0)
        self.score = 0
        self.game_over = False

        # Add an initial point to avoid empty list issue
        self.points.append(self.head_previous)

        # Reset food location
        self.randomize_food()


def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, WINDOW_WIDTH)
    cap.set(4, WINDOW_HEIGHT)
    
    game = SnakeGame(r"C:\Users\HP\Desktop\Snake_CV\normal.png")
    
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
        key = cv2.waitKey(1)
        if key == ord('r'):
            game.reset_game()
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
