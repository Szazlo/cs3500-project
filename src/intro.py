import tkinter as tk


class Page(tk.Frame):
    def __init__(self, master, text_list):
        super().__init__(master.root)
        self.text_list = text_list
        self.current_index = 0 # Index of the current text in the list

        # Set up control buttons
        self.label = tk.Label(self, text=self.text_list[self.current_index])
        self.label.pack(pady=20)

        self.bottom_label = tk.Label(self, text="Made by: Team 20 ")
        self.bottom_label.pack(side="bottom", pady=20)

        self.prev_button = tk.Button(self, text="Previous", command=self.show_previous_text)
        self.prev_button.pack(side="left", pady=10, padx=10)

        self.next_button = tk.Button(self, text="Next", command=self.show_next_text)
        self.next_button.pack(side="left", pady=10, padx=10)

        self.leave_intro_button = tk.Button(self, text="Leave Intro", command=master.on_intro_complete)
        self.leave_intro_button.pack(side="left", pady=10, padx=10)


    def show_next_text(self): # Show the next text in the list
        if self.current_index < len(self.text_list) - 1:
            self.current_index += 1
            self.label.config(text=self.text_list[self.current_index])

    def show_previous_text(self): # Show the previous text in the list
        if self.current_index > 0:
            self.current_index -= 1
            self.label.config(text=self.text_list[self.current_index])


class Intro:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ATC Simulator - Introduction")

        # Set the window size
        self.root.geometry("620x400")

        # Linekd list of text for each page of intro
        intro_text_list = [
            # Page 1
            "Welcome to the ATC Simulator!\n\nAs the staff of 'Cork Airport' have left for Christmas, you have been "
            "left in charge of the airport.\nYour job is to ensure that all planes land safely and that all "
            "passengers arrive at their destination on time.\n\nGood luck!",
            # Page 2
            'Controls:\n\nTo make you job easier, pilots have been informed of your "Skills" and planes will be '
            'automatically directed to you.\n You just need to avoid collisions. To manage aircrafts, select the route'
            'from the side panels. \nFor arriving planes you must decide to maintain or slow their speed with the button '
            'provided.\nDeparting planes are scheduled, and you will need to approve or delay their clearance, \nusing '
            'the provided buttons, to avoid a disaster.\n'
            'You can also pause the simulation at any time using the "Stop" button.\n'
            'To resume the simulation, press the "Resume" button.\n',
            # Page 3
            "Scoring:\n\nYou will be scored on how many planes you land.\n"
            "You will also be scored on how many planes you allow to take off, and whether they were on time.\n"
            "Delaying/slowing an arrival plane will slow it by 38 Knts and will cost you 5 points each time.\n"
            "Delaying a departing plane can be done twice for +15s; for first you will earn 1 point on takeoff.\n"
            "The second time will deduct 10 points. Departures will cancel on 3rd delay attempt or when timer hits 0.\n"
            "Canceling a departing plane will deduct 15 points.\n"
            "Scores and Penalties as follows:\n"
            "On time take off: +5 points\n"
            "Delaying(slowing) an arriving: -5 points\n"
            "Delaying departing: +1 point (once) | -10 (twice)\n"
            "Cancelling departure: -15 points\n"

        ]
        # Create the intro page
        self.intro_page = Page(self, intro_text_list)
        self.intro_page.pack()
    def on_intro_complete(self): # Called when the intro is complete
        self.root.destroy()  # Close the intro window
        # Will continue to run main.py

    def run(self):
        self.root.wait_window()  # Displays window and halts execution of main.py until window is closed
        print("Intro finished.")
