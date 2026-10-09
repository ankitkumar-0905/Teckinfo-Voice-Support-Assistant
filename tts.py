import pyttsx3

# Step 1: TTS engine initialize karo
engine = pyttsx3.init()

# Step 2: Bolne ke liye text
text = "Hello! MySQL service kaise restart karein."

# Step 3: Text ko speech queue mein add karo
engine.say(text)

# Step 4: Speech ko play karo
engine.runAndWait()