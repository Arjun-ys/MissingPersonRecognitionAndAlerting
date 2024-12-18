import cv2
import face_recognition
from io import BytesIO
from database_utils import fetch_missing_persons, get_image

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

        if face_distances[best_match_index] < 0.6:  # Adjust tolerance as needed
            name = known_names[best_match_index]
            confidence = 1 - face_distances[best_match_index]  # Convert distance to confidence
            print(f"Match found: {name} with confidence: {confidence:.2f}")
            matches_found.append({
                "name": name,
                "distance": face_distances[best_match_index],
                "confidence": confidence
            })
        else:
            print("Mr.Nobody")

    return matches_found

def recognize_faces_in_video(camera_index=1):
    """
    Recognize faces from a video feed using the specified camera index.

    Args:
        camera_index (int): Index of the camera to use (default: 1 for iPhone camera).
    """
    print("Starting video feed for recognition...")

    # Initialize video capture
    video_capture = cv2.VideoCapture(camera_index)
    if not video_capture.isOpened():
        print(f"Error: Unable to access the camera at index {camera_index}.")
        return
    print("Camera successfully initialized.")

    # Fetch known faces from the database
    print("Fetching missing persons from the database...")
    known_encodings = []
    known_names = []

    try:
        missing_persons = fetch_missing_persons()
        for person in missing_persons:
            image_bytes = get_image(person["image_file_id"])
            if not image_bytes:
                print(f"Image data for {person['name']} is missing or corrupted.")
                continue

            # Decode the image and get face encodings
            image_stream = BytesIO(image_bytes)
            known_image = face_recognition.load_image_file(image_stream)
            known_encoding = face_recognition.face_encodings(known_image)[0]
            known_encodings.append(known_encoding)
            known_names.append(person["name"])
    except Exception as e:
        print(f"Error fetching known faces: {e}")
        video_capture.release()
        return

    print(f"Number of known encodings fetched: {len(known_encodings)}")
    if not known_encodings:
        print("No valid encodings found for known faces. Video recognition cannot proceed.")
        video_capture.release()
        return

    while True:
        print("Reading frame...")
        ret, frame = video_capture.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Resize the frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_small_frame = small_frame[:, :, ::-1]  # Convert to RGB

        # Detect face locations and encodings
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        print(f"Detected face locations: {face_locations}")
        print(f"Number of face encodings detected: {len(face_encodings)}")

        # Scale back face locations to the original frame size
        scaled_face_locations = [(top * 2, right * 2, bottom * 2, left * 2) for (top, right, bottom, left) in face_locations]

        # Match detected faces with known encodings
        for (top, right, bottom, left), face_encoding in zip(scaled_face_locations, face_encodings):
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            if len(face_distances) > 0:
                best_match_index = face_distances.argmin()
                confidence = 1 - face_distances[best_match_index]  # Calculate confidence
                if confidence > 0.6:  # Adjust confidence threshold as needed
                    name = known_names[best_match_index]
                    print(f"Match found: {name} with confidence: {confidence:.2f}")
                    # Draw bounding box and label with confidence
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, f"{name} ({confidence:.2f})", (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                else:
                    print("No confident match found, displaying 'Unknown'")
                    # Draw bounding box with 'Unknown' label
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.putText(frame, "Unknown", (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Display the video feed
        cv2.imshow("Video Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Quit on 'q'
            break

    video_capture.release()
    cv2.destroyAllWindows()
