from atc_system import Plane
from atc_visualiser import ATCSimulator
import random
import tkinter as tk
from PIL import Image, ImageTk

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
        root.after(random.randint(15000, 30000), create_new_plane)

    create_new_plane()
    atc_simulator.update_planes()

    root.mainloop()

if __name__ == "__main__":
    main()
