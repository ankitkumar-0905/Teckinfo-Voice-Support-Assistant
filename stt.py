import whisper

model = whisper.load_model("base")

result = model.transcribe("audio.wav")

print("\nTranscribed Text:")
print(result["text"])


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

