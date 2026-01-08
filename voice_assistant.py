import speech_recognition as sr
import pyttsx3
import datetime
import google.generativeai as genai
import tkinter as tk
from tkinter import scrolledtext
import threading
import os
import sys

# ---------------- CONFIG ----------------
API_KEY = "AIzaSyD46wVLyQmgyDRDp60gY1sbXBi0eBDhyEM"  # set this in your environment
if not API_KEY:
    print("ERROR: GEMINI_API_KEY not set.")
    sys.exit(1)

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

engine = pyttsx3.init()

# ---------------- FLAGS ----------------
GUI_MODE = True
root = None

# ---------------- SPEAK ----------------
def speak(text):
    if GUI_MODE:
        text_area.insert(tk.END, f"\n[Assistant]: {text}")
        text_area.see(tk.END)
    else:
        print(f"[Assistant]: {text}")

    engine.say(text)
    engine.runAndWait()

# ---------------- COMMAND HANDLER ----------------
def handle_command(command):
    if not command.strip():
        return

    if GUI_MODE:
        text_area.insert(tk.END, f"\n[You]: {command}")
        text_area.see(tk.END)
    else:
        print(f"[You]: {command}")

    command = command.lower()

    if "time" in command:
        speak(datetime.datetime.now().strftime("The time is %I:%M %p."))
    elif "date" in command:
        speak(datetime.datetime.now().strftime("Today is %B %d, %Y."))
    elif "exit" in command or "quit" in command:
        speak("Goodbye.")
        if GUI_MODE:
            root.quit()
        else:
            sys.exit(0)
    else:
        try:
            response = model.generate_content(command)
            speak(response.text)
        except Exception as e:
            speak("I couldn't reach the AI service.")
            print(e)

# ---------------- TEXT INPUT ----------------
def send_text():
    command = user_entry.get()
    user_entry.delete(0, tk.END)
    handle_command(command)

# ---------------- VOICE INPUT ----------------
def listen_voice():
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            speak("Listening.")
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            text = r.recognize_google(audio)
            handle_command(text)

    except OSError:
        speak("No microphone detected. Please type your command.")
    except sr.UnknownValueError:
        speak("I didn't understand that.")
    except sr.WaitTimeoutError:
        speak("No speech detected.")
    except sr.RequestError:
        speak("Speech recognition service is unavailable.")

def start_listening():
    threading.Thread(target=listen_voice, daemon=True).start()

# ---------------- GUI SETUP ----------------
try:
    root = tk.Tk()
    root.title("AI Voice Assistant")
    root.geometry("650x450")

    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    entry_frame = tk.Frame(root)
    entry_frame.pack(fill=tk.X, padx=10)

    user_entry = tk.Entry(entry_frame)
    user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

    send_button = tk.Button(entry_frame, text="Send")
    send_button.pack(side=tk.RIGHT)

except tk.TclError:
    GUI_MODE = False
    print("GUI not available. Running in console-only mode.")

# ---------------- GUI BINDINGS ----------------
if GUI_MODE:
    send_button.config(command=send_text)
    user_entry.bind("<Return>", lambda e: send_text())

    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)

    tk.Button(button_frame, text="🎤 Listen", command=start_listening).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="🕒 Time", command=lambda: handle_command("time")).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="📅 Date", command=lambda: handle_command("date")).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="❌ Exit", command=lambda: handle_command("exit")).pack(side=tk.LEFT, padx=5)

    text_area.insert(tk.END, "Assistant ready. Type or speak a command.\n")
    root.mainloop()

# ---------------- CONSOLE MODE ----------------
else:
    print("Assistant ready. Type commands (or Ctrl+C to exit).")
    while True:
        try:
            cmd = input("> ")
            handle_command(cmd)
        except KeyboardInterrupt:
            print("\nGoodbye.")
            break
