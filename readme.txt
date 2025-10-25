Quantum Video-to-Audio Converter with Qiskit
=============================================

Description:
------------
This project is a **Quantum-enhanced Video-to-Audio Converter** built using Python 3.12. 
It allows users to upload video files (MP4, MOV, AVI, MKV) and convert them into MP3 audio files. 
Quantum algorithms using Qiskit are integrated to **modulate audio chunks based on qubit measurements**, demonstrating a real quantum effect in the conversion process.

Features:
---------
1. Upload video and convert to audio.
2. Quantum-enhanced processing: each audio chunk is modified based on **qubit measurement**.
3. Download the converted MP3 audio directly from the browser.
4. Attractive HTML frontend using Flask templates.
5. Works with multiple video formats: MP4, MOV, AVI, MKV.

Folder Structure:
-----------------
QuantumVideoToAudio/
├── app.py                   # Main Flask application
├── templates/
│   └── index.html           # HTML template for the web interface
└── uploads/                 # Folder to store uploaded videos and converted audio files

Requirements:
-------------
- Python 3.12
- Flask
- MoviePy
- Qiskit
- Qiskit Aer
- pydub
- numpy
- FFmpeg (must be installed and added to system PATH)

Setup Instructions:
-------------------
1. Clone this repository:

   git clone <your-repo-url>
   cd QuantumVideoToAudio

2. Create and activate a Python 3.12 virtual environment:

   python -m venv venv312
   .\venv312\Scripts\activate   (Windows PowerShell)

3. Install dependencies:

   pip install flask moviepy==1.0.3 qiskit qiskit-aer pydub numpy

4. Install FFmpeg:
   - Download from: https://www.gyan.dev/ffmpeg/builds/
   - Extract and add `bin` folder to system PATH
   - Verify installation: `ffmpeg -version`

5. Run the application:

   python app.py

6. Open a web browser and go to:

   http://127.0.0.1:5000

7. Upload a video and download the quantum-enhanced audio.

Usage Notes:
------------
- The quantum effect in the audio is demonstrated by **randomly modulating small audio chunks** based on qubit measurements.
- Currently, one qubit is used per chunk, applying a simple volume modification to create subtle quantum variations.
- Video-to-audio conversion is still handled classically; qubits influence the audio characteristics only.

License:
--------
MIT License

Author:
-------
Akanksha