import tkinter as tk
from tkinter import ttk
import pyttsx3 as tts
import threading
import time
from datetime import datetime
import pygame
import os
import json
import sys
import shutil

# Initialize text-to-speech engine
engine = tts.init()

# Initialize pygame mixer
pygame.mixer.init()

# Paths to audio files
bell_sound = os.path.join(os.path.dirname(__file__), 'audio/bell3.mp3')
fire_alarm_sound = os.path.join(os.path.dirname(__file__), 'audio/fire_alarm.mp3')
json_file_path = os.path.join(os.path.dirname(__file__), 'json/alarms.json')

def get_base_path():
    # Return the path of the bundled or source directory
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS  # Temporary directory for PyInstaller
    return os.path.dirname(os.path.abspath(__file__))

def get_writable_path():
    # Use a writable location for alarms.json
    user_data_dir = os.path.join(os.path.expanduser("~"), "BellRinger")
    os.makedirs(user_data_dir, exist_ok=True)  # Create directory if it doesn't exist
    return os.path.join(user_data_dir, "alarms.json")

def initialize_alarms_file():
    # Get paths
    bundled_json_path = os.path.join(get_base_path(), "json", "alarms.json")
    writable_json_path = get_writable_path()

    # If the writable file doesn't exist, copy the bundled file
    if not os.path.exists(writable_json_path):
        if os.path.exists(bundled_json_path):  # Only copy if bundled file exists
            shutil.copy(bundled_json_path, writable_json_path)
    
    return writable_json_path

# Initialize the alarms.json path
json_file_path = initialize_alarms_file()

# Load alarms from file
alarm_settings = []
triggered_alarms_today = set()

def load_alarms_from_file():
    global alarm_settings
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as f:
            alarm_settings = json.load(f)
    else:
        alarm_settings = []

def save_alarms_to_file():
    with open(json_file_path, 'w') as f:
        json.dump(alarm_settings, f)

# Text-to-speech function (threaded)
def text_to_speech(text, rate=100):
    def speak():
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate', rate)
        engine.setProperty('volume', 0.8)
        engine.say(text)
        engine.runAndWait()

    threading.Thread(target=speak, daemon=True).start()

