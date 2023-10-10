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
        initial_positions = [
            (random.randint(-self.canvas.winfo_screenwidth(), -20), random.randint(-self.canvas.winfo_screenheight(), self.canvas.winfo_screenheight() + 20)),
            (random.randint(self.canvas.winfo_screenwidth() + 20, self.canvas.winfo_screenwidth() * 2), random.randint(-self.canvas.winfo_screenheight(), self.canvas.winfo_screenheight() + 20))
        ]
        self.x, self.y = random.choice(initial_positions)
        self.direction = random.uniform(0, 2 * math.pi)  # Random direction in radians
        self.speed = random.uniform(1, 3)  # Random speed
        self.dot = canvas.create_oval(self.x, self.y, self.x+10, self.y+10, fill="yellow")
        self.label = canvas.create_text(self.x + 15, self.y, anchor=tk.W, text=f"Flight {self.flight_number} ({self.destination})")
        self.has_reached_finder = False
        self.has_reached_airport = False
        self.deceleration_rate = .999 # Deceleration rate
        

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
                self.speed = self.speed * self.deceleration_rate
            else:
                self.has_reached_airport = True

    
        else:
            self.canvas.delete(self.dot)
            self.canvas.delete(self.label)

class ATCSimulator:
    def __init__(self, root, canvas, finder1_x, finder1_y, airport_x, airport_y):
        self.root = root
        self.canvas = canvas
        self.finder1_x, self.finder1_y = finder1_x, finder1_y
        self.airport_x, self.airport_y = airport_x, airport_y
        self.finder = canvas.create_rectangle(finder1_x - 5, finder1_y - 5, finder1_x + 5, finder1_y + 5, fill="white")  # Finder rectangle
        self.airport = canvas.create_rectangle(airport_x - 5, airport_y - 5, airport_x + 5, airport_y + 5, fill="white")  # Airport rectangle
        self.planes = []
        

    def create_plane(self):
        flight_number = f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(100, 999)}"
        destinations = ["New York", "London", "Paris", "Tokyo", "Dubai", "Cork", "Dublin", "Lanzarote", "Malaga", "Lyon", "Munich", "LAX", "Faro"]
        destination = random.choice(destinations)
        plane = Plane(self.canvas, self.finder1_x, self.finder1_y, self.airport_x, self.airport_y, flight_number, destination)
        self.planes.append(plane)

    def update_planes(self):
        for plane in self.planes:
            plane.move()
        self.planes = [plane for plane in self.planes if (plane.x != self.finder1_x or plane.y != self.finder1_y)]  # Remove planes that have reached the finder location
        self.planes = [plane for plane in self.planes if (plane.x != self.airport_x or plane.y != self.airport_y)]  # Remove planes that have reached the airport
        self.root.after(100, self.update_planes)

def main():
    root = tk.Tk()
    root.title("ATC Simulator")
    

      # Load the background image
    background_image = Image.open("ORK_airport.png") 
    background_photo = ImageTk.PhotoImage(background_image)

    # Set the window size to match the image dimensions
    window_width, window_height = background_image.width, background_image.height
    root.geometry(f"{window_width}x{window_height}")

    canvas = tk.Canvas(root, width=window_width, height=window_height)
    canvas.pack()

    canvas.create_image(0, 0, anchor=tk.NW, image=background_photo)
    canvas.image = background_photo  # Keep a reference to the image object to prevent it from being garbage collected

    finder1_x, finder1_y = 760, 250
    airport_x, airport_y = 890, 600
    atc_simulator = ATCSimulator(root, canvas, finder1_x, finder1_y, airport_x, airport_y)

    def create_new_plane():
        atc_simulator.create_plane()
        root.after(random.randint(5000, 15000), create_new_plane)

    create_new_plane()
    atc_simulator.update_planes()

    root.mainloop()

if __name__ == "__main__":
    main()





