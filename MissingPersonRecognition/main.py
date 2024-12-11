#Steps to Run the Program
# Add Missing Person:
# Run the program in "add" mode and provide the image file, the person's name, and optional metadata.
# Example: python main.py --mode add --file "path_to_image" --name "John Doe" --metadata "age=30,last_seen=NYC" --email "your_email@gmail.com"
# Recognize in Image:
# For recognition from an image file, use the "recognize-image" mode.
# Example: python main.py --mode recognize-image --file "path_to_image_for_recognition"
# If a recognized person matches an entry in the database, an alert email is sent to the specified email address.
# Recognize in Video:
# For real-time video recognition, run in "recognize-video" mode.
# Example: python main.py --mode recognize-video

from dotenv import load_dotenv
import os

load_dotenv()

EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
GMAIL_CLIENT_ID = os.getenv("GMAIL_CLIENT_ID")
GMAIL_CLIENT_SECRET = os.getenv("GMAIL_CLIENT_SECRET")
GMAIL_REFRESH_TOKEN = os.getenv("GMAIL_REFRESH_TOKEN")



import argparse
from database_utils import store_person, fetch_missing_persons, get_image, delete_person
from recognition_utils import recognize_faces_in_image, recognize_faces_in_video
from alert_utils import send_email_alert

def main():
    parser = argparse.ArgumentParser(description="Missing Person Recognition System")
    parser.add_argument("--mode", choices=["add", "recognize-image", "recognize-video"], required=True,
                        help="Mode of operation: add (store a new missing person), recognize-image, or recognize-video")
    parser.add_argument("--file", type=str, help="Path to the file (image for recognition or missing person)")
    parser.add_argument("--name", type=str, help="Name of the missing person (for 'add' mode)")
    parser.add_argument("--metadata", type=str, nargs="*", help="Additional metadata for missing persons (key=value format)")
    parser.add_argument("--email", type=str, help="Recipient email for alerts")

    args = parser.parse_args()

    if args.mode == "add":
        if not args.file or not args.name:
            print("Error: For 'add' mode, both --file and --name are required.")
            return
        
        # Parse metadata into a dictionary
        metadata = {}
        if args.metadata:
            for item in args.metadata:
                key, value = item.split("=", 1)
                metadata[key] = value

        # Store the missing person
        file_id = store_person(args.file, args.name, metadata)

        print(f"Stored missing person: {args.name} (ID: {file_id})")

    elif args.mode == "recognize-image":
        if not args.file:
            print("Error: For 'recognize-image' mode, --file is required.")
            return

        # Recognize faces in the provided image
        results = recognize_faces_in_image(args.file)
        for person in results:
            print(f"Recognized person: {person['name']}")
            if args.email:
                send_email_alert(args.email, person['name'], person['metadata'])

    elif args.mode == "recognize-video":
        # Recognize faces in real-time video feed
        recognize_faces_in_video()

if __name__ == "__main__":
    main()
