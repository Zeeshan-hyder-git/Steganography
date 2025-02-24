import cv2
import numpy as np
import os

def load_image(image_path):
    """Load an image and ensure it exists."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Error: Image '{image_path}' not found!")
    return cv2.imread(image_path, cv2.IMREAD_COLOR)

def generate_mappings():
    """Generate character-to-integer and integer-to-character mappings."""
    return {chr(i): i for i in range(256)}, {i: chr(i) for i in range(256)}

def encrypt_message(img, message):
    """Encrypt and embed the message into the image."""
    img = img.copy()  
    rows, cols, _ = img.shape
    char_to_int, _ = generate_mappings()
    
    if len(message) > rows * cols:
        raise ValueError("Error: Message is too long for the given image!")

    idx = 0
    for char in message:
        x, y = divmod(idx, cols)
        img[x, y, idx % 3] = max(0, min(char_to_int[char], 255))  # Ensure valid pixel values
        idx += 1

    return img.astype(np.uint8)

def decrypt_message(img, message_length):
    """Extract and decrypt the message from the image."""
    rows, cols, _ = img.shape
    _, int_to_char = generate_mappings()
    
    decrypted_msg = ""
    idx = 0

    for _ in range(message_length):
        x, y = divmod(idx, cols)
        decrypted_msg += int_to_char[img[x, y, idx % 3]]
        idx += 1

    return decrypted_msg

def main():
    image_path = "mdzeeshanhyder.jpg"
    
    try:
        img = load_image(image_path)
        message = input("Enter secret message: ").strip()
        password = input("Set a passcode: ").strip()

        encrypted_img = encrypt_message(img, message)

        encrypted_image_path = "encryptedImage.png"
        success = cv2.imwrite(encrypted_image_path, encrypted_img)
        if success:
            print(f"\n✅ Message successfully encrypted and saved as '{encrypted_image_path}'.")
            
            cv2.namedWindow("Encrypted Image", cv2.WINDOW_NORMAL)
            cv2.imshow("Encrypted Image", encrypted_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("\n❌ Error: Failed to save encrypted image!")
            return

        entered_password = input("\nEnter passcode for decryption: ").strip()
        if entered_password == password:
            decrypted_msg = decrypt_message(encrypted_img, len(message))
            print("\n🔓 Decrypted message:", decrypted_msg)
        else:
            print("\n❌ Authentication failed! Incorrect passcode. Image will not be displayed.")

    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
