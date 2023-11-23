import random
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from planes import Plane, OutgoingPlane

import json

with open('../data/flight_data.json', 'r') as file:  # Load Possible Flights
    flight_data = json.load(file)
    arrivals = flight_data['arrivals']
    departures = flight_data['departures']


class CustomListbox(tk.Listbox):
    """Listbox with buttons for each flight"""

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.buttons = {}  # Dictionary to store buttons for each item

    def add_button(self, item, callback):
        frame = tk.Frame(self)
        frame.pack(fill=tk.X)

        label = tk.Label(frame, text=item, anchor=tk.W)
        label.pack(side=tk.LEFT, fill=tk.X)

        button = tk.Button(frame, text="Button", command=callback)
        button.pack(side=tk.RIGHT, padx=5)

        self.buttons[item] = button


class ATCSimulator:
    """Class to manage the ATC Simulator GUI"""

    def __init__(self, root, canvas, finder1_x, finder1_y, finder2_x, finder2_y, airport_x, airport_y):
        self.root = root
        self.canvas = canvas
        self.finder1_x, self.finder1_y = finder1_x, finder1_y
        self.finder2_x, self.finder2_y = finder2_x, finder2_y
        self.airport_x, self.airport_y = airport_x, airport_y
        self.planes = []
        self.simulation_running = True
        self.last_click_time = None

        self.setup_gui()

    def setup_gui(self):
        """Setup the GUI"""
        self.setup_labels()
        self.setup_listboxes()
        self.setup_flight_details_label()
        self.setup_control_panel()
        self.setup_listbox_callbacks()
        self.setup_buttons()

    def setup_labels(self):
        """Setup the labels for the GUI"""
        above_text = "Incoming Flights"
        incoming_flights_label = ttk.Label(self.canvas, text=above_text, font=("TkDefaultFont", 20))
        incoming_flights_label.place(x=20, y=12, anchor=tk.NW)

        above_outgoing_text = "Departing Flights"
        outgoing_flights_label = ttk.Label(self.canvas, text=above_outgoing_text, font=("TkDefaultFont", 20))
        outgoing_flights_label.place(x=20, y=235, anchor=tk.NW)

    def setup_listboxes(self):
        """Setup the listboxes for the GUI,
        for listing incoming and outgoing flights"""
        listbox_height, listbox_width = 10, 30

        style = ttk.Style()
        style.configure("TListbox", font=("TkDefaultFont", 12))

        self.incoming_flights_listbox = CustomListbox(width=listbox_width, height=listbox_height,
                                                      selectbackground="#a6a6a6",
                                                      selectforeground="black", activestyle='none')
        self.incoming_flights_listbox.pack(side=tk.LEFT, anchor=tk.NW)
        self.incoming_flights_listbox.place(x=20, y=50)

        self.outgoing_flights_listbox = CustomListbox(width=listbox_width, height=listbox_height,
                                                      selectbackground="#a6a6a6",
                                                      selectforeground="black", activestyle='none')
        self.outgoing_flights_listbox.pack(side=tk.LEFT, anchor=tk.NW)
        self.outgoing_flights_listbox.place(x=20, y=273)

    def setup_flight_details_label(self):
        """Attach the label for the flight details"""
        self.flight_details_label = ttk.Label(self.canvas, text="", font=("TkDefaultFont", 16))
        self.flight_details_label.pack(side=tk.LEFT, anchor=tk.NW)
        self.flight_details_label.place(x=200, y=300)

    def setup_control_panel(self):
        """Setup the control panel for pausing and resuming the simulation"""
        control_panel = ttk.Frame(self.root)
        #   position the control panel in the top right corner, relative to the screen size
        control_panel.place(x=self.root.winfo_screenwidth() - 250, y=10)
        self.control_panel = control_panel

    def setup_listbox_callbacks(self):
        """Setup the callbacks for the listboxes"""
        self.incoming_flights_listbox.bind("<<ListboxSelect>>", lambda event,
                                                                       flight_listbox=self.incoming_flights_listbox: self.show_flight_details(
            event, flight_listbox))
        self.outgoing_flights_listbox.bind("<<ListboxSelect>>", lambda event,
                                                                       flight_listbox=self.outgoing_flights_listbox: self.show_flight_details(
            event, flight_listbox))

    def setup_buttons(self):
        """Add buttons to Out-items in the listboxes"""

        '''Print statement for debugging'''
        def button_callback():
            print("Button clicked!")

        for item in self.outgoing_flights_listbox.get(0, tk.END):
            self.outgoing_flights_listbox.add_button(item, button_callback)

    def show_flight_details(self, event, flight_listbox):
        """Show the flight details for the selected flight.
        Duration of 10 seconds.
        """
        selected_flight_index = flight_listbox.curselection()  # Get the index of the selected flight
        if selected_flight_index:
            selected_flight_index = int(selected_flight_index[0])
            selected_flight = flight_listbox.get(selected_flight_index)

            flight_info = selected_flight.split()
            flight_number, origin, destination = flight_info[1], flight_info[2][1:-1], flight_info[4][:-1]

            for plane in self.planes:  # Find the plane with the same flight number, origin and destination
                if plane.flight_number == flight_number and plane.origin == origin and plane.destination == destination:
                    details_text = f"Selected Flight Details:\nFlight Number: {plane.flight_number}\n"
                    details_text += f"Destination: {plane.destination}\nOrigin: {plane.origin}\n"
                    details_text += f"Aircraft: {plane.aircraft}"

                    self.flight_details_label.config(text=details_text, font=("TkDefaultFont", 15, "bold"), anchor="w")
                    self.last_click_time = self.root.after(10000,
                                                           self.hide_flight_details)  # Hide the flight details after 10 seconds

    def hide_flight_details(self):
        """Hide the flight details"""
        self.flight_details_label.config(text="")

    def create_plane(self):
        """Schedule a new arrival plane"""
        this_journey = random.choice(arrivals)  # Choose a random flight from the arrivals list
        aircraft, flight_number, origin, destination = this_journey['aircraft'], this_journey['flight_number'], \
            this_journey['departure_airport'], this_journey['arrival_airport']

        plane = Plane(self.canvas, self.finder1_x, self.finder1_y, self.airport_x, self.airport_y,
                      aircraft, flight_number, origin, destination, self)

        self.planes.append(plane)
        self.update_incoming_flights_list(flight_number, origin)  # Add the flight to the incoming flights listbox

    def create_outgoing_plane(self):
        """Schedule a new departure plane"""
        this_journey = random.choice(departures)  # Choose a random flight from the departures list
        aircraft, flight_number, origin, destination = this_journey['aircraft'], this_journey['flight_number'], \
            this_journey['departure_airport'], this_journey['arrival_airport']
        # Create a new outgoing plane
        out_plane = OutgoingPlane(self.canvas, self.finder1_x, self.finder1_y, self.airport_x, self.airport_y,
                                  aircraft, flight_number, origin, destination, self)

        self.planes.append(out_plane)
        self.update_outgoing_flights_list(flight_number, destination)
        # Remove the plane from the outgoing flights listbox after 15 seconds
        # (enough time for the plane to go off-screen)
        self.root.after(15000, lambda: self.remove_outgoing_plane_from_listbox(out_plane))

    def remove_plane_from_listbox(self, plane):
        """Remove the plane from the listbox"""
        flight_info = f"Flight {plane.flight_number} ({plane.origin})"
        list_items = self.incoming_flights_listbox.get(0, tk.END)
        if flight_info in list_items:
            index = list_items.index(flight_info)
            self.incoming_flights_listbox.delete(index)

    def remove_outgoing_plane_from_listbox(self, plane):
        """Remove the plane from the listbox (outgoing flights"""
        flight_info = f"Flight {plane.flight_number} ({plane.destination})"
        list_items = self.outgoing_flights_listbox.get(0, tk.END)
        if flight_info in list_items:
            index = list_items.index(flight_info)
            self.outgoing_flights_listbox.delete(index)

    # Update the listboxes for in/out flights
    def update_incoming_flights_list(self, flight_number, origin):
        self.incoming_flights_listbox.insert(tk.END, f"Flight {flight_number} ({origin})")

    def update_outgoing_flights_list(self, flight_number, destination):
        self.outgoing_flights_listbox.insert(tk.END, f"Flight {flight_number} ({destination})")

    def update_planes(self):
        """Update the positions of the planes"""
        if self.simulation_running:
            for plane in self.planes:
                plane.move()

            self.planes = [plane for plane in self.planes if (
                    plane.x != self.finder1_x or plane.y != self.finder1_y)]

            self.planes = [plane for plane in self.planes if (
                    plane.x != self.airport_x or plane.y != self.airport_y)]

            self.root.after(100, self.update_planes)  # Update the planes every 100 milliseconds
            # This should be enough to make the planes move smoothly

    def start_simulation(self):  # Start the simulation when the button is clicked
        if not self.simulation_running:
            self.simulation_running = True
            print("Simulation started")
            self.root.after(100, self.update_planes)

    def stop_simulation(self):  # Stop sim
        print("Simulation stopped")
        self.simulation_running = False


