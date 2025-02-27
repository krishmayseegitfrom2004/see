import cv2
import os

def capture_images(user_name, roll_number, face_id, num_images=8):
    # Create a folder for the student in the dataset directory
    dir_path = os.path.join("..", "dataset", f"{user_name}_{roll_number}_{face_id}")
    os.makedirs(dir_path, exist_ok=True)
    
    cap = cv2.VideoCapture(0)
    count = 0
    print("Press 'c' to capture an image. You need to capture at least 8 images.")
    while count < num_images:
        ret, frame = cap.read()
        if not ret:
            continue
        cv2.imshow("Capture - Press 'c' to capture", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            image_path = os.path.join(dir_path, f"img_{count}.jpg")
            cv2.imwrite(image_path, frame)
            count += 1
            print(f"Captured image {count}/{num_images}")
        elif key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    user_name = input("Enter Name: ")
    roll_number = input("Enter Roll Number: ")
    face_id = input("Enter Face ID: ")
    capture_images(user_name, roll_number, face_id)
