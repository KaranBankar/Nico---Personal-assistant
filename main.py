import speech_recognition as sr
import pyttsx3
import os
import datetime
import time
import logging
import webbrowser
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions

GEMINI_API_KEY = "AIzaSyDPatNMu9otaw3L9ZPhJZGDCJcD0sRhEaA"
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    logging.debug("Gemini AI initialized successfully")
except Exception as e:
    print(f"Error initializing Gemini AI: {e}")
    logging.error(f"Error initializing Gemini AI: {e}")


logging.basicConfig(filename='kavya.log', level=logging.DEBUG, format='%(asctime)s - %(message)s')

def init_engine():
    try:
        engine = pyttsx3.init('sapi5')  
        voices = engine.getProperty('voices')
        
        heera_voice = None
        for voice in voices:
            if "heera" in voice.name.lower():
                heera_voice = voice.id
                break
        
        if heera_voice:
            engine.setProperty('voice', heera_voice)
            print(f"Selected voice: Microsoft Heera")
            logging.debug("Selected voice: Microsoft Heera")
        else:
            #print("Warning: Microsoft Heera voice not found. Using default voice.")
            engine.setProperty('voice', voices[0].id)
            #print(f"Selected voice: {voices[0].name}")
            logging.debug(f"Selected voice: {voices[0].name}")
        
        engine.setProperty('rate', 150)
        logging.debug(f"Engine properties: rate={engine.getProperty('rate')}, voice={engine.getProperty('voice')}")
        return engine
    except Exception as e:
        print(f"Error initializing speech engine: {e}")
        logging.error(f"Error initializing speech engine: {e}")
        return None

def speak(text):
    print(f"Nico: {text}")
    logging.debug(f"Speaking: {text}")
    engine = init_engine()
    if not engine:
        print("Error: Speech engine not initialized")
        logging.error("Speech engine not initialized")
        return
    try:
        # Sanitize text and limit to 100 characters
        text = ''.join(c for c in text if c.isprintable())[:300]
        logging.debug("Engine state: Attempting to speak")
        engine.stop()
        engine.say(text)
        engine.runAndWait()
        time.sleep(0.5)
        logging.debug("Speech completed successfully")
    except Exception as e:
        print(f"Error in speak function: {e}")
        logging.error(f"Error in speak function: {e}")

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        logging.debug("Listening started")
        try:
            audio = r.listen(source)
            command = r.recognize_google(audio).lower()
            print(f"You: {command}")
            logging.debug(f"Recognized command: {command}")
            return command
        except sr.UnknownValueError:
            print("Could not understand audio")
            logging.warning("Could not understand audio")
            return ""
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            logging.error(f"Speech recognition error: {e}")
            speak("Sorry Karan Sir, there was an issue with the speech recognition service.")
            return ""
        except Exception as e:
            print(f"Listening error: {e}")
            logging.error(f"Listening error: {e}")
            return ""

def query_gemini(command):
    try:
        # Prompt Gemini to respond naturally and concisely
        prompt = f"You are Nico, a friendly and conversational voice assistant created by Karan, an Android developer from Maharashtra. Respond to the following query naturally, as a human would, in a concise and helpful manner (max 50 words): '{command}'"
        response = model.generate_content(prompt)
        if response.text:
            logging.debug(f"Gemini response: {response.text.strip()}")
            return response.text.strip()
        else:
            logging.debug("Gemini returned no response text")
            return "Sorry Karan Sir, I couldn't find an answer for that."
    except google_exceptions.TooManyRequests as e:
        print(f"Error: Gemini AI quota exceeded: {e}")
        logging.error(f"Gemini AI quota exceeded: {e}")
        return "Sorry Karan Sir, I've reached my query limit. Please try again later."
    except google_exceptions.ResourceExhausted as e:
        print(f"Error: Gemini AI resource exhausted: {e}")
        logging.error(f"Gemini AI resource exhausted: {e}")
        return "Sorry Karan Sir, I've reached my query limit. Please try again later."
    except google_exceptions.RetryError as e:
        print(f"Error: Gemini AI retry error: {e}")
        logging.error(f"Gemini AI retry error: {e}")
        return "Sorry Karan Sir, I'm having trouble connecting to the AI service right now."
    except google_exceptions.ClientError as e:
        print(f"Error: Gemini AI client error: {e}")
        logging.error(f"Error: Gemini AI client error: {e}")
        return "Sorry Karan Sir, I couldn't process that request due to a client error."
    except Exception as e:
        print(f"Error querying Gemini AI: {e}")
        logging.error(f"Error querying Gemini AI: {e}")
        return "Sorry Karan Sir, I couldn't process that request right now."

