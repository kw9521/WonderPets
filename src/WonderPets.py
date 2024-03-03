import tkinter as tk
from tkinter import *
from tkinter import messagebox 
from PIL import Image, ImageTk, ImageOps
import threading
import datetime
import random
import time
import os

absolute_path = os.path.dirname(__file__)
relative_path = "\media"
path_to_imgs = absolute_path+relative_path

class pet():
    def show_welcome_message(self):
        welcome_window = tk.Tk()
        welcome_window.withdraw()
        tk.messagebox.showinfo("Welcome\n", "Welcome to Wonder Pets!!!\n\nIn this world, your pet will never leave you (unless you CTRL+C).\n\nInstead, they will bother you by making a full rotation around your screen.")
        welcome_window.destroy() 

    def select_pet(self):
        selection_window = tk.Tk()
        selection_window.title("Choose Your Pet")

        # Keep the window on top of all other applications
        selection_window.attributes('-topmost', True)

        def on_pet_selected(pet_name):
            self.imageChosen = pet_name
            selection_window.destroy()

        label = tk.Label(selection_window, text="Before we get started...Please choose your pet:")
        label.pack(pady=10)

        pets = ["Petal", "Quacker", "Berry", "Sunny", "Winston", "Cake"]
        for pet in pets:
            button = tk.Button(selection_window, text=pet, command=lambda pet_name=pet: on_pet_selected(pet_name))
            button.pack(pady=2)

        # Calculate the center position of the window
        selection_window.update_idletasks()  # Update "requested size" from geometry manager
        width = selection_window.winfo_width()
        height = selection_window.winfo_height()
        x = (selection_window.winfo_screenwidth() // 2) - (width // 2)
        y = (selection_window.winfo_screenheight() // 2) - (height // 2)
        selection_window.geometry(f'{width}x{height}+{x}+{y}')  # Set the position of the window

        selection_window.mainloop()


    def __init__(self):

        # Show welcome message and pet selection before initializing the window
        self.show_welcome_message()
        self.select_pet()

        # create a window
        self.window = tk.Tk()
        
        # Initialize direction attribute
        self.direction = 'right'  

        # placeholder image
        imgName = chr(92)+self.imageChosen+".gif"
        self.walking_right = [tk.PhotoImage(file=path_to_imgs+ imgName, format='gif -index %i' % (i)) for i in range(4)]

        # Load and flip images for leftward walking
        self.walking_left = []
        for i in range(4):
            pil_image = Image.open(f"{path_to_imgs}"+chr(92)+self.imageChosen+".gif")
            pil_image.seek(i)
            flipped_image = ImageOps.mirror(pil_image)
            tk_image = ImageTk.PhotoImage(flipped_image)
            self.walking_left.append(tk_image)

        self.frame_index = 0
        self.img = self.walking_right[self.frame_index]
        # self.timestamp = time.time()
        self.setup_window()

        # Start destressActivities in a separate thread
        threading.Thread(target=self.run_destress_activities, daemon=True).start()
        
        # run self.update() after 0ms when mainloop starts
        self.window.after(0, self.update)
        self.window.mainloop()

    def setup_window(self):

        # set focushighlight to black when the window does not have focus
        self.window.config(highlightbackground='black')

        # make window frameless
        self.window.overrideredirect(True)

        # make window draw over all others
        self.window.attributes('-topmost', True)

        # turn black into transparency
        self.window.wm_attributes('-transparentcolor', 'black')

        # create a label as a container for our image
        self.label = tk.Label(self.window, bd=0, bg='black')

        # create a window of size 128x128 pixels, at coordinates 0,0
        self.x = 0
        self.y = 0
        self.window.geometry('64x64+{x}+0'.format(x=str(self.x)))

        # add the image to our label
        self.label.configure(image=self.img)

        # give window to geometry manager (so it will appear)
        self.label.pack()

    def update(self):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Change direction based on current position and direction
        if self.direction == 'right' and self.x >= screen_width - 64:
            self.direction = 'down'
        elif self.direction == 'down' and self.y >= screen_height - 64:
            self.direction = 'left'
        elif self.direction == 'left' and self.x <= 0:
            self.direction = 'up'
        elif self.direction == 'up' and self.y <= 0:
            self.direction = 'right'

        # Move based on direction
        if self.direction == 'right':
            self.x += 1
            self.img = self.walking_right[self.frame_index]  # Use right-facing images
        elif self.direction == 'down':
            self.y += 1
            self.img = self.walking_right[self.frame_index]  # Optionally, use down-facing images if available
        elif self.direction == 'left':
            self.x -= 1
            self.img = self.walking_left[self.frame_index]  # Use left-facing (flipped) images
        elif self.direction == 'up':
            self.y -= 1
            self.img = self.walking_left[self.frame_index]  # Optionally, use up-facing images if available

        # Update the frame and image for animation
        self.frame_index = (self.frame_index + 1) % 4
        
        if self.direction in ['right', 'down']:  # Use rightward frames for right and down directions
            self.img = self.walking_right[self.frame_index]
        else:  # Use leftward (flipped) frames for left and up directions
            self.img = self.walking_left[self.frame_index]

        # Update the window geometry and image
        self.window.geometry('64x64+{x}+{y}'.format(x=self.x, y=self.y))
        self.label.configure(image=self.img)
        self.label.pack()

        # Call update after 10ms
        self.window.after(75, self.update)

    def run_destress_activities(self):
        path_to_msg = absolute_path+relative_path+"\\messages\\"
        
        short_break = ['curious.png', 'embrace-journey.png', 'great-things.png', 'porcupine.png', 'unicorn.png', 'victory.png']
        medium_break = ['enough.png', 'keep-going.png', 'hydration.png']
        long_break = ['screen-reminder.png', 'stretch.png', 'take-care.png']
        hour_count = 0
        current_time = datetime.datetime.now()

        target_time = current_time + datetime.timedelta(seconds=5)
        while True:

            while current_time < target_time:
                current_time = datetime.datetime.now()
            
            target_time = current_time + datetime.timedelta(seconds=5)
            hour_count += 1

            if hour_count % 6 == 0:
                img_path = os.path.join(path_to_msg, random.choice(long_break))
            elif hour_count % 3 == 0:
                img_path = os.path.join(path_to_msg, random.choice(medium_break))
            elif hour_count % 1 == 0:
                img_path = os.path.join(path_to_msg, random.choice(short_break))
            if os.path.exists(img_path):
                self.show_break_image(img_path)

    def show_break_image(self, img_path):
        # This method schedules show_custom_dialog to be called in the main thread
        self.window.after(0, lambda: self.show_custom_dialog(img_path))

    def show_custom_dialog(self, img_path):
        dialog = tk.Toplevel(self.window)
        dialog.title("Time for a break!")
        dialog.overrideredirect(True)  # This removes the window borders and title bar
        dialog.attributes('-topmost', True)  # Ensure the window is on top

        # Load the image using PIL and create a PhotoImage
        image = Image.open(img_path)
        photo = ImageTk.PhotoImage(image)

        # Keep a reference to the image so that it's not garbage collected
        dialog.image = photo

        # Set the window shape to match the image (with transparency)
        dialog.config(bg='#404040')
        dialog.attributes('-transparentcolor', '#404040')


        label = tk.Label(dialog, image=photo, bd=0)
        label.pack()

        # This function will be called when the image is clicked, destroying the dialog
        def on_click(event=None):
            dialog.destroy()

        # Bind the click event to the label containing the image
        label.bind("<Button-1>", on_click)

        dialog.update_idletasks()  # Update geometry now
        width = photo.width()
        height = photo.height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)

        dialog.geometry(f'{width}x{height}+{x}+{y}')
        dialog.deiconify()

        # To automatically close the dialog after 5000 ms...approx 3 secs
        # This shouldn't be a problem when we adjust the time it takes for each message to appear in the future!!!
        dialog.after(3000, dialog.destroy)  


pet()