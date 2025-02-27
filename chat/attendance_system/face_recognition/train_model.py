import face_recognition
import os
import pickle

def train_model(dataset_path=os.path.join("..", "dataset"), model_path="trained_model.pkl"):
    known_encodings = []
    known_names = []
    
    # Loop over each student's folder
    for user_folder in os.listdir(dataset_path):
        folder_path = os.path.join(dataset_path, user_folder)
        if not os.path.isdir(folder_path):
            continue
        # Process each image in the folder
        for image_name in os.listdir(folder_path):
            image_path = os.path.join(folder_path, image_name)
            image = face_recognition.load_image_file(image_path)
            boxes = face_recognition.face_locations(image)
            encodings = face_recognition.face_encodings(image, boxes)
            for encoding in encodings:
                known_encodings.append(encoding)
                known_names.append(user_folder)  # Format: Name_RollNumber_FaceID
    data = {"encodings": known_encodings, "names": known_names}
    with open(model_path, "wb") as f:
        pickle.dump(data, f)
    print("Training completed and model saved to", model_path)

if __name__ == "__main__":
    train_model()
