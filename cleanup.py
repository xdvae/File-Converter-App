import threading
import os
import time
from flask import Flask

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"

def clear_uploads_periodically():
    while True:
        time.sleep(3600)  # Wait 1 hour
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")

# Start the cleanup thread
threading.Thread(target=clear_uploads_periodically, daemon=True).start()

if __name__ == '__main__':
    app.run()