def tell_about_karan():
    print("DEBUG: tell_about_karan function called")
    logging.debug("tell_about_karan function called")
    info = "Karan Sir is a passionate Android Developer from Maharashtra, and the developer of Nico assistant. Karan sir believes that marks doesn't matter skills matter"
    speak(info)

def run_kavya():
    try:
        speak("Hello Karan Sir, I am Nico — your personal assistant. How can I help you today?")
        
        while True:
            command = listen()
            if not command:
                continue
            print(f"DEBUG: Processing command: {command}")
            logging.debug(f"Processing command: {command}")

            if "nico open chrome" in command or "nico open karo" in command:
                speak("Sure Karan Sir, opening Google Chrome for you.")
                chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
                try:
                    os.startfile(chrome_path)
                except FileNotFoundError:
                    print(f"Error: Chrome path not found: {chrome_path}")
                    logging.error(f"Chrome path not found: {chrome_path}")

            elif "nico open vs code" in command:
                speak("Alright Karan Sir, opening Visual Studio Code.")
                vs_code_path = "C:\\Users\\karan\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                try:
                    os.startfile(vs_code_path)
                except FileNotFoundError:
                    print(f"Error: VS Code path not found: {vs_code_path}")
                    logging.error(f"VS Code path not found: {vs_code_path}")

            elif "nico open youtube" in command:
                speak("Sure Karan Sir, opening YouTube for you.")
                youtube_url = "https://www.youtube.com"
                try:
                    webbrowser.open(youtube_url)
                    logging.debug(f"Opened YouTube: {youtube_url}")
                except Exception as e:
                    print(f"Error opening YouTube: {e}")
                    logging.error(f"Error opening YouTube: {e}")

            elif "nico open chat gpt" in command:
                speak("Sure Karan Sir, opening ChatGPT for you.")
                chatgpt_url = "https://chatgpt.com/"
                try:
                    webbrowser.open(chatgpt_url)
                    logging.debug(f"Opened ChatGPT: {chatgpt_url}")
                except Exception as e:
                    print(f"Error opening ChatGPT: {e}")
                    logging.error(f"Error opening ChatGPT: {e}")

            elif "nico play video" in command:
                speak("Playing a YouTube video for you, Karan Sir.")
                video_url = "https://youtu.be/sUf2PtEZris?si=CQKBT36p6DzlRg29"
                try:
                    webbrowser.open(video_url)
                    logging.debug(f"Opened YouTube video: {video_url}")
                except Exception as e:
                    print(f"Error opening YouTube video: {e}")
                    logging.error(f"Error opening YouTube video: {e}")

            elif "open project folder" in command:
                speak("Opening your project folder now, Karan Sir.")
                project_path = "C:\\Users\\karan\\Documents\\MyProjects"
                try:
                    os.startfile(project_path)
                except FileNotFoundError:
                    print(f"Error: Project folder not found: {project_path}")
                    logging.error(f"Error: Project folder not found: {project_path}")

            elif "nico what time" in command:
                time_str = datetime.datetime.now().strftime('%I:%M %p')
                speak(f"Karan Sir, the current time is {time_str}")

            elif "nico what date" in command:
                date = datetime.datetime.now().strftime('%d %B %Y')
                speak(f"Karan Sir, today's date is {date}")

            elif "nico who is karan" in command or "nico tell me about karan" in command:
                tell_about_karan()

            elif "exit" in command or "by nico" in command:
                speak("Goodbye Karan Sir. Nico is going offline.")
                break

            else:
                # Fallback to Gemini AI for unrecognized commands
                speak("Let me check that for you, Karan Sir.")
                gemini_response = query_gemini(command)
                speak(gemini_response)

    except Exception as e:
        print(f"Error in run_kavya: {e}")
        logging.error(f"Error in run_kavya: {e}")
        speak("Sorry Karan Sir, an error occurred. Let me try to continue.")
        run_kavya()  # Restart the loop to avoid shutdown

if __name__ == "__main__":
    try:
        run_kavya()
    except KeyboardInterrupt:
        speak("Nico is shutting down.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        logging.error(f"Unexpected error: {e}")
        speak("An unexpected error occurred. Nico is shutting down.")
