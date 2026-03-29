import sqlite3
import pyttsx3
import speech_recognition as sr
import tkinter as tk
from PIL import Image, ImageTk
import threading
import requests


# 1. Database initialization for questions and answers
def init_db():
    conn = sqlite3.connect('assistant_db.db')
    c = conn.cursor()
    c.execute(''' 
        CREATE TABLE IF NOT EXISTS questions_answers (
            question TEXT PRIMARY KEY,
            answer TEXT
        )
    ''')
    random_questions_answers = [
        ("what are you doing", "I am doing fine, thank you!"),
        ("how are you", "I am doing great, thank you for asking!"),
        ("what is your name", "My name is Bobby, the voice assistant!"),
        ("how old are you", "I am an artificial intelligence program, I don't have an age."),
        ("what is your favorite color", "I don't have preferences, but I can tell you your favorite color!"),
        ("what is my favorite color", "Your favorite color is purple!"),
        ("what is artificial intelligence",
         "Artificial intelligence is the field in which computers are trained to solve complex problems."),
        ("who won the last world cup", "The last FIFA world cup was won by Argentina in 2022!"),
        ("what is 2+2", "2+2 equals 4"),
        ("how tall is the eiffel tower", "The Eiffel Tower is 324 meters tall."),
        ("give me a random fact",
         "Did you know that honey never spoils? Archaeologists have found pots of honey in ancient tombs that are over 3,000 years old!"),
        (
        "who is the president of the united states", "As of 2025, the President of the United States is Donald Trump."),
        ("how far is the moon from earth",
         "The average distance from the Earth to the Moon is about 384,400 kilometers."),
        ("what is the tallest mountain in the world",
         "Mount Everest is the tallest mountain in the world, standing at 8,848 meters above sea level."),
        ("what is the smallest country in the world",
         "Vatican City is the smallest country in the world by both population and area."),
        ("where do you live", "I live in the cloud, but I am always available to assist you!"),
        ("give me a motivational quote", "Keep your face always toward the sunshine, and shadows will fall behind you.")
    ]
    for question, answer in random_questions_answers:
        c.execute("INSERT OR IGNORE INTO questions_answers (question, answer) VALUES (?, ?)", (question, answer))
    conn.commit()
    conn.close()


# Initialize database on startup
init_db()


# 2. Function to search for an answer in the database
def get_answer_from_db(question):
    # Strip punctuation for better matching
    question = question.replace('?', '').strip()

    if "weather" in question:
        return get_weather()

    conn = sqlite3.connect('assistant_db.db')
    c = conn.cursor()
    c.execute("SELECT answer FROM questions_answers WHERE question=?", (question,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else "Sorry, I don't have an answer for that question."


# 3. Function to fetch current weather data
def get_weather():
    # REMINDER: Users must insert their own API key below
    api_key = "YOUR_API_KEY_HERE"
    city = "Bucharest"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            main = data["main"]
            weather_description = data["weather"][0]["description"]
            temperature = main["temp"]
            return f"The weather in {city} is currently {weather_description} with a temperature of {temperature}°C."
        else:
            return "Sorry, I couldn't fetch the weather information right now. Please check the API key."
    except Exception as e:
        return f"Error fetching weather: {e}"


# 4. Text-to-Speech (TTS) engine setup
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


# 5. Function to continuously listen for the wake word
def listen_for_activation():
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening for 'hey Bobby'...")
            update_status_label("Listening for 'hey Bobby'...")
            try:
                audio = recognizer.listen(source, timeout=10)
                phrase = recognizer.recognize_google(audio, language="en-US").lower()
                print(f"Detected phrase: {phrase}")
                if "hey bobby" in phrase:
                    print("Activation command detected!")
                    speak("Hey there, what can I help you with?")
                    update_status_label("I am listening to your question...")
                    start_assistant()  # Start listening for the actual question
            except sr.UnknownValueError:
                pass  # Ignore background noise that isn't understood
            except sr.RequestError:
                print("Could not request results from Google Speech Recognition.")
            except Exception as e:
                print(f"Error: {e}")


# 6. Main function to handle user query after activation
def start_assistant():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("You can ask me a question...")
        try:
            audio = recognizer.listen(source, timeout=10)
            question = recognizer.recognize_google(audio, language="en-US").lower()
            print(f"User's question: {question}")
            answer = get_answer_from_db(question)
            print(f"Answer: {answer}")
            speak(answer)
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that!")
            speak("Sorry, I didn't understand that!")
        except sr.RequestError:
            print("There was an issue connecting to the Google API.")
            speak("There was an issue connecting to the Google service.")


# 7. GUI Setup and Logo creation
def create_logo(image_path):
    try:
        img = Image.open(image_path).convert("RGBA")
        img = img.resize((100, 100), Image.Resampling.LANCZOS)
    except IOError:
        print("Could not load the image.")
        img = Image.new("RGBA", (100, 100), (255, 255, 255, 255))
    return img


# Image path (ensure the 'images' folder exists in the same directory)
image_path = "mic.png"

logo = create_logo(image_path)

# Tkinter window configuration
root = tk.Tk()
root.title("Python Voice Assistant")
root.geometry("400x400")
root.configure(background="white")

# Display logo
logo_photo = ImageTk.PhotoImage(logo)
label_logo = tk.Label(root, image=logo_photo, bg="white")
label_logo.pack(pady=20)

# Status label
status_label = tk.Label(root, text="Starting engine...", font=("Helvetica", 12), fg="blue", bg="white")
status_label.pack(pady=20)


# Exit function
def stop_assistant():
    print("Assistant stopped.")
    speak("Goodbye!")
    root.quit()


# Stop button
stop_button = tk.Button(root, text="Stop Assistant", command=stop_assistant, font=("Helvetica", 12), bg="#ff5555",
                        fg="white")
stop_button.pack(pady=10)


# Function to safely update GUI text from threads
def update_status_label(new_text):
    status_label.config(text=new_text)
    root.update_idletasks()


# Start the background listening thread
threading.Thread(target=listen_for_activation, daemon=True).start()

# Start the main GUI loop
root.mainloop()