# Play bell sound function (threaded)
def play_bell(bell_path, volume=0.6, duration=3):
    def play_alarm():
        pygame.mixer.music.load(bell_path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play()
        time.sleep(duration)
        pygame.mixer.music.stop()

    threading.Thread(target=play_alarm, daemon=True).start()

# Function to check and trigger alarms
def check_alarms():
    now = datetime.now()
    current_time = now.strftime('%H:%M')
    today = now.strftime('%A')

    for alarm in alarm_settings:
        alarm_time = alarm['time']
        alarm_id = (today, alarm_time)  # Unique identifier for daily alarm

        if current_time == alarm_time and today in alarm['days'] and alarm_id not in triggered_alarms_today:
            trigger_alarm(alarm['text'])
            triggered_alarms_today.add(alarm_id)  # Mark as triggered for the day
    
    root.after(15000, check_alarms)  # Check every 15 seconds

# Trigger alarm function with 15-second cycle
def trigger_alarm(text):
    end_time = time.time() + 15  # Alarm cycle for 15 seconds
    def alarm_sequence():
        while time.time() < end_time:
            play_bell(bell_sound)     # Play bell for 3 seconds
            time.sleep(3)           # Short pause before TTS
            text_to_speech(text)      # Say alarm text
            time.sleep(5)             # Short pause after TTS
    
    threading.Thread(target=alarm_sequence, daemon=True).start()

# Reset triggered alarms at midnight
def reset_triggered_alarms():
    triggered_alarms_today.clear()
    root.after(86400000, reset_triggered_alarms)  # Reset every 24 hours (86400000 ms)

# Schedule new alarm
def schedule_alarm():
    alarm_time = alarm_time_entry.get()
    alarm_text = alarm_text_entry.get()
    selected_days = [day for day, var in day_vars.items() if var.get()]

    try:
        alarm_time_obj = datetime.strptime(alarm_time, '%H:%M')
        alarm_settings.append({
            'time': alarm_time_obj.strftime('%H:%M'),
            'text': alarm_text,
            'days': selected_days
        })

        save_alarms_to_file()
        update_alarm_listbox()
        status_label.config(text="Alarm scheduled!", foreground="green")
    except ValueError:
        status_label.config(text="Invalid time format. Please use HH:MM.", foreground="red")

# Function to delete an alarm
def delete_alarm(index):
    if 0 <= index < len(alarm_settings):
        del alarm_settings[index]
        save_alarms_to_file()
        update_alarm_listbox()
        status_label.config(text="Alarm deleted.", foreground="blue")

# Update alarm listbox with delete buttons
def update_alarm_listbox():
    for widget in alarm_list_frame.winfo_children():
        widget.destroy()

    for idx, alarm in enumerate(alarm_settings):
        days_str = ', '.join(alarm['days'])
        alarm_text = f'{alarm["time"]} - {alarm["text"]} ({days_str})'

        label = tk.Label(alarm_list_frame, text=alarm_text, font=('Arial', 12), anchor="w")
        label.grid(row=idx, column=0, sticky="w")

        delete_btn = tk.Button(alarm_list_frame, text="Delete", command=lambda i=idx: delete_alarm(i))
        delete_btn.grid(row=idx, column=1, padx=5)

    alarm_canvas.configure(scrollregion=alarm_canvas.bbox("all"))

# Fire alarm functionality (plays continuously and says emergency message)
def fire_alarm():
    fire_text = "Emergency! Please evacuate immediately!"
    end_time = time.time() + 360 * 60

    def play_fire_alarm():
        pygame.mixer.music.load(fire_alarm_sound)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(loops=-1)
        while time.time() < end_time:
            time.sleep(1)
        pygame.mixer.music.stop()

    threading.Thread(target=play_fire_alarm, daemon=True).start()

    while time.time() < end_time:
        text_to_speech(fire_text, rate=120)
        time.sleep(5)

# Load alarms and update listbox at startup
load_alarms_from_file()

# Set up main application window
root = tk.Tk()
root.title("Bell Ringer with Alarms")
root.geometry("500x700")
root.configure(bg="#f0f0f0")

# Alarm input section
alarm_frame = tk.Frame(root, bg="#f0f0f0")
alarm_frame.pack(pady=10)

alarm_time_label = tk.Label(alarm_frame, text="Set Alarm Time (HH:MM):", font=('Arial', 12), bg="#f0f0f0")
alarm_time_label.grid(row=0, column=0, padx=5)
alarm_time_entry = tk.Entry(alarm_frame, font=('Arial', 12))
alarm_time_entry.grid(row=0, column=1, padx=5)

alarm_text_label = tk.Label(alarm_frame, text="Alarm Text:", font=('Arial', 12), bg="#f0f0f0")
alarm_text_label.grid(row=1, column=0, padx=5)
alarm_text_entry = tk.Entry(alarm_frame, font=('Arial', 12))
alarm_text_entry.grid(row=1, column=1, padx=5)

# Day selection checkboxes
day_vars = {}
days_frame = tk.Frame(alarm_frame, bg="#f0f0f0")
days_frame.grid(row=2, column=0, columnspan=2, pady=10)
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
for i, day in enumerate(days):
    var = tk.IntVar()
    cb = tk.Checkbutton(days_frame, text=day, variable=var, bg="#f0f0f0")
    cb.grid(row=i // 4, column=i % 4, padx=5, pady=5, sticky="w")
    day_vars[day] = var

# Set Alarm button
set_alarm_btn = tk.Button(alarm_frame, text="Set Alarm", command=schedule_alarm, font=('Arial', 12, 'bold'))
set_alarm_btn.grid(row=3, column=0, columnspan=2, pady=10)

# Fire/Emergency alarm button
fire_alarm_frame = tk.Frame(alarm_frame, bg="red")
fire_alarm_frame.grid(row=4, column=0, columnspan=2, pady=10)
fire_alarm_btn = tk.Button(fire_alarm_frame, text="Fire/Emergency Alarm", command=fire_alarm, font=('Arial', 12, 'bold'), bg='red', fg='white')
fire_alarm_btn.pack(padx=10, pady=5)

# Add message box for typing custom messages
message_frame = tk.Frame(root, bg="#f0f0f0")
message_frame.pack(pady=10)

message_label = tk.Label(message_frame, text="Type a Message to Speak:", font=('Arial', 12), bg="#f0f0f0")
message_label.grid(row=0, column=0, padx=5)

message_entry = tk.Entry(message_frame, font=('Arial', 12), width=30)
message_entry.grid(row=0, column=1, padx=5)

# Button to speak the typed message
speak_message_btn = tk.Button(message_frame, text="Say Message", command=lambda: text_to_speech(message_entry.get()), font=('Arial', 12, 'bold'))
speak_message_btn.grid(row=1, column=0, columnspan=2, pady=10)

# Alarm list section with scrollbar
alarm_canvas = tk.Canvas(root, bg="#f0f0f0", width=450, height=200)
alarm_scrollbar = tk.Scrollbar(root, orient="vertical", command=alarm_canvas.yview)
alarm_canvas.configure(yscrollcommand=alarm_scrollbar.set)

alarm_list_frame = tk.Frame(alarm_canvas, bg="#f0f0f0")
alarm_list_frame.bind("<Configure>", lambda e: alarm_canvas.configure(scrollregion=alarm_canvas.bbox("all")))

alarm_canvas.create_window((0, 0), window=alarm_list_frame, anchor="nw")
alarm_canvas.pack(side="left", fill="both", expand=True)
alarm_scrollbar.pack(side="right", fill="y")

# Status label
status_label = tk.Label(root, text="", font=('Arial', 12), bg="#f0f0f0")
status_label.pack(pady=5)

# Start the periodic check and reset triggered alarms at midnight
root.after(30000, check_alarms)
root.after(86400000, reset_triggered_alarms)

# Populate listbox on startup
update_alarm_listbox()

# Run the main loop
root.mainloop()
