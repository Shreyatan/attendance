import cv2
import face_recognition
import numpy as np
import pandas as pd
from datetime import datetime

# Load known faces and their names
def load_known_faces(known_faces_path=r"C:\Users\Lenovo\OneDrive\Desktop\Project\images"):
    known_encodings = []
    known_names = []

    import os
    for filename in os.listdir(known_faces_path):
        if filename.endswith(('.jpg', '.png')):
            img_path = f"{known_faces_path}/{filename}"
            img = face_recognition.load_image_file(img_path)
            aligned_img = align_face(img)  # Align the face before encoding
            encodings = face_recognition.face_encodings(aligned_img)
            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(os.path.splitext(filename)[0])
    return known_encodings, known_names

# Align face using landmarks
# Align face using landmarks
def align_face(image):
    face_landmarks_list = face_recognition.face_landmarks(image)
    if not face_landmarks_list:
        return None  # If no landmarks are detected, return None

    # Use the first face detected (extend logic for multiple faces if needed)
    landmarks = face_landmarks_list[0]

    # Get the eye coordinates
    left_eye = np.mean(landmarks['left_eye'], axis=0)
    right_eye = np.mean(landmarks['right_eye'], axis=0)

    # Calculate the angle between the eyes
    delta_x = right_eye[0] - left_eye[0]
    delta_y = right_eye[1] - left_eye[1]
    angle = np.degrees(np.arctan2(delta_y, delta_x))

    # Calculate the center between the eyes
    eye_center = ((left_eye[0] + right_eye[0]) / 2, (left_eye[1] + right_eye[1]) / 2)

    # Perform the rotation to align the eyes horizontally
    rotation_matrix = cv2.getRotationMatrix2D(tuple(eye_center), angle, scale=1)
    aligned_image = cv2.warpAffine(image, rotation_matrix, (image.shape[1], image.shape[0]))

    return aligned_image




# Other functions (initialize_attendance, mark_attendance, etc.) remain the same
def load_attendance_from_excel(output_file="c:/Users/Lenovo/OneDrive/Desktop/Project/Attendance.xlsx"):
    try:
        attendance_df = pd.read_excel(output_file)
    except FileNotFoundError:
        attendance_df = pd.DataFrame(columns=["Name"])  # Initialize if file doesn't exist

    # Ensure 'Name' column exists in the DataFrame
    if 'Name' not in attendance_df.columns:
        attendance_df['Name'] = pd.NA
        
    print("Columns in the DataFrame:", attendance_df.columns)
    attendance_df.rename(columns=lambda x: x.strip(), inplace=True)  # Remove leading/trailing spaces
    print("Renamed Columns:", attendance_df.columns)


    return attendance_df


def initialize_attendance(excel_file, sheet_name="Sheet1"):
    """Load attendance Excel file and ensure a current date column is present."""
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Load the existing attendance sheet
    try:
        attendance_df = pd.read_excel(excel_file, sheet_name=sheet_name)
    except FileNotFoundError:
        # If the file doesn't exist, create a new DataFrame
        attendance_df = pd.DataFrame(columns=["Name"])
    
    # Ensure 'Name' column exists in the DataFrame and rename it if necessary
    attendance_df.rename(columns=lambda x: x.strip(), inplace=True)

    if 'Name' not in attendance_df.columns:
        raise ValueError("The 'Name' column is missing in the Excel file. Please add it and re-run.")
    
    # Add current date column if it doesn't exist, and mark all as 'Absent' by default
    if current_date not in attendance_df.columns:
        attendance_df[current_date] = "Absent"
    
    # Mark all students as 'Absent' by default for the current date
    attendance_df[current_date] = "Absent"

    return attendance_df

# Mark attendance: Set 'Present' for the recognized student
def mark_attendance(name, attendance_df, excel_file, sheet_name="Sheet1"):
    """Mark a student present in the attendance DataFrame."""
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Check if the name exists in the 'Name' column
    if name in attendance_df['Name'].values:
        # Mark the student as 'Present' for today
        attendance_df.loc[attendance_df['Name'] == name, current_date] = "Present"
        print(f"{name} marked present for {current_date}")
    else:
        print(f"{name} not found in the attendance sheet.")

    # Save the updated DataFrame back to Excel
    attendance_df.to_excel(excel_file, index=False, sheet_name=sheet_name)
    return attendance_df





# Save attendance to Excel
def save_attendance_to_excel(attendance_df, output_file="c:/Users/Lenovo/OneDrive/Desktop/Project/Attendance.xlsx"):
    attendance_df.to_excel(output_file, index=False)
    print(f"Attendance saved to {output_file}")


# Main function
def main():
    excel_file = "c:/Users/Lenovo/OneDrive/Desktop/Project/Attendance.xlsx"
    sheet_name = "Sheet1"

    # Initialize attendance from Excel
    attendance_df = initialize_attendance(excel_file, sheet_name)

    print("Initialized Attendance DataFrame:")
    print(attendance_df.head())  # Debug: Print the first few rows

    # Load known faces
    known_encodings, known_names = load_known_faces()

    # Start video capture
    video_capture = cv2.VideoCapture(0)
    print("Press 'q' to exit.")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to grab frame. Exiting...")
            break

        # Convert frame from BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Find all face locations in the frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = []

        # Align each face and then encode
        for face_location in face_locations:
            top, right, bottom, left = face_location
            face_image = rgb_frame[top:bottom, left:right]

    # Align the face
            aligned_face = align_face(face_image)
            if aligned_face is None:
                print("No landmarks detected. Skipping face.")
                continue

    # Encode the aligned face
            encoding = face_recognition.face_encodings(aligned_face)
            if not encoding:
                print("Failed to encode face. Skipping.")
                continue

            face_encodings.append(encoding[0])

        for face_encoding, face_location in zip(face_encodings, face_locations):
    # Compare the detected face with known faces
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)

            if matches:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_names[best_match_index]
                else:
                    name = "Unknown"
            else:
                name = "Unknown"

    # Mark the student or log as "Unknown"
            if name != "Unknown":
                attendance_df = mark_attendance(name, attendance_df, excel_file, sheet_name)
            else:
                print(f"Unrecognized face detected at location {face_location}. Marked as 'Unknown'.")

    # Draw a rectangle around the face
            top, right, bottom, left = face_location
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)  # Green for known, red for unknown
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)


            if matches:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_names[best_match_index]

                    # Mark the student as present in the attendance sheet
                    attendance_df = mark_attendance(name, attendance_df, excel_file, sheet_name)

                    # Draw a rectangle around the face
                    top, right, bottom, left = face_location
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    
            else:
                top, right, bottom, left = face_location
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2) 
                cv2.putText(frame, "Unknown", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                print("Unidentified face detected.")
                # Mark "Unknown" in the attendance sheet
                attendance_df = mark_attendance("Unknown", attendance_df, excel_file, sheet_name)
        # Show the video frame with face recognition
        cv2.imshow('Face Recognition Attendance System', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    video_capture.release()
    cv2.destroyAllWindows()

    # Save the attendance
    attendance_df.to_excel(excel_file, index=False, sheet_name=sheet_name)
    print(f"Final attendance saved to {excel_file}")


if __name__ == "__main__":
    main()
