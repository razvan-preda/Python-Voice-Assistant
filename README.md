# Interactive Voice Assistant (Python)

## Overview
A desktop-based virtual assistant built with Python. The application provides a hands-free conversational interface capable of listening to user voice commands, interpreting them, and responding via synthesized speech. It features a graphical user interface (GUI) and logs interaction history using a local database.

## Key Features
* **Speech-to-Text (STT):** Captures microphone input and converts it to text using the `SpeechRecognition` library.
* **Text-to-Speech (TTS):** Provides spoken audio feedback using the offline `pyttsx3` engine.
* **Real-time Weather Data:** Integrates with the OpenWeather API to fetch and speak current weather conditions for specified cities.
* **Command Logging:** Automatically initializes and stores a history of user queries and assistant responses in a local SQLite database.
* **Desktop GUI:** An accessible user interface built with `tkinter`, featuring visual feedback for microphone activation.

## Technologies & Libraries
* **Language:** Python 3.x
* **Core Libraries:** `SpeechRecognition`, `pyttsx3`, `sqlite3`, `tkinter`
* **Network/API:** `requests`, OpenWeather API
* **Audio Processing:** `PyAudio`

## Setup & Execution
1. Clone the repository to your local machine.
2. Install the required dependencies (e.g., `pip install SpeechRecognition pyttsx3 requests Pillow pyaudio`).
3. Replace the placeholder in the script with your own OpenWeather API key.
4. Run `Bobby.py` to launch the assistant. The SQLite database (`assistant_db.db`) will initialize automatically on the first run.
