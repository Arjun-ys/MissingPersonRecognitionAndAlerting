import face_recognition
import cv2
from database_utils import get_image, list_missing_persons, delete_person
from alert_utils import send_email_alert

def recognize_faces_in_image(image_path):
    # Load the image
    unknown_image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    # Fetch all missing persons from the database
    missing_persons = list_missing_persons()

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces([fp['image'] for fp in missing_persons], face_encoding)
        name = "Unknown"

        # Find the best match
        face_distances = face_recognition.face_distance([fp['image'] for fp in missing_persons], face_encoding)
        best_match_index = face_distances.argmin()

        if matches[best_match_index]:
            name = missing_persons[best_match_index]['name']
            metadata = missing_persons[best_match_index]['metadata']
            print(f"Match found: {name}")

            # Send alert if needed
            send_email_alert("recipient_email@gmail.com", name, metadata)
        else:
            print("No match found.")

def recognize_faces_in_video():
    video_capture = cv2.VideoCapture(0)  # Open the default camera

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Find all face locations in the current frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Fetch all missing persons from the database
        missing_persons = list_missing_persons()

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces([fp['image'] for fp in missing_persons], face_encoding)
            name = "Unknown"

            # Find the best match
            face_distances = face_recognition.face_distance([fp['image'] for fp in missing_persons], face_encoding)
            best_match_index = face_distances.argmin()

            if matches[best_match_index]:
                name = missing_persons[best_match_index]['name']
                metadata = missing_persons[best_match_index]['metadata']
                print(f"Match found: {name}")

                # Send alert if needed
                send_email_alert("recipient_email@gmail.com", name, metadata)
            else:
                print("No match found.")

        # Display the resulting image with rectangles and labels
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

        cv2.imshow('Video', frame)

        # Press 'q' to exit the video capture
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
