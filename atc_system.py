import tkinter as tk
import math
import random
from PIL import Image, ImageTk

class Plane:
    def __init__(self, canvas, finder1_x, finder1_y, airport_x, airport_y, flight_number, destination):
        self.canvas = canvas
        self.finder1_x, self.finder1_y = finder1_x, finder1_y
        self.airport_x, self.airport_y = airport_x, airport_y
        self.flight_number = flight_number
        self.destination = destination
        
        # Randomly select an edge (top, bottom, left, or right)
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        if edge == 'top':
            self.x, self.y = random.randint(0, canvas.winfo_screenwidth()), -5
        elif edge == 'bottom':
            self.x, self.y = random.randint(0, canvas.winfo_screenwidth()), canvas.winfo_screenheight() + 5
        elif edge == 'left':
            self.x, self.y = -5, random.randint(0, canvas.winfo_screenheight())
        else:
            self.x, self.y = canvas.winfo_screenwidth() + 5, random.randint(0, canvas.winfo_screenheight())
        
        self.direction = random.uniform(0, 2 * math.pi)  # Random direction in radians
        self.speed = random.uniform(1.6, 3.5)  # Random speed
        self.dot = canvas.create_oval(self.x, self.y, self.x+10, self.y+10, fill="lime")
        self.label = canvas.create_text(self.x + 15, self.y, anchor=tk.W, text=f"Flight {self.flight_number} ({self.destination})")
        self.has_reached_finder = False
        self.has_reached_airport = False
        self.deceleration_rate = 1.5  # Deceleration rate .99

    def move(self):
        if not self.has_reached_finder:
            if math.dist((self.x, self.y), (self.finder1_x, self.finder1_y)) > 5:
                angle_to_finder = math.atan2(self.finder1_y - self.y, self.finder1_x - self.x)
                dx = self.speed * math.cos(angle_to_finder)
                dy = self.speed * math.sin(angle_to_finder)
                self.canvas.move(self.dot, dx, dy)
                self.canvas.move(self.label, dx, dy)
                self.x += dx
                self.y += dy
            else:
                self.has_reached_finder = True
        elif not self.has_reached_airport:
            if math.dist((self.x, self.y), (self.airport_x, self.airport_y)) > 5:
                angle_to_airport = math.atan2(self.airport_y - self.y, self.airport_x - self.x)
                dx = self.speed * math.cos(angle_to_airport)
                dy = self.speed * math.sin(angle_to_airport)
                self.canvas.move(self.dot, dx, dy)
                self.canvas.move(self.label, dx, dy)
                self.x += dx
                self.y += dy
                self.speed = self.deceleration_rate
            else:
                self.has_reached_airport = True
        else:
            self.canvas.delete(self.dot)
            self.canvas.delete(self.label)