def main():
    root = tk.Tk()
    root.title("ATC Simulator")

    background_image = Image.open("../assets/ORK_airport.png")  # Load the background image
    background_photo = ImageTk.PhotoImage(background_image)
    window_width, window_height = background_image.width, background_image.height
    root.geometry(f"{window_width}x{window_height}")

    canvas = tk.Canvas(root, width=window_width, height=window_height)
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=background_photo)
    canvas.image = background_photo

    finder1_x, finder1_y = 760, 250  # Set catcher position to start landing process
    finder2_x, finder2_y = 700, 100  # Catcher for runway 2
    airport_x, airport_y = 890, 600  # Set airport position, for taxiing

    # Create the ATC Simulator
    atc_simulator = ATCSimulator(root, canvas, finder1_x, finder1_y, finder2_x, finder2_y, airport_x, airport_y)

    def create_new_plane(): # Schedule a new plane to be created
        # Stops generating when simulation is paused
        if atc_simulator.simulation_running:
            atc_simulator.create_plane()
            root.after(random.randint(15000, 30000), create_new_plane)

    def create_outgoing_plane(): # Schedule a new outgoing plane to be created
        # Stops generating when simulation is paused
        if atc_simulator.simulation_running:
            atc_simulator.create_outgoing_plane()
            root.after(random.randint(35000, 50000), create_outgoing_plane)

    control_panel = tk.Frame(root)
    control_panel.pack(pady=10)

    start_button = tk.Button(control_panel, text="Start Simulation", command=atc_simulator.start_simulation)
    start_button.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.CENTER)

    stop_button = tk.Button(control_panel, text="Stop Simulation", command=atc_simulator.stop_simulation)
    stop_button.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.CENTER)

    window_width = root.winfo_screenwidth()
    control_panel.place(x=window_width - 250, y=10)

    create_new_plane()
    create_outgoing_plane()
    atc_simulator.update_planes()

    root.mainloop()


if __name__ == "__main__":
    main()
