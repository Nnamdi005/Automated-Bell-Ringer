# Bell Ringer with Alarms
## Project Description
Bell Ringer with Alarms is a Python-based desktop application that manages alarms, schedules, and emergency notifications. The app provides an easy-to-use interface for scheduling alarms with text-to-speech notifications, customizable schedules, and support for multiple alarms. It also includes an emergency "fire alarm" mode for immediate evacuation alerts.

This project is designed with Tkinter for the user interface, pygame for audio playback, and pyttsx3 for text-to-speech functionality. The app is packaged as a standalone .exe file using PyInstaller.

# Features
Alarm Scheduling: Set alarms with custom messages and assign them to specific days of the week.

Text-to-Speech: Announces alarm messages using a speech synthesizer.

Audio Playback: Plays a bell sound for alarms and an emergency fire alarm sound.

Day Selection: Configure alarms to repeat on specific days of the week.

Real-Time Alarm Checking: Continuously monitors and triggers alarms at the appropriate time.

Emergency Fire Alarm Mode: Activates a looping alarm sound and evacuation message.

Persistent Storage: Alarms are saved in a JSON file and loaded on application startup.

User-Friendly Interface: Built with Tkinter, featuring buttons, scrollable lists, and input fields.


# Requirements
## Dependencies
Python 3.10+ (tested on Python 3.12)
Required Python libraries:
pygame

pyttsx3

tkinter

json

# System Requirements
Windows OS

A working sound system for audio playback

# Installation and Setup
## Clone the Repository

git clone https://github.com/Endee5/automated-bell-ringer-system.git

cd automated-bell-ringer-system

## Install Dependencies
## run the application


# Usage Instructions
Launch the application (bell_ringer.exe or python bell_ringer.py).

Use the "Set Alarm" section to schedule alarms:

Enter a time in HH:MM format.

Add a custom alarm message.

Select the days of the week for the alarm.

Click "Set Alarm" to save it.

View scheduled alarms in the scrollable list.

Delete alarms by clicking the "Delete" button next to an alarm.

Activate the Fire/Emergency Alarm button to play a continuous emergency alert.

Add a custom message in the message box and click "Say Message" to hear it.


# License
This project is licensed under the MIT License. See the LICENSE file for details.

# Author
Developed by Nnamdi Chidi.

Feel free to contribute to this project by submitting issues or feature requests! 😊
