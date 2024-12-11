# Missing Person Recognition System

## Overview
The Missing Person Recognition System is a Python-based project that utilizes face recognition technology to help identify and locate missing persons. The system allows users to:

1. Add missing persons (image, name, and metadata) to the database.
2. Recognize individuals from an image or a real-time video feed.
3. Send email alerts when a missing person is identified.

## Features
- **Face Recognition**: Uses `face_recognition` library for detecting and identifying faces.
- **Database Integration**: Stores images and metadata using MongoDB and GridFS.
- **Real-time Video Recognition**: Detects faces in video streams.
- **Email Notifications**: Sends alerts when a match is found.

## Prerequisites
- Python 3.8 or above
- MongoDB (local or hosted)
- Basic understanding of Python and terminal/command line usage

## Installation
1. Clone this repository or download the project files.
   ```bash
   git clone https://github.com/your-repository/missing-person-recognition.git
   cd missing-person-recognition
   ```

2. Install the required Python packages.
   ```bash
   pip install -r requirements.txt
   ```

3. Set up MongoDB:
   - Install MongoDB and start the service on your machine.
   - Ensure MongoDB is running on `localhost:27017` (default).
   
4. Configure the `.env` file:
   - Create a file named `.env` in the project root.
   - Add the following variables:
     ```env
     EMAIL=your_email@gmail.com
     EMAIL_PASSWORD=your_email_password
     GMAIL_CLIENT_ID=your_client_id
     GMAIL_CLIENT_SECRET=your_client_secret
     GMAIL_REFRESH_TOKEN=your_refresh_token
     ```

## File Structure
```
.
├── main.py                   # Entry point of the application
├── requirements.txt          # Python dependencies
├── database_utils.py         # Handles image and metadata storage/retrieval
├── recognition_utils.py      # Face recognition functionality
├── alert_utils.py            # Sends email alerts
├── .env                      # Environment variables (excluded from repo)
├── README.md                 # Documentation
└── known_faces/              # Folder to preload images (optional)
```

## Usage

### 1. Adding a Missing Person
Store a missing person’s image and metadata in the database.
```bash
python main.py --mode add --file "path/to/image.jpg" --name "Person Name" --metadata "age=30" "last_seen=NYC"
```

### 2. Recognize Missing Person in an Image
Identify missing persons in a given image.
```bash
python main.py --mode recognize-image --file "path/to/image.jpg"
```

### 3. Recognize Missing Person in a Video
Use the real-time video feed to identify missing persons.
```bash
python main.py --mode recognize-video
```

## Testing
Run the project with test data to verify functionality. For example:
- Add a known face image to the database.
- Run `recognize-image` or `recognize-video` modes to test recognition and alerts.

## Troubleshooting
1. **MongoDB Connection Issues**:
   - Ensure MongoDB service is running.
   - Check `localhost:27017` connectivity.

2. **Face Recognition Errors**:
   - Ensure the input image contains a clearly visible face.
   - Check for proper installation of `dlib` and `face_recognition` libraries.

3. **Email Alert Failures**:
   - Verify `.env` variables are correctly set.
   - Ensure your Gmail account has "Less secure app access" enabled or is set up for OAuth2.

## Contributing
Feel free to fork this repository and make improvements. Pull requests are welcome!

## License
This project is licensed under the MIT License. See `LICENSE` for details.

## Acknowledgements
- [face_recognition](https://github.com/ageitgey/face_recognition)
- [MongoDB](https://www.mongodb.com/)
- [GridFS](https://docs.mongodb.com/manual/core/gridfs/)

