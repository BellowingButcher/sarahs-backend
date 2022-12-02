import pyrebase

config = {
  "apiKey": "AIzaSyBVnXXEUy3ujtvX_m7ldMnVk3gxK3AdirA",
  "authDomain": "total-time-tracker.firebaseapp.com",
  "databaseURL": "gs://total-time-tracker.appspot.com",
  "storageBucket": "total-time-tracker.appspot.com",
  # serviceAccount this allows us to bypass authenticating users on this end.
  # I plan to do that on the front end with a log in process
  # "serviceAccount": "path/to/serviceAccountCredentials.json",
}


firebase = pyrebase.initialize_app(config)

db = firebase.database()
print(db)
