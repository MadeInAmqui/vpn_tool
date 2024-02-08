import tkinter as tk
from PIL import Image, ImageTk

def make_window(frame, image, resize):
    image = Image.open(image)
    image_resized = image.resize(resize)
    back_image = ImageTk.PhotoImage(image_resized)

    logo_widget = tk.Label(frame, image=back_image)
    logo_widget.image = back_image
    logo_widget.grid(sticky= "ew")