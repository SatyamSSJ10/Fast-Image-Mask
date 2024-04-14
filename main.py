import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw

INPUT_PATH = r"F:\TODO" #Where Images are located
PROCESSED_PATH = r"F:\PROCESSED" #Where to Save

# Function to resize image to fit the screen height and maintain aspect ratio
def resize_image(img_path):
    img = Image.open(img_path)
    width, height = img.size
    max_height = 1080

    if height > max_height:
        ratio = max_height / height
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
    
    return img

# Function to handle saving processed image
def save_processed_image(img_path, rect_coords):
    # Create a copy of the original image
    processed_img = Image.open(img_path)

    # Convert rectangle coordinates to original image's coordinate system
    width, height = processed_img.size
    rect_coords = [
        (int(coord[0] * width / canvas.winfo_width()), int(coord[1] * height / canvas.winfo_height()))
        for coord in rect_coords
    ]

    # Fill rectangle coordinates with white pixels
    draw = ImageDraw.Draw(processed_img)
    draw.rectangle(rect_coords, fill='white')

    # Save the processed image
    processed_img.save(os.path.join(PROCESSED_PATH, os.path.basename(img_path)))

# Function to draw rectangle on canvas
def draw_rectangle(event):
    global rect_start_x, rect_start_y, rect_coords

    # Update starting coordinates of the rectangle
    rect_start_x, rect_start_y = event.x, event.y

# Function to update rectangle coordinates and draw rectangle on canvas
def update_rectangle(event):
    global rect_end_x, rect_end_y, rect_coords, canvas, rect_id

    # Update ending coordinates of the rectangle
    rect_end_x, rect_end_y = event.x, event.y

    # Clear existing rectangle
    canvas.delete(rect_id)

    # Draw new rectangle
    rect_id = canvas.create_rectangle(rect_start_x, rect_start_y, rect_end_x, rect_end_y, outline='red')

    # Update rectangle coordinates
    rect_coords = [(rect_start_x, rect_start_y), (rect_end_x, rect_end_y)]

# Function to handle key press events
def key_press(event):
    global img_index, images

    # Check if left arrow key is pressed
    if event.keysym == 'Left':
        img_index = (img_index - 1) % len(images)
        display_image(images[img_index])

    # Check if right arrow key is pressed
    elif event.keysym == 'Right':
        img_index = (img_index + 1) % len(images)
        display_image(images[img_index])

    # Check if Tab key is pressed
    elif event.keysym == 'Tab':
        save_processed_image(images[img_index], rect_coords)

# Function to display image on canvas
def display_image(img_path):
    global img, rect_id, canvas

    # Resize image to fit screen height
    img = ImageTk.PhotoImage(resize_image(img_path))

    # Update canvas with new image
    canvas.config(width=img.width(), height=img.height())
    canvas.create_image(0, 0, anchor=tk.NW, image=img)

    # Clear existing rectangle
    canvas.delete(rect_id)

# Initialize tkinter window
root = tk.Tk()
root.title("Image Processor")

# Create canvas for displaying images
canvas = tk.Canvas(root)
canvas.pack(fill=tk.BOTH, expand=True)

# Initialize rectangle variables
rect_start_x, rect_start_y = 0, 0
rect_end_x, rect_end_y = 0, 0
rect_coords = [(0, 0), (0, 0)]
rect_id = None

# Bind mouse events to canvas
canvas.bind("<ButtonPress-1>", draw_rectangle)
canvas.bind("<B1-Motion>", update_rectangle)

# Bind key press events to root window
root.bind("<KeyPress>", key_press)


# Create processed directory if it doesn't exist
if not os.path.exists(PROCESSED_PATH):
    os.makedirs(PROCESSED_PATH)

# Get images from input directory
images = [os.path.join(INPUT_PATH, file) for file in os.listdir(INPUT_PATH) if file.endswith(('jpg', 'jpeg', 'png'))]
img_index = 0

# Display first image
display_image(images[img_index])

# Start tkinter event loop
root.mainloop()
