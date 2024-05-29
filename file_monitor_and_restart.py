import os
import time
import signal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, filepath, script):
        super().__init__()
        self.filepath = filepath
        self.script = script
        self.process = None
        self.last_change_time = 0
        self.debounce_time = 5

    def start_process(self):
        self.process = subprocess.Popen(["python", self.script])

    def stop_process(self):
        if self.process is not None:
            print(f"Stopping {self.script}...")
            self.process.terminate()
            self.process.wait()
            print(f"{self.script} stopped.")

    def on_any_event(self, event):
        current_time = time.time()
        if current_time - self.last_change_time < self.debounce_time:
            return
        self.last_change_time = current_time

        if event.src_path.endswith(self.filepath):
            print(f"{self.filepath} has changed. Restarting {self.script}...")
            self.stop_process()
            self.start_process()

if __name__ == "__main__":
    file_to_watch = "face_encodings.npy"  # Change this to the appropriate file name
    script_to_restart = "runFaster.py"  # Change this to the script name
    event_handler = FileChangeHandler(file_to_watch, script_to_restart)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()

    try:
        event_handler.start_process()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        event_handler.stop_process()
        observer.stop()
    observer.join()
