# QR Code Absensi App

A simple Flask web application for attendance tracking using QR codes. The application allows students to scan QR codes generated for each student to mark their attendance.

## Features

- **QR Code Scanning:** Students can scan QR codes using the device camera to register their attendance.
- **Manual Attendance:** In addition to QR code scanning, the app supports manual attendance entry.
- **Data Storage:** The app stores attendance data, including the date and list of students present.
- **QR Code Generation:** The application provides a feature to generate QR codes for new students.

## Prerequisites

Make sure you have the following installed:

- [Python](https://www.python.org/) (>=3.6)
- [Flask](https://flask.palletsprojects.com/en/2.1.x/)
- [OpenCV](https://pypi.org/project/opencv-python/)
- [qrcode](https://pypi.org/project/qrcode/)

Install the required packages using the following command:

```bash
pip install Flask opencv-python qrcode[pil]
```

## Usage

1. Clone the repository:

```bash
git clone https://github.com/developerlight/absen-scanqr-python.git
cd absen-scanqr-python
```

2. Run the Flask application:

```bash
python app.py
```

3. Open your browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to access the application.

## Routes

- `/`: Landing page with general information.
- `/scan_qr`: QR code scanning page.
- `/process_qr`: Processing scanned QR codes.
- `/absensi`: Manual attendance entry.
- `/absensii`: API endpoint for attendance with JSON data.
- `/generate_qrcode`: Page for generating QR codes for new students.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
