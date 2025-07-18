import speech_recognition as sr
import pyttsx3
import os
import datetime
import time
import logging
import webbrowser
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
import tkinter as tk
from tkinter import Canvas
import random
import threading
import math

# Configure Gemini AI once at startup
GEMINI_API_KEY = "AIzaSyDPatNMu9otaw3L9ZPhJZGDCJcD0sRhEaA"
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    logging.debug("Gemini AI initialized successfully")
except Exception as e:
    print(f"Error initializing Gemini AI: {e}")
    logging.error(f"Error initializing Gemini AI: {e}")

# Set up logging
logging.basicConfig(filename='kavya.log', level=logging.DEBUG, format='%(asctime)s - %(message)s')

# Initialize the speech engine
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
        # Sanitize text and limit to 300 characters
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
        logging.error(f"Error: Gemini AI retry error: {e}")
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

# Hacker-themed GUI with matrix-style animation
def display_hacker_gui():
    try:
        root = tk.Tk()
        root.title("NICO - Advanced Tech Interface")
        root.geometry("1200x800")
        root.configure(bg="#0a0a0a")
        root.attributes('-alpha', 0.97)  # Subtle transparency for sleek effect

        # Create canvas
        canvas = Canvas(root, bg="#0a0a0a", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # Animation variables
        particles = [(random.randint(100, 1100), random.randint(100, 700), random.uniform(0, 2*math.pi), random.uniform(50, 150), random.uniform(0.02, 0.06)) for _ in range(30)]  # (x, y, angle, radius, speed)
        core_pulse = 0.5
        wave_phase = 0

        def update_ui():
            nonlocal core_pulse, wave_phase
            canvas.delete("all")

            # Draw gradient background with noise
            for y in range(0, 800, 10):
                shade = int(10 + (y / 800) * 25)
                canvas.create_rectangle(0, y, 1200, y + 10, fill=f"#{shade:02x}{shade:02x}{shade:02x}", outline="")
            for _ in range(50):  # Subtle noise
                x, y = random.randint(0, 1200), random.randint(0, 800)
                canvas.create_oval(x, y, x+1, y+1, fill="#1a1a1a", outline="")

            # Draw orbiting particles with trails
            for i in range(len(particles)):
                x, y, angle, radius, speed = particles[i]
                angle += speed
                new_x = 600 + math.cos(angle) * radius
                new_y = 400 + math.sin(angle) * radius
                # Draw trail
                for j in range(3):
                    trail_x = 600 + math.cos(angle - j * 0.1) * radius
                    trail_y = 400 + math.sin(angle - j * 0.1) * radius
                    alpha = 0.3 * (1 - j * 0.3)
                    color = f"#00{int(alpha * 240):02x}ff"
                    canvas.create_oval(trail_x - 2, trail_y - 2, trail_x + 2, trail_y + 2, fill=color, outline="")
                # Draw particle
                canvas.create_oval(new_x - 3, new_y - 3, new_x + 3, new_y + 3, fill="#00f0ff", outline="")
                particles[i] = (new_x, new_y, angle, radius, speed)

            # Draw pulsing core
            core_pulse = 0.5 + 0.5 * math.sin(time.time() * 1.5)
            core_radius = 20 + 10 * core_pulse
            core_color = f"#00{int(core_pulse * 200):02x}ff" if core_pulse < 0.75 else f"#cc{int((core_pulse - 0.75) * 4 * 200):02x}ff"
            canvas.create_oval(600 - core_radius, 400 - core_radius, 600 + core_radius, 400 + core_radius, fill=core_color, outline="#00f0ff")
            canvas.create_text(600, 400, text="CORE", fill="white", font=("Helvetica", 12, "bold"))

            # Draw wave effect
            wave_phase += 0.1
            for x in range(0, 1200, 10):
                y = 700 + 20 * math.sin(wave_phase + x * 0.05)
                canvas.create_line(x, y, x + 10, y, fill="#00f0ff", width=1)

            # Draw header with glow
            glow_color = f"#00{int(core_pulse * 100):02x}ff"
            canvas.create_text(602, 82, text="NICO: AI ASSISTANT v2.0", fill=glow_color, font=("Helvetica", 32, "bold"))
            canvas.create_text(600, 80, text="NICO: AI ASSISTANT v2.0", fill="#00f0ff", font=("Helvetica", 32, "bold"))
            canvas.create_text(602, 132, text="Developed by Karan, Android Innovator", fill="#cc00ff", font=("Helvetica", 18))
            canvas.create_text(600, 130, text="Developed by Karan, Android Innovator", fill="#cc00ff", font=("Helvetica", 18))

            # Draw HUD elements
            canvas.create_text(20, 20, text="SYSTEM: ACTIVE", fill="#00f0ff", font=("Helvetica", 12), anchor="nw")
            canvas.create_text(1180, 20, text="CORE: STABLE", fill="#00f0ff", font=("Helvetica", 12), anchor="ne")
            canvas.create_text(20, 780, text="MODE: ASSIST", fill="#00f0ff", font=("Helvetica", 12), anchor="sw")
            canvas.create_text(1180, 780, text="NET: ONLINE", fill="#00f0ff", font=("Helvetica", 12), anchor="se")
            # Animated corner arcs
            arc_pulse = 0.5 + 0.5 * math.sin(time.time() * 2)
            arc_color = f"#00{int(arc_pulse * 240):02x}ff"
            canvas.create_arc(10, 10, 50, 50, start=0, extent=90, outline=arc_color, width=2, style="arc")
            canvas.create_arc(1150, 10, 1190, 50, start=90, extent=90, outline=arc_color, width=2, style="arc")
            canvas.create_arc(10, 750, 50, 790, start=270, extent=90, outline=arc_color, width=2, style="arc")
            canvas.create_arc(1150, 750, 1190, 790, start=180, extent=90, outline=arc_color, width=2, style="arc")

            root.after(30, update_ui)

        # Start animation
        update_ui()

        # Run GUI
        root.mainloop()
        logging.debug("Modern UI closed")
    except Exception as e:
        print(f"Error in modern UI: {e}")
        logging.error(f"Error in modern UI: {e}")

def run_kavya():
    try:
        # Start hacker GUI in a separate thread
        gui_thread = threading.Thread(target=display_hacker_gui, daemon=True)
        gui_thread.start()
        logging.debug("Hacker GUI thread started")

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
