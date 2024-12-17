import face_recognition
import cv2
from io import BytesIO
from database_utils import fetch_missing_persons, get_image

# Helper function to fetch and encode known faces
def get_known_faces():
    print("Fetching missing persons from the database...")
    missing_persons = fetch_missing_persons()
    known_encodings = []
    known_names = []

    for person in missing_persons:
        try:
            # Get the image bytes from the database
            image_bytes = get_image(person["image_file_id"])
            if not image_bytes:
                print(f"Image data for {person['name']} is missing or corrupted.")
                continue

            # Load the image in memory using BytesIO
            image_stream = BytesIO(image_bytes)
            known_image = face_recognition.load_image_file(image_stream)

            # Get face encodings
            known_encoding = face_recognition.face_encodings(known_image)[0]
            known_encodings.append(known_encoding)
            known_names.append(person["name"])
        except Exception as e:
            print(f"Error processing image for {person['name']}: {e}")
    
    return known_encodings, known_names

# Recognize faces in a static image
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

    # Fetch known faces
    known_encodings, known_names = get_known_faces()
    if not known_encodings:
        print("No known faces found in the database.")
        return []

    matches_found = []

    for unknown_encoding in unknown_encodings:
        # Use face_distance and find the closest match
        face_distances = face_recognition.face_distance(known_encodings, unknown_encoding)
        best_match_index = face_distances.argmin()

        if face_distances[best_match_index] < 0.5:  # Adjust tolerance as needed
            name = known_names[best_match_index]
            print(f"Match found: {name}")
            matches_found.append({
                "name": name,
                "distance": face_distances[best_match_index]
            })

    return matches_found

# Recognize faces in a video feed
def recognize_faces_in_video():
    print("Starting video feed for recognition...")
    video_capture = cv2.VideoCapture(1) #set this as 0 for default webcam or 1 for phone camera

    # Fetch known faces
    known_encodings, known_names = get_known_faces()
    if not known_encodings:
        print("No valid encodings found for known faces. Video recognition cannot proceed.")
        return

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to capture video frame.")
            break

        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Use face_distance to find the closest match
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_match_index = face_distances.argmin()

            if len(face_distances) > 0 and face_distances[best_match_index] < 0.6:  # Adjust tolerance
                name = known_names[best_match_index]
                print(f"Match found: {name}")
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Display the video feed
        cv2.imshow("Video Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
