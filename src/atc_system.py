import tkinter as tk
import random
from PIL import Image, ImageTk
import json
from planes import Plane

with open('../data/flight_data.json', 'r') as file:
    flight_data = json.load(file)
    arrivals = flight_data['arrivals']
    departures = flight_data['departures']


class ATCSimulator:
    def __init__(self, root, canvas, finder1_x, finder1_y, airport_x, airport_y):
        self.root = root
        self.canvas = canvas
        self.finder1_x, self.finder1_y = finder1_x, finder1_y
        self.airport_x, self.airport_y = airport_x, airport_y
        # self.finder = canvas.create_rectangle(finder1_x - 5, finder1_y - 5, finder1_x + 5, finder1_y + 5,
        #                                       fill="white")  # Finder rectangle
        # self.airport = canvas.create_rectangle(airport_x - 5, airport_y - 5, airport_x + 5, airport_y + 5,
        #                                        fill="white")  # Airport rectangle
        self.planes = []

    def create_plane(self):
        this_journey = random.choice(arrivals)
        aircraft = this_journey['aircraft']
        flight_number = this_journey['flight_number']
        origin = this_journey['departure_airport']
        destination = this_journey['arrival_airport']
        plane = Plane(self.canvas, self.finder1_x, self.finder1_y, self.airport_x, self.airport_y,
                      aircraft, flight_number, origin, destination)
        self.planes.append(plane)

    def update_planes(self):
        for plane in self.planes:
            plane.move()
        self.planes = [plane for plane in self.planes if (
            # Remove planes that have reached the finder location
            plane.x != self.finder1_x or plane.y != self.finder1_y)]
        self.planes = [plane for plane in self.planes if (
            plane.x != self.airport_x or plane.y != self.airport_y)]  # Remove planes that have reached the airport
        self.root.after(100, self.update_planes)


def main():
    root = tk.Tk()
    root.title("ATC Simulator")

    # Load the background image
    background_image = Image.open("../assets/ORK_airport.png")
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
