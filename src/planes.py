import math
import random
import tkinter as tk


class Plane:
    def __init__(self, canvas, finder1_x, finder1_y, airport_x, airport_y, aircraft, flight_number, origin,
                 destination, atc_simulator):
        self.canvas = canvas
        self.finder1_x, self.finder1_y = finder1_x, finder1_y  # Catcher coordinates to slow down the plane
        self.airport_x, self.airport_y = airport_x, airport_y  # Airport coordinates to land the plane
        self.aircraft = aircraft
        self.flight_number = flight_number
        self.origin = origin
        self.destination = destination
        self.atc_simulator = atc_simulator

        # Spawn Positions
        initial_positions = [
            (random.randint(-self.canvas.winfo_screenwidth(), -20),
             random.randint(-self.canvas.winfo_screenheight(), self.canvas.winfo_screenheight() + 20)),
            (random.randint(self.canvas.winfo_screenwidth() + 20, self.canvas.winfo_screenwidth() * 2),
             random.randint(-self.canvas.winfo_screenheight(), self.canvas.winfo_screenheight() + 20))
        ]

        self.x, self.y = random.choice(initial_positions)
        self.direction = random.uniform(0, 2 * math.pi)  # Random direction in radians
        self.speed = random.uniform(5, 6)  # Random speed
        self.dot = canvas.create_oval(self.x, self.y, self.x + 10, self.y + 10, fill="yellow")
        self.label = canvas.create_text(self.x + 15, self.y, anchor=tk.W,
                                        text=f"Flight {self.flight_number}\n{self.aircraft}\n{self.origin} to {self.destination}")
        self.has_reached_finder = False
        self.has_reached_airport = False
        self.acceleration_rate = 0.25
        self.has_disappeared = False
        self.status = "Delayed" if random.random() < 0.2 else "On time"

    def move(self):
        if self.has_reached_airport and not self.has_disappeared:  # If the plane has reached the airport and still in
            # list; remove
            self.canvas.delete(self.dot)
            self.canvas.delete(self.label)
            self.has_disappeared = True
            # Call the method to remove the plane from the listbox
            self.atc_simulator.remove_plane_from_listbox(self)
        if not self.has_reached_finder:  # If the plane has not reached the finder, set the destination to the finder
            destination = (self.finder1_x, self.finder1_y)
        elif not self.has_reached_airport:  # If the plane has reached the finder, set the destination to the airport
            destination = (self.airport_x, self.airport_y)
        else:
            self.canvas.delete(self.dot)
            self.canvas.delete(self.label)
            return

        if math.dist((self.x, self.y), destination) > 5:  # If the plane has not reached the destination
            # Calculate trajectory to destination
            angle_to_destination = math.atan2(destination[1] - self.y, destination[0] - self.x)
            dx = self.speed * math.cos(angle_to_destination)
            dy = self.speed * math.sin(angle_to_destination)
            self.canvas.move(self.dot, dx, dy)
            self.canvas.move(self.label, dx, dy)
            self.x += dx
            self.y += dy
            if self.has_reached_finder:
                # Gradually slow down the plane when it reaches the finder, to reach landing speed
                if self.speed >= 2:
                    self.acceleration_rate = 0.05
                else:
                    self.acceleration_rate = 0.005
                if self.speed <= 0.8:
                    self.acceleration_rate = 0
                self.speed -= self.acceleration_rate
                if self.canvas.coords(self.dot)[2] - self.canvas.coords(self.dot)[0] > 7:
                    self.canvas.coords(self.dot, self.canvas.coords(self.dot)[0] + 0.1,
                                       self.canvas.coords(self.dot)[1] + 0.1, self.canvas.coords(self.dot)[2] - 0.1,
                                       self.canvas.coords(self.dot)[3] - 0.1)
        else:  # set plane status positions
            if not self.has_reached_finder:
                self.status = "Landing"
                self.has_reached_finder = True
            elif not self.has_reached_airport:
                self.status = "Taxiing"
                self.has_reached_airport = True


class OutgoingPlane:
    def __init__(self, canvas, finder1_x, finder1_y, airport_x, airport_y, aircraft, flight_number, origin,
                 destination, atc_simulator):
        self.canvas = canvas
        self.finder1_x, self.finder1_y = finder1_x, finder1_y
        self.airport_x, self.airport_y = airport_x, airport_y
        self.aircraft = aircraft
        self.flight_number = flight_number
        self.origin = origin
        self.destination = destination
        self.atc_simulator = atc_simulator

        initial_positions = [airport_x - 55, airport_y - 150]

        self.x, self.y = initial_positions
        self.direction = random.uniform(0, 2 * math.pi)  # Random direction in radians
        self.speed = 0  # Initial speed set to 0
        self.max_speed = random.uniform(3, 5)
        self.dot = None
        self.label = None
        self.has_reached_finder = False
        self.has_reached_airport = False
        self.acceleration_rate = 0.25
        self.has_disappeared = False
        self.approved = False
        self.delayed = 0
        self.status = "Taxiing"

    def taxi(self):
        self.dot = self.canvas.create_oval(self.x, self.y, self.x + 10, self.y + 10, fill="yellow")
        self.label = self.canvas.create_text(self.x + 15, self.y, anchor=tk.W,
                                        text=f"Flight {self.flight_number}\n{self.aircraft}\n{self.origin} to {self.destination}")
        self.status = "Taking off"
    def move(self):
        if self.approved:
            destination = (1090, 1200)  # Set the destination to the finder location

            # Calculate the angle to the destination
            angle_to_destination = math.atan2(destination[1] - self.y, destination[0] - self.x)

            # Accelerate the plane until it reaches the maximum speed
            if self.speed < self.max_speed:
                self.speed += self.acceleration_rate

            dx = self.speed * math.cos(angle_to_destination)
            dy = self.speed * math.sin(angle_to_destination)
            self.canvas.move(self.dot, dx, dy)
            self.canvas.move(self.label, dx, dy)
            self.x += dx
            self.y += dy
