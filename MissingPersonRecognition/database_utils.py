import face_recognition
import cv2
from database_utils import fetch_missing_persons

def recognize_faces_in_image(image_path):
    # Load the image
    unknown_image = face_recognition.load_image_file(image_path)
    unknown_encodings = face_recognition.face_encodings(unknown_image)

    if not unknown_encodings:
        print("No faces found in the image.")
        return []

    # Fetch missing persons from the database
    missing_persons = fetch_missing_persons()

    matches_found = []
    for missing_person in missing_persons:
        # Decode the image and calculate the face encoding
        known_image = face_recognition.load_image_file(missing_person["image"])
        known_encoding = face_recognition.face_encodings(known_image)[0]

        for unknown_encoding in unknown_encodings:
            # Compare the encodings
            match = face_recognition.compare_faces([known_encoding], unknown_encoding)

            if match[0]:
                print(f"Match found: {missing_person['name']}")
                matches_found.append({
                    "name": missing_person["name"],
                    "metadata": missing_person["metadata"]
                })

    return matches_found

def recognize_faces_in_video():
    video_capture = cv2.VideoCapture(0)

    # Fetch missing persons from the database
    missing_persons = fetch_missing_persons()
    known_encodings = []
    known_names = []

    for missing_person in missing_persons:
        known_image = face_recognition.load_image_file(missing_person["image"])
        known_encoding = face_recognition.face_encodings(known_image)[0]
        known_encodings.append(known_encoding)
        known_names.append(missing_person["name"])

    matches_found = []
    while True:
        # Capture a single frame from the video feed
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to capture video frame.")
            break

        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            for i, match in enumerate(matches):
                if match:
                    print(f"Match found: {known_names[i]}")
                    matches_found.append({
                        "name": known_names[i],
                        "metadata": missing_persons[i]["metadata"]
                    })
                    break

        # Display the video feed with detected face(s)
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        cv2.imshow("Video", frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return matches_found
