import tkinter as tk
from itertools import count
from PIL import Image, ImageTk

class AnimatedGif:
    def __init__(self, root, gif_path, x=0, y=0):
        self.root = root
        self.gif_path = gif_path
        self.label = tk.Label(root)
        self.label.place(x=x, y=y)
        
        image = Image.open(gif_path)
        self.frames = []

        try:
            for i in count(0):
                self.frames.append(ImageTk.PhotoImage(image.copy()))
                image.seek(i + 1)
        except EOFError:
            pass  

        self.delay = image.info.get('duration', 100)  

        self.frame_index = 0
        self.update_frame()

    def update_frame(self):
        self.label.configure(image=self.frames[self.frame_index])
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.root.after(self.delay, self.update_frame)