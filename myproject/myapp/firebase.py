import pyrebase
from pathlib import Path
import os
from django.conf import settings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

config = {
    "apiKey": "AIzaSyBVnXXEUy3ujtvX_m7ldMnVk3gxK3AdirA",
    "authDomain": "total-time-tracker.firebaseapp.com",
    "databaseURL": "gs://total-time-tracker.appspot.com",
    "storageBucket": "total-time-tracker.appspot.com",
    # serviceAccount this allows us to bypass authenticating users on this end.
    # I plan to do that on the front end with a log in process
    "serviceAccount": os.path.join(settings.BASE_DIR, "serviceAccountCredentials.json"),
}


firebase = pyrebase.initialize_app(config)

# source_blob_name = "UQ4ADY.json"
# #The path to which the file should be downloaded
# destination_file_name = r"temp\ftmp.json"

# # Storage is coming from your firebase.py file
storage = firebase.storage()
# bucket = storage.bucket()
# blob = bucket.blob(source_blob_name)
# data = blob.download_as_text(destination_file_name)
