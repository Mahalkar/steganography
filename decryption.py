import cv2

def decrypt_message(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Image not found!")
        return

    try:
        with open("key.txt", "r") as f:
            stored_password = f.read().strip()
    except FileNotFoundError:
        print("Encryption key not found!")
        return

    pas = input("Enter passcode for decryption: ")

    if pas == stored_password:
        c = {i: chr(i) for i in range(255)}
        message = ""

        n, m, z = 0, 0, 0
        while True:
            try:
                message += c[img[n, m, z]]
                n = (n + 1) % img.shape[0]
                m = (m + 1) % img.shape[1]
                z = (z + 1) % 3
            except KeyError:
                break

        print("Decryption successful! Hidden message:", message)
    else:
        print("Incorrect passcode! Access denied.")

if __name__ == "__main__":
    decrypt_message("encryptedImage.jpg")
