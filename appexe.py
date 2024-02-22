import os
import tkinter as tk
from PIL import Image, ImageTk
import speech_recognition as sr
from googletrans import Translator
from langdetect import detect
import webbrowser
import urllib.parse

# Set the INDIC_RESOURCES_PATH environment variable
os.environ['INDIC_RESOURCES_PATH'] = 'C:\\Users\\adity\\AppData\\Roaming\\Python\\Python312\\site-packages\\indicnlp'

# Initialize the recognizer
recognizer = sr.Recognizer()

# Function to capture audio input with dynamic duration
def record_audio():
    print("Listening... (Speak now)")
    with sr.Microphone() as source:
        audio = recognizer.listen(source, phrase_time_limit=5)  # Adjust the phrase_time_limit as needed
    return audio

# Function to recognize language using speech recognition
def recognize_language(audio):
    try:
        language = recognizer.recognize_google(audio, language='en')
        return language.lower()  # Convert the recognized language to lowercase
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the language.")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    return None

# Function to detect language
def detect_language(text):
    try:
        language = detect(text)
        return language
    except:
        print("Language detection failed.")
        return None

# Function to translate text
def translate_text(text, dest_lang):
    if text is None:
        print("Text to translate is None.")
        return ""

    if isinstance(text, str):
        translator = Translator()
        translated_text = translator.translate(text, dest=dest_lang)
        print("Translated text:", translated_text.text)  # Debugging print statement
        return translated_text.text
    else:
        print("Invalid input for translation.")
        return ""

# Function to open the web browser and search for the translated text
def search_web():
    website_name = website_name_entry.get()
    spoken_language = spoken_language_entry.get()
    query = query_entry.get()
    
    if not website_name:
        print("Please enter the website name.")
        return
    if not spoken_language:
        print("Please specify the language to speak.")
        return
    if not query:
        print("Please enter the search query.")
        return

    website_url = f"https://www.{website_name.lower()}.com"

    # Translate the search query to English
    try:
        translated_query = translate_text(query, dest_lang="en")
        print("Translated query:", translated_query)

        # Update GUI labels with search information
        website_name_label.config(text=f"Website name: {website_name}")
        spoken_language_label.config(text=f"Language to speak: {spoken_language}")
        query_label.config(text=f"Search query: {query}")
        translated_query_label.config(text=f"Translated query: {translated_query}")

        if website_name == "amazon":
            website_search_url = "https://www.amazon.com/s?k=" + urllib.parse.quote_plus(translated_query)
            webbrowser.open_new_tab(website_search_url)
        else:
            website_search_url = website_url + "/search?q=" + urllib.parse.quote_plus(translated_query)
            webbrowser.open_new_tab(website_search_url)
    except Exception as e:
        print("An error occurred during translation:", e)

# Create the main window
root = tk.Tk()
root.title("Voice Search App")

# Load logo image
logo_img = Image.open("C:/Users/adity/Downloads/logo-removebg-preview-removebg-preview.jpg")  # Replace with the path to your logo image
logo_img = logo_img.resize((200, 200))  # Adjust size as needed
logo_img = ImageTk.PhotoImage(logo_img)

# Create label for logo
logo_label = tk.Label(root, image=logo_img)
logo_label.place(relx=0.05, rely=0.05)  # Adjust position as needed

# Load microphone image
mic_img = Image.open("C:/Users/adity/Desktop/micc.JPG")  # Replace with the path to your microphone image
mic_img = mic_img.resize((80, 80))
mic_img = ImageTk.PhotoImage(mic_img)

# Function to handle microphone button click event
def on_mic_click(entry):
    audio = record_audio()
    spoken_language = recognize_language(audio)
    if spoken_language:
        entry.delete(0, tk.END)
        entry.insert(0, spoken_language)

# Create GUI elements
spoken_language_label = tk.Label(root, text="Language to speak:")
spoken_language_entry = tk.Entry(root, width=50)
website_name_label = tk.Label(root, text="Website name:")
query_label = tk.Label(root, text="Search query:")
translated_query_label = tk.Label(root, text="Translated query:")
website_name_entry = tk.Entry(root, width=50)
query_entry = tk.Entry(root, width=50)
search_button = tk.Button(root, text="Start Voice Search", command=search_web, image=mic_img, compound="left")

# Create microphone buttons
spoken_language_mic_button = tk.Button(root, image=mic_img, command=lambda: on_mic_click(spoken_language_entry))
website_name_mic_button = tk.Button(root, image=mic_img, command=lambda: on_mic_click(website_name_entry))
query_mic_button = tk.Button(root, image=mic_img, command=lambda: on_mic_click(query_entry))

# Place GUI elements in the window
# Calculate the width and height of the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the x and y coordinates for the window to be centered
x_coordinate = (screen_width - root.winfo_reqwidth()) / 2
y_coordinate = (screen_height - root.winfo_reqheight()) / 2

# Set the window position
root.geometry("+%d+%d" % (x_coordinate, y_coordinate))

# Place GUI elements in the window
spoken_language_label.place(relx=0.25, rely=0.1, anchor="center")
spoken_language_entry.place(relx=0.5, rely=0.1, anchor="center")
spoken_language_mic_button.place(relx=0.75, rely=0.1, anchor="center")
website_name_label.place(relx=0.25, rely=0.3, anchor="center")
website_name_entry.place(relx=0.5, rely=0.3, anchor="center")
website_name_mic_button.place(relx=0.75, rely=0.3, anchor="center")
query_label.place(relx=0.25, rely=0.5, anchor="center")
query_entry.place(relx=0.5, rely=0.5, anchor="center")
query_mic_button.place(relx=0.75, rely=0.5, anchor="center")
search_button.place(relx=0.5, rely=0.7, anchor="center")
translated_query_label.place(relx=0.5, rely=0.9, anchor="center")

# Run the application
root.mainloop()
