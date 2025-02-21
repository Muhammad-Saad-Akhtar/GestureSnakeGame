Hand-Tracking Snake Game


Overview:
This Snake game uses Computer Vision to track hand movements instead of traditional keyboard controls. The game detects your index finger position using OpenCV and MediaPipe and moves the snake accordingly.

Features:
- Real-time hand tracking for intuitive control.
- Dynamic food mechanics: Normal, Bonus, and Poison food with different effects.
- Boundary detection to end the game when the snake moves out of bounds.
- Sound effects to enhance the gaming experience.

Installation:

1. Get the repository:

https://github.com/Muhammad-Saad-Akhtar/GestureSnakeGame


2. Install dependencies:

pip install opencv-python cvzone numpy pygame

3. Run the game:

python new.py


How to Play?

- Place your hand in front of the camera.  
- Move your index finger to control the snake’s direction.  
- Eat normal food (+1 point, increases length by 50).  
- Eat bonus food (+2 points, increases length by 100).  
- Avoid poison food (-2 points, no length gain).  
- The game ends if the snake moves out of bounds.  

Technologies Used:
- Python for game logic.  
- OpenCV & cvzone for hand tracking and graphics overlay.  
- Pygame for sound effects.  
- MediaPipe for hand detection.  

Future Improvements:
- Adding difficulty levels and increasing speed over time.  
- Improving UI/UX with animations and better graphics.  
- Implementing a leaderboard system for high scores.  


