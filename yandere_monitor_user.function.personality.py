import time
import subprocess
import win32gui
import psutil

class AIAssistant:
    def __init__(self):
        self.is_monitoring_enabled = False

    def monitor_user(self):
        if self.is_monitoring_enabled:
            print("Monitoring user...")
            try:
                while True:
                    user_input = self.get_user_input()
                    print("User input:", user_input)

                    active_window = self.get_active_window()
                    print("Active window:", active_window)

                    running_processes = self.get_running_processes()
                    print("Running processes:", running_processes)

                    self.analyze_user_activity(user_input, active_window, running_processes)

                    self.perform_action_based_on_condition(user_input)

                    time.sleep(1)
            except KeyboardInterrupt:
                print("Monitoring stopped.")
        else:
            print("Monitoring is currently disabled.")

    def enable_monitoring(self):
        self.is_monitoring_enabled = True
        print("Monitoring has been enabled.")

    def disable_monitoring(self):
        self.is_monitoring_enabled = False
        print("Monitoring has been disabled.")

    def get_user_input(self):
        user_input = input("User input: ")
        return user_input

    def get_active_window(self):
        try:
            active_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        except win32gui.error:
            active_window = "Unknown"
        return active_window

    def get_running_processes(self):
        try:
            running_processes = [proc.name() for proc in psutil.process_iter(['name'])]
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            running_processes = []
        return running_processes

    def analyze_user_activity(self, user_input, active_window, running_processes):
        if "password" in user_input.lower():
            self.record_activity("User entered a password.")
            self.send_notification("Warning: Sensitive information entered!")

        if "important_process.exe" in running_processes:
            self.record_activity("An important process is running.")
            self.send_notification("Attention: Important process detected!")

        if active_window == "Private Browsing":
            self.send_notification("Privacy Alert: User is browsing privately.")

        if user_input.lower() == "help":
            self.display_help()

        # Add more activity analysis and conditions here

    def perform_action_based_on_condition(self, user_input):
        if "open browser" in user_input.lower():
            self.open_browser()
        elif "play music" in user_input.lower():
            self.play_music()
        # Add more conditions and corresponding actions here
        elif "search" in user_input.lower():
            self.search_web(user_input)

    def open_browser(self):
        subprocess.run(["start", "chrome.exe"])
        # Add more code for browser opening and control

    def play_music(self):
        subprocess.run(["start", "spotify.exe"])
        # Add more code for music playing and control

    def search_web(self, user_input):
        search_query = user_input.split("search", 1)[1].strip()
        search_url = "https://www.google.com/search?q=" + search_query
        subprocess.run(["start", search_url])
        # Add more code for search functionality

    def record_activity(self, activity):
        try:
            with open("activity_log.txt", "a") as log_file:
                log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {activity}\n")
        except IOError:
            print("Failed to record activity. Please check file permissions.")
        # Add more code for activity logging and analysis

    def send_notification(self, message):
        try:
            subprocess.run(["notify-send", "AI Assistant", message])
        except FileNotFoundError:
            print("Notification command not found. Please ensure the notification mechanism is supported.")
        # Add more code for notification handling

    def display_help(self):
        print("Available commands:")
        print("  - open browser: Open the default web browser.")
        print("  - play music: Play music using the default music player.")
        print("  - search [query]: Perform a web search with the specified query.")
        # Add more help information for available commands


# Example usage:
assistant = AIAssistant()
assistant.enable_monitoring()
assistant.monitor_user()
