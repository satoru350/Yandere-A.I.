import logging
import time
import subprocess
import psutil
import json
import os
import pynput
import keyboard
import win32gui
import webbrowser

class AIAssistant:
    def __init__(self):
        self.is_monitoring_enabled = False

        # Initializing logging
        logging.basicConfig(filename="activity.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        self.logger = logging.getLogger("AIAssistant")

        # Initializing configuration
        config_path = "config.json"
        self.config = self.load_config(config_path)

    def load_config(self, config_path):
        try:
            if os.path.exists(config_path):
                with open(config_path) as f:
                    return json.load(f)
            else:
                # Default configuration
                return {
                    "monitor_interval": 1,
                    "action_threshold": 3,
                    "logging_enabled": True,
                }
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.error(f"Error loading configuration: {e}")
            # Returning an empty configuration as fallback
            return {}

    def save_config(self, config_path):
        try:
            with open(config_path, "w") as f:
                json.dump(self.config, f, indent=4)
        except (FileNotFoundError, json.JSONDecodeError, IOError) as e:
            self.logger.error(f"Error saving configuration: {e}")

    def monitor_user(self):
        if self.is_monitoring_enabled:
            print("Monitoring user...")
            try:
                # Initializing process list
                process_list = self.get_running_processes()

                # Initializing event listener for user input
                listener = keyboard.Listener(on_press=self.on_key_press)
                listener.start()

                while True:
                    # Getting active window and updating process list
                    active_window = self.get_active_window()
                    process_list = self.get_running_processes(process_list)

                    # Logging user activity
                    if self.config.get("logging_enabled", False):
                        self.record_activity(active_window, process_list)

                    # Analyzing user activity and performing actions if necessary
                    self.analyze_user_activity(active_window, process_list)

                    time.sleep(self.config.get("monitor_interval", 1))
            except KeyboardInterrupt:
                # Stopping event listener and monitoring
                listener.stop()
                self.is_monitoring_enabled = False
                print("Monitoring stopped.")
            except Exception as e:
                self.logger.error(f"Error during monitoring: {e}")
        else:
            print("Monitoring is currently disabled.")

    def on_key_press(self, key):
        try:
            # Handling alphanumeric character input
            if key.char.isalnum():
                self.analyze_user_activity(key.char, "", [])
        except AttributeError:
            # Ignoring non-alphanumeric key presses
            pass

    def enable_monitoring(self):
        self.is_monitoring_enabled = True
        print("Monitoring has been enabled.")

    def disable_monitoring(self):
        self.is_monitoring_enabled = False
        print("Monitoring has been disabled.")

    def get_active_window(self):
        try:
            active_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        except win32gui.error:
            active_window = "Unknown"
        return active_window

    def get_running_processes(self, existing_processes=[]):
        try:
            # Retrieving updated list of processes
            new_processes = [proc.name() for proc in psutil.process_iter(['name'])]

            # Updating the existing process list by removing processes that are no longer running
            existing_processes = [process for process in existing_processes if process in new_processes]

            # Adding new processes to the existing process list
            existing_processes.extend(process for process in new_processes if process not in existing_processes)

            return existing_processes
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            return existing_processes

    def analyze_user_activity(self, active_window, process_list):
        if "password" in active_window.lower():
            self.perform_action("Warning: Sensitive information entered!")

        if any(keyword in active_window.lower() for keyword in ["browser", "chrome", "firefox", "edge", "safari"]):
            self.perform_action("Opening browser...")

        if any(keyword in process.lower() for process in process_list for keyword in ["spotify", "music", "media player"]):
            self.perform_action("Playing/pausing music...")

        if any(keyword in process.lower() for process in process_list for keyword in ["search", "search engine"]):
            self.perform_action("Performing web search...")

    def perform_action(self, message):
        # Performing an action
        print(message)

    def record_activity(self, active_window, process_list):
        try:
            with open("activity_log.txt", "a") as log_file:
                log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Active Window: {active_window}, Processes: {process_list}\n")
        except IOError:
            print("Failed to record activity. Please check file permissions.")

    def search_web(self, user_input):
        search_query = user_input.split("search", 1)[1].strip()
        search_url = "https://www.google.com/search?q=" + search_query
        webbrowser.open_new_tab(search_url)

    def perform_action_based_on_condition(self, user_input):
        if "open browser" in user_input.lower():
            self.perform_action("Opening browser...")
            webbrowser.open_new_tab("https://www.google.com")
        elif "play music" in user_input.lower():
            self.perform_action("Playing music...")
            # Code for playing music goes here
        elif "search" in user_input.lower():
            self.search_web(user_input)

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
