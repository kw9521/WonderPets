import tkinter as tk
from PIL import Image, ImageTk, ImageOps
import time
import os

absolute_path = os.path.dirname(__file__)
relative_path = "\media"
path_to_imgs = absolute_path+relative_path

class stickFigurePet():
    def __init__(self):
        # create a window
        self.window = tk.Tk()
        
        # Initialize direction attribute
        self.direction = 'right'  

        # placeholder image
        self.walking_right = [tk.PhotoImage(file=path_to_imgs+'\walking_right.gif', format='gif -index %i' % (i)) for i in range(4)]

        # Load and flip images for leftward walking
        self.walking_left = []
        for i in range(4):
            pil_image = Image.open(f"{path_to_imgs}\walking_right.gif")
            pil_image.seek(i)
            flipped_image = ImageOps.mirror(pil_image)
            tk_image = ImageTk.PhotoImage(flipped_image)
            self.walking_left.append(tk_image)

        self.frame_index = 0
        self.img = self.walking_right[self.frame_index]

        # timestamp to check whether to advance frame
        self.timestamp = time.time()

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
        self.window.geometry('10x10+{x}+0'.format(x=str(self.x)))

        # add the image to our label
        self.label.configure(image=self.img)

        # give window to geometry manager (so it will appear)
        self.label.pack()

        # run self.update() after 0ms when mainloop starts
        self.window.after(0, self.update)
        self.window.mainloop()

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
        self.window.after(10, self.update)



stickFigurePet()
