import json
import random
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

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
        self.planes = []

        # Stop/Start Simulation
        self.simulation_running = False

        # Label for incoming and outgoing flights
        above_text = "Incoming Flights"
        incoming_flights_label = ttk.Label(canvas, text=above_text, font=("TkDefaultFont", 20))
        incoming_flights_label.place(x=20, y=12, anchor=tk.NW)

        above_outgoing_text = "Departing Flights"
        outgoing_flights_label = ttk.Label(canvas, text=above_outgoing_text, font=("TkDefaultFont", 20))
        outgoing_flights_label.place(x=20, y=235, anchor=tk.NW)

        self.last_click_time = None  # Click tracker for pausing and resuming the simulation

        # Incoming and outgoing box sizes
        listbox_height = 10
        listbox_width = 20

        style = ttk.Style()
        style.configure("TListbox", font=("TkDefaultFont", 12))

        # Incoming box decoration
        self.incoming_flights_listbox = tk.Listbox(width=listbox_width, height=listbox_height,
                                                   selectbackground="#a6a6a6",
                                                   selectforeground="black", activestyle='none')
        self.incoming_flights_listbox.pack(side=tk.LEFT, anchor=tk.NW)
        self.incoming_flights_listbox.place(x=20, y=50)  # Adjust the position as needed

        # Outgoing box decoration
        self.outgoing_flights_listbox = tk.Listbox(width=listbox_width, height=listbox_height,
                                                   selectbackground="#a6a6a6",
                                                   selectforeground="black", activestyle='none')
        self.outgoing_flights_listbox.pack(side=tk.LEFT, anchor=tk.NW)
        self.outgoing_flights_listbox.place(x=20, y=273)

        # Flight details label
        self.flight_details_label = ttk.Label(self.canvas, text="", font=("TkDefaultFont", 16))
        self.flight_details_label.pack(side=tk.LEFT, anchor=tk.NW)
        self.flight_details_label.place(x=200, y=300)

        # Control panel
        self.control_panel = ttk.Frame(root)

        # Control panel
        self.flight_details_label.place(x=1525, y=70)

        # Use show_flight_details function to display flight details in boxes
        self.incoming_flights_listbox.bind("<<ListboxSelect>>", lambda event,
                                                                       flight_listbox=self.incoming_flights_listbox: self.show_flight_details(
            event, flight_listbox))
        self.outgoing_flights_listbox.bind("<<ListboxSelect>>", lambda event,
                                                                       flight_listbox=self.outgoing_flights_listbox: self.show_flight_details(
            event, flight_listbox))

    def show_flight_details(self, event, flight_listbox):
        selected_flight_index = flight_listbox.curselection()
        if selected_flight_index:
            selected_flight_index = int(selected_flight_index[0])
            selected_flight = flight_listbox.get(selected_flight_index)

            # Extract flight number and origin from the selected flight
            flight_info = selected_flight.split()
            flight_number = flight_info[1]
            origin = flight_info[2][1:-1]  # Remove parentheses

            # Find the corresponding plane in the planes list
            for plane in self.planes:
                if plane.flight_number == flight_number and plane.origin == origin:
                    # Display additional details in the flight details label
                    details_text = "Selected Flight Details:\n"
                    details_text += f"Flight Number: {plane.flight_number}\n"
                    details_text += f"Destination: {plane.destination}\n"
                    details_text += f"Origin: {plane.origin}\n"
                    # Remove the line below as "airline" is not an attribute of Plane
                    # details_text += f"Airline: {plane.airline}\n"
                    details_text += f"Aircraft: {plane.aircraft}"

                    # Configure label with bold title and regular text, left alignment
                    self.flight_details_label.config(text=details_text, font=("TkDefaultFont", 15, "bold"), anchor="w")

                    # Auto hide the flight details label after 10 seconds
                    self.last_click_time = self.root.after(10000, self.hide_flight_details)

    def hide_flight_details(self):
        # Reset the flight details label
        self.flight_details_label.config(text="")

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

        # Remove the plane from the listbox after 15 seconds (enough time for plant to go off screen)
        self.root.after(15000, lambda: self.remove_outgoing_plane_from_listbox(out_plane))

    def remove_plane_from_listbox(self, plane):
        # Remove the plane from the list box
        flight_info = f"Flight {plane.flight_number} ({plane.origin})"
        list_items = self.incoming_flights_listbox.get(0, tk.END)
        if flight_info in list_items:
            index = list_items.index(flight_info)
            self.incoming_flights_listbox.delete(index)

    def remove_outgoing_plane_from_listbox(self, plane):
        # Remove the plane from the outgoing planes list box after a certain time period (e.g., 15 seconds)
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
        if self.simulation_running:
            for plane in self.planes:
                plane.move()
            self.planes = [plane for plane in self.planes if (
                # Remove planes that have reached the finder location
                    plane.x != self.finder1_x or plane.y != self.finder1_y)]
            self.planes = [plane for plane in self.planes if (
                    plane.x != self.airport_x or plane.y != self.airport_y)]  # Remove planes that have reached the
            # airport
            self.root.after(100, self.update_planes)

    def start_simulation(self):
        if not self.simulation_running:
            self.simulation_running = True
            print("Simulation started")
            self.root.after(100, self.update_planes)  # Start updating planes after a short delay

    def stop_simulation(self):
        print("Simulation stopped")
        self.simulation_running = False


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
    canvas.image = background_photo

    # Create the ATC simulator
    finder1_x, finder1_y = 760, 250
    finder2_x, finder2_y = 700, 100
    airport_x, airport_y = 890, 600
    atc_simulator = ATCSimulator(root, canvas, finder1_x, finder1_y, finder2_x, finder2_y, airport_x, airport_y)

    def create_new_plane():
        """Create a new plane and schedule the next plane creation"""
        atc_simulator.create_plane()
        root.after(random.randint(15000, 30000), create_new_plane)

    def create_outgoing_plane():
        """Create a new outgoing plane and schedule the next plane creation"""
        atc_simulator.create_outgoing_plane()
        root.after(random.randint(35000, 50000), create_outgoing_plane)

    # Control panel
    control_panel = tk.Frame(root)
    control_panel.pack(pady=10)  # Padding

    start_button = tk.Button(control_panel, text="Start Simulation", command=atc_simulator.start_simulation)
    start_button.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.CENTER)

    stop_button = tk.Button(control_panel, text="Stop Simulation", command=atc_simulator.stop_simulation)
    stop_button.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.CENTER)

    # Place the control panel on the canvas
    control_panel.place(x=1525, y=15)

    create_new_plane()
    create_outgoing_plane()
    atc_simulator.update_planes()

    root.mainloop()


if __name__ == "__main__":
    main()
