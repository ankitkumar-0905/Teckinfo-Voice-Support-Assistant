import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
SAMPLE_RATE = 16000
AUDIO_FILE = "question.wav"
print(sd.query_devices())
def main():
    print("\n===================================")
    print("   TECKINFO AI VOICE ASSISTANT")
    print("===================================")
    print("Ask your support question by voice.")
    print("Press Ctrl+C to stop.\n")



    try:
        while True:
            print(sd.query_devices())
            print("Default devices:", sd.default.device)
            def record_audio():
                print("\n🎤 Speak your Teckinfo support question...")
                print("Recording will stop after silence.")

                silence_limit = 1.5
                threshold = 0.015
                chunk_duration = 0.1

            chunks = []
            silence_time = 0
            speech_detected = False

            with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32"
            ) as stream:

                while True:
                    chunk, overflowed = stream.read(
                    int(SAMPLE_RATE * chunk_duration)
                    )

                    chunks.append(chunk.copy())

                    volume = np.sqrt(np.mean(chunk ** 2))

                    if volume > threshold:
                        speech_detected = True
                        silence_time = 0
                    elif speech_detected:
                        silence_time += chunk_duration

                    if speech_detected and silence_time >= silence_limit:
                        break

                    audio = np.concatenate(chunks, axis=0).flatten()
                    audio_int16 = (audio * 32767).astype(np.int16)

                    write(AUDIO_FILE, SAMPLE_RATE, audio_int16)
                    print("Recording complete.")

                    if not question:
                        print("No speech detected. Please try again.")
                        continue

            # Exit if the recognized speech is "exit"
                    if question.lower().strip().rstrip(".!") == "exit":
                        print("Voice assistant closed.")
                        break

            # answer = get_voice_answer(question)
            # speak_answer(answer)

    except KeyboardInterrupt:
        print("\nVoice assistant stopped.")

    except Exception as error:
        print("\nError:", error)


if __name__ == "__main__":
    main()

