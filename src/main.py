import random
import tkinter as tk
from PIL import Image, ImageTk
from atc_system import ATCSimulator


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

    def create_new_plane():  # Schedule a new plane to be created
        # Stops generating when simulation is paused
        if atc_simulator.simulation_running:
            atc_simulator.create_plane()
            root.after(random.randint(15000, 30000), create_new_plane)

    def create_outgoing_plane():  # Schedule a new outgoing plane to be created
        # Stops generating when simulation is paused
        if atc_simulator.simulation_running:
            atc_simulator.create_outgoing_plane()
            root.after(random.randint(35000, 50000), create_outgoing_plane)

    # Create the control panel
    control_panel = tk.Frame(root)
    control_panel.pack(pady=10)
    start_button = tk.Button(control_panel, text="Resume", command=atc_simulator.start_simulation)
    start_button.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.CENTER)
    stop_button = tk.Button(control_panel, text="Stop", command=atc_simulator.stop_simulation)
    stop_button.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.CENTER)
    control_panel.place(x=20, y=450)  # Control panel position

    create_new_plane()
    create_outgoing_plane()
    atc_simulator.update_planes()
    atc_simulator.refresh_outgoing_flights_list()
    root.mainloop()


if __name__ == "__main__":
    main()
