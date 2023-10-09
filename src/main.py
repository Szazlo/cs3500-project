import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk

# Create a function to toggle the sidebar visibility
def toggle_sidebar():
    if sidebar_listbox.winfo_viewable():
        sidebar_listbox.pack_forget()
    else:
        sidebar_listbox.pack(side=tk.LEFT, fill=tk.Y)

# Create the main window
root = tk.Tk()
root.title("ATC")
root.geometry("800x600")

background_image = Image.open("../assets/map.png")
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

toggle_button = ttk.Combobox(root, values=["Toggle Sidebar"])
toggle_button.place(x=10, y=10)
toggle_button.set("Toggle Sidebar")
toggle_button.bind("<<ComboboxSelected>>", lambda event: toggle_sidebar())

sidebar_listbox = tk.Listbox(root)
sidebar_listbox.pack_forget()
for i in range(10):
    sidebar_listbox.insert(tk.END, f"Item {i+1}")

root.mainloop()
