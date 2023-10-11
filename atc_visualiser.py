from atc_system import Plane
import random

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
        self.planes = [plane for plane in self.planes if (plane.x != self.finder1_x or plane.y != self.finder1_y)] 
        self.planes = [plane for plane in self.planes if (plane.x != self.airport_x or plane.y != self.airport_y)]  # Remove planes that have reached the airport
        self.root.after(100, self.update_planes)
