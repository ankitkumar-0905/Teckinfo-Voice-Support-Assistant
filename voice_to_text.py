import sounddevice as sd
from scipy.io.wavfile import write
import whisper

# Step 1: Audio settings
sample_rate = 16000
duration = 5

# Step 2: Record voice
print("Speak now...")

audio = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype="int16"
)

sd.wait()

# Step 3: Save audio
write("audio.wav", sample_rate, audio)

# Step 4: Load Whisper model
print("Loading Whisper...")
model = whisper.load_model("base")

# Step 5: Convert speech into text
print("Converting speech to text...")
result = model.transcribe("audio.wav")

# Step 6: Display recognized text
print("You said:", result["text"])