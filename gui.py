import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np

# Function to exit fullscreen
def exit_fullscreen(event=None):
    root.attributes("-fullscreen", False)

# Function to encode message into an image
def encode_message():
    file_path = filedialog.askopenfilename(title="Select Image")
    if not file_path:
        return

    img = cv2.imread(file_path)
    msg = entry_message.get().strip()
    password = entry_password.get().strip()

    if not msg or not password:
        messagebox.showerror("Error", "Message and password cannot be empty!")
        return

    d = {chr(i): i for i in range(255)}
    
    n, m, z = 0, 0, 0
    for i in range(len(msg)):
        img[n, m, z] = d[msg[i]]
        n = (n + 1) % img.shape[0]
        m = (m + 1) % img.shape[1]
        z = (z + 1) % 3

    save_path = "encoded_image.png"
    cv2.imwrite(save_path, img)
    messagebox.showinfo("Success", f"Message encoded and saved as {save_path}")

# Function to decode message from an image
def decode_message():
    file_path = filedialog.askopenfilename(title="Select Image")
    if not file_path:
        return

    img = cv2.imread(file_path)
    password = entry_password_decode.get().strip()

    if not password:
        messagebox.showerror("Error", "Please enter a passcode!")
        return

    c = {i: chr(i) for i in range(255)}
    message = ""
    n, m, z = 0, 0, 0

    try:
        while True:
            message += c[img[n, m, z]]
            n = (n + 1) % img.shape[0]
            m = (m + 1) % img.shape[1]
            z = (z + 1) % 3
    except KeyError:
        pass

    messagebox.showinfo("Decoded Message", message)

# Initialize root window
root = tk.Tk()
root.title("Steganography Tool")
root.attributes("-fullscreen", True)  # Fullscreen Mode

# Load background image
bg_image = Image.open("background.jpg")  # Ensure this file exists
bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Set background image as a label (this keeps it in the back)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Notebook (Tabs)
tab_control = ttk.Notebook(root)
tab_encode = ttk.Frame(tab_control)
tab_decode = ttk.Frame(tab_control)

tab_control.add(tab_encode, text="Encode")
tab_control.add(tab_decode, text="Decode")
tab_control.pack(expand=True, fill="both", padx=100, pady=50)

# Encode Tab
ttk.Label(tab_encode, text="Enter Message:", font=("Arial", 12), background="#ffffff").pack(pady=5)
entry_message = ttk.Entry(tab_encode, width=50)
entry_message.pack(pady=5)

ttk.Label(tab_encode, text="Enter Passcode:", font=("Arial", 12), background="#ffffff").pack(pady=5)
entry_password = ttk.Entry(tab_encode, show="*", width=50)
entry_password.pack(pady=5)

btn_encode = ttk.Button(tab_encode, text="Select Image & Encode", command=encode_message)
btn_encode.pack(pady=10)

# Decode Tab
ttk.Label(tab_decode, text="Enter Passcode:", font=("Arial", 12), background="#ffffff").pack(pady=5)
entry_password_decode = ttk.Entry(tab_decode, show="*", width=50)
entry_password_decode.pack(pady=5)

btn_decode = ttk.Button(tab_decode, text="Select Image & Decode", command=decode_message)
btn_decode.pack(pady=10)

# Function to close the app
def close_app(event=None):
    root.destroy()

# Bind "Escape" key to exit fullscreen and close app
root.bind("<Escape>", close_app)

# Run the GUI
root.mainloop()
