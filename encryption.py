import cv2
import os

def encrypt_message(image_path, output_path):
    img = cv2.imread(image_path)  # Load image
    if img is None:
        print("Error: Image not found!")
        return

    msg = input("Enter secret message: ")
    password = input("Enter a passcode: ")

    d = {chr(i): i for i in range(255)}

    n, m, z = 0, 0, 0
    for char in msg:
        img[n, m, z] = d[char]
        n = (n + 1) % img.shape[0]
        m = (m + 1) % img.shape[1]
        z = (z + 1) % 3

    cv2.imwrite(output_path, img)
    os.system(f"start {output_path}")  # Opens the image on Windows

    with open("key.txt", "w") as f:
        f.write(password)

    print("Message encrypted successfully!")

if __name__ == "__main__":
    encrypt_message("mypic.jpg", "encryptedImage.jpg")
