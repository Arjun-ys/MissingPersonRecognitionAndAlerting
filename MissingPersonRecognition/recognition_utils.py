import face_recognition
import cv2
from database_utils import fetch_missing_persons, get_image

def recognize_faces_in_image(image_path):
    print("Loading image for recognition...")
    try:
        unknown_image = face_recognition.load_image_file(image_path)
        unknown_encodings = face_recognition.face_encodings(unknown_image)
    except Exception as e:
        print(f"Error loading or encoding image: {e}")
        return []

    if not unknown_encodings:
        print("No faces found in the image.")
        return []

    print(f"Number of faces found: {len(unknown_encodings)}")
    print("Fetching missing persons from the database...")

    missing_persons = fetch_missing_persons()
    matches_found = []

    for person in missing_persons:
        try:
            image_bytes = get_image(person["image_file_id"])
            with open("temp.jpg", "wb") as temp_image:
                temp_image.write(image_bytes)

            known_image = face_recognition.load_image_file("temp.jpg")
            known_encoding = face_recognition.face_encodings(known_image)[0]
        except Exception as e:
            print(f"Error processing image for {person['name']}: {e}")
            continue

        for unknown_encoding in unknown_encodings:
            match = face_recognition.compare_faces([known_encoding], unknown_encoding, tolerance=0.6)
            if match[0]:
                print(f"Match found: {person['name']}")
                matches_found.append({
                    "name": person["name"],
                    "metadata": person["metadata"]
                })

    return matches_found


def recognize_faces_in_video():
    print("Starting video feed for recognition...")
    video_capture = cv2.VideoCapture(0)

    missing_persons = fetch_missing_persons()
    known_encodings = []
    known_names = []

    for person in missing_persons:
        try:
            image_bytes = get_image(person["image_file_id"])
            with open("temp.jpg", "wb") as temp_image:
                temp_image.write(image_bytes)

            known_image = face_recognition.load_image_file("temp.jpg")
            known_encoding = face_recognition.face_encodings(known_image)[0]
            known_encodings.append(known_encoding)
            known_names.append(person["name"])
        except Exception as e:
            print(f"Error encoding image for {person['name']}: {e}")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to capture video frame.")
            break

        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.6)
            for i, match in enumerate(matches):
                if match:
                    print(f"Match found: {known_names[i]}")
                    cv2.putText(frame, known_names[i], (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        cv2.imshow("Video Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
