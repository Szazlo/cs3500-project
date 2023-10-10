import tkinter as tk
import math
import random
from PIL import Image, ImageTk

class Plane:
    def __init__(self, canvas, airport_x, airport_y, flight_number, destination):
        self.canvas = canvas
        self.airport_x, self.airport_y = airport_x, airport_y
        self.flight_number = flight_number
        self.destination = destination
        screen_width = self.canvas.winfo_screenwidth()
        screen_height = self.canvas.winfo_screenheight()
        initial_positions = [
            (random.randint(-screen_width, -20), random.randint(-screen_height, screen_height + 20)),
            (random.randint(screen_width + 20, screen_width * 2), random.randint(-screen_height, screen_height + 20))
        ]
        self.x, self.y = random.choice(initial_positions)
        self.direction = random.uniform(0, 2 * math.pi)  # Random direction in radians
        self.speed = random.uniform(.5, 2)  # Random speed
        self.dot = canvas.create_oval(self.x, self.y, self.x+10, self.y+10, fill="yellow")
        self.label = canvas.create_text(self.x + 15, self.y, anchor=tk.W, text=f"Flight {self.flight_number} from {self.destination}")

    def move(self):
        if math.dist((self.x, self.y), (self.airport_x, self.airport_y)) > 5:  # Check distance to airport
            angle_to_airport = math.atan2(self.airport_y - self.y, self.airport_x - self.x)
            dx = self.speed * math.cos(angle_to_airport)
            dy = self.speed * math.sin(angle_to_airport)
            self.canvas.move(self.dot, dx, dy)
            self.canvas.move(self.label, dx, dy)
            self.x += dx
            self.y += dy
        else:
            self.canvas.delete(self.dot)
            self.canvas.delete(self.label)

class ATCSimulator:
    def __init__(self, root, canvas, airport_x, airport_y):
        self.root = root
        self.canvas = canvas
        self.airport_x, self.airport_y = airport_x, airport_y
        self.airport = canvas.create_rectangle(airport_x - 20, airport_y - 20, airport_x + 20, airport_y + 20, fill="red")  # Airport rectangle
        self.planes = []

    def create_plane(self):
        flight_number = f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(100, 999)}"
        destinations = ["New York", "London", "Paris", "Tokyo", "Dubai", "Cork", "Dublin", "Lanzarote", "Malaga", "Lyon", "Munich", "LAX", "Faro"]
        destination = random.choice(destinations)
        plane = Plane(self.canvas, self.airport_x, self.airport_y, flight_number, destination)
        self.planes.append(plane)

    def update_planes(self):
        for plane in self.planes:
            plane.move()
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

    airport_x, airport_y = window_width // 2, window_height // 2
    atc_simulator = ATCSimulator(root, canvas, airport_x, airport_y)

    def create_new_plane():
        atc_simulator.create_plane()
        root.after(random.randint(10000, 15000), create_new_plane)

    create_new_plane()
    atc_simulator.update_planes()

    root.mainloop()

if __name__ == "__main__":
    main()





