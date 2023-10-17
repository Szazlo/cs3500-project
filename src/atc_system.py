import tkinter as tk
import random
from PIL import Image, ImageTk
import json
from planes import Plane, OutgoingPlane

with open('../data/flight_data.json', 'r') as file:
    flight_data = json.load(file)
    arrivals = flight_data['arrivals']
    departures = flight_data['departures']


class ATCSimulator:
    def __init__(self, root, canvas, finder1_x, finder1_y, finder2_x, finder2_y, airport_x, airport_y):
        self.root = root
        self.canvas = canvas
        self.finder1_x, self.finder1_y = finder1_x, finder1_y
        self.finder2_x, self.finder2_y = finder2_x, finder2_y
        self.airport_x, self.airport_y = airport_x, airport_y
        # self.finder = canvas.create_rectangle(finder1_x - 5, finder1_y - 5, finder1_x + 5, finder1_y + 5,
        #                                       fill="white")  # Finder rectangle
        # self.airport = canvas.create_rectangle(airport_x - 5, airport_y - 5, airport_x + 5, airport_y + 5,
        #                                        fill="white")  # Airport rectangle
        self.planes = []

        # Add a label for text above the Listbox
        above_text = "Incoming Flights"
        canvas.create_text(20, 12, text=above_text, font=("TkDefaultFont", 20), anchor=tk.NW)

        listbox_height = 10
        listbox_width = 16
        self.incoming_flights_listbox = tk.Listbox(width=listbox_width, height=listbox_height)
        self.incoming_flights_listbox.pack(side=tk.LEFT, anchor=tk.NW)
        self.incoming_flights_listbox.place(x=20, y=40)  # Adjust the position as needed

        above_outgoing_text = "Departing Flights"
        canvas.create_text(20, 235, text=above_outgoing_text, font=("TkDefaultFont", 20), anchor=tk.NW)

        self.outgoing_flights_listbox = tk.Listbox(width=listbox_width, height=listbox_height)
        self.outgoing_flights_listbox.pack(side=tk.LEFT, anchor=tk.NW)
        self.outgoing_flights_listbox.place(x=20, y=260)

    def create_plane(self):
        this_journey = random.choice(arrivals)
        aircraft = this_journey['aircraft']
        flight_number = this_journey['flight_number']
        origin = this_journey['departure_airport']
        destination = this_journey['arrival_airport']
        # Inside the ATCSimulator class, where you create a new plane
        plane = Plane(self.canvas, self.finder1_x, self.finder1_y, self.airport_x, self.airport_y,
                      aircraft, flight_number, origin, destination, self)

        self.planes.append(plane)
        # Add the plane to the listbox
        self.update_incoming_flights_list(flight_number, origin)

    def create_outgoing_plane(self):
        this_journey = random.choice(departures)
        aircraft = this_journey['aircraft']
        flight_number = this_journey['flight_number']
        origin = this_journey['departure_airport']
        destination = this_journey['arrival_airport']
        # Inside the ATCSimulator class, where you create a new plane
        out_plane = OutgoingPlane(self.canvas, self.finder1_x, self.finder1_y, self.airport_x, self.airport_y,
                                  aircraft, flight_number, origin, destination, self)

        self.planes.append(out_plane)
        # Add the plane to the listbox
        self.update_outgoing_flights_list(flight_number, destination)

        # Remove the plane from the listbox after 20 seconds
        self.root.after(30000, lambda: self.remove_outgoing_plane_from_listbox(out_plane))

    def remove_plane_from_listbox(self, plane):
        # Remove the plane from the list box
        flight_info = f"Flight {plane.flight_number} ({plane.origin})"
        list_items = self.incoming_flights_listbox.get(0, tk.END)
        if flight_info in list_items:
            index = list_items.index(flight_info)
            self.incoming_flights_listbox.delete(index)

    def remove_outgoing_plane_from_listbox(self, plane):
        # Remove the plane from the outgoing planes list box after a certain time period (e.g., 20 seconds)
        flight_info = f"Flight {plane.flight_number} ({plane.destination})"
        list_items = self.outgoing_flights_listbox.get(0, tk.END)
        if flight_info in list_items:
            index = list_items.index(flight_info)
            self.outgoing_flights_listbox.delete(index)

    def update_incoming_flights_list(self, flight_number, origin):
        self.incoming_flights_listbox.insert(tk.END, f"Flight {flight_number} ({origin})")

    def update_outgoing_flights_list(self, flight_number, destination):
        self.outgoing_flights_listbox.insert(tk.END, f"Flight {flight_number} ({destination})")

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
    finder2_x, finder2_y = 700, 100
    airport_x, airport_y = 890, 600
    atc_simulator = ATCSimulator(root, canvas, finder1_x, finder1_y, finder2_x, finder2_y, airport_x, airport_y)

    def create_new_plane():
        atc_simulator.create_plane()
        root.after(random.randint(25000, 40000), create_new_plane)

    def create_outgoing_plane():
        atc_simulator.create_outgoing_plane()
        root.after(random.randint(30000, 50000), create_outgoing_plane)

    create_new_plane()
    create_outgoing_plane()
    atc_simulator.update_planes()

    root.mainloop()


if __name__ == "__main__":
    main()