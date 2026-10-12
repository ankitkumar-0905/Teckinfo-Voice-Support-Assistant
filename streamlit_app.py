
import streamlit as st
from api.api_client import ask_rag
from voice.tts import speak_answer
from api.start_api import ensure_api_running
from ui.login import show_login
from ui.admin import show_admin_dashboard
from ui.user import show_user_dashboard

st.set_page_config(
    page_title="Teckinfo AI Support Assistant",
    page_icon="🎧",
    layout="centered"
)
# Initialize login session
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Show login page if user is not logged in
if not st.session_state["authenticated"]:
    show_login()
    st.stop()

# Get logged-in user
user = st.session_state.get("user")

if not user:
    st.session_state["authenticated"] = False
    st.rerun()

# Sidebar user information
st.sidebar.write(f"Logged in: {user['username']}")
st.sidebar.caption(f"Role: {user['role']}")


# Admin dashboard
if user["role"] == "admin":
    show_admin_dashboard(user)
    st.stop()

# User dashboard
elif user["role"] == "user":
    show_user_dashboard(user)

else:
    st.error("Invalid user role.")
    st.stop()
try:
    ensure_api_running()
except Exception as error:
    st.error(f"Backend not started : {error}")
    st.stop()


# Login status initialize karo
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Agar user login nahi hai, to login page dikhao
if not st.session_state["authenticated"]:
    show_login()
    st.stop()

# Logged-in user ki details lo
user = st.session_state.get("user")

# Safety check: user details missing hain to logout
if not user:
    st.session_state["authenticated"] = False
    st.rerun()

# Role ke hisaab se dashboard dikhao
if user["role"] == "admin":
    show_admin_dashboard(user)
    st.stop()

elif user["role"] == "user":
    show_user_dashboard(user)



else:
    st.error("Invalid user role. Please contact administrator.")
    st.session_state["authenticated"] = False
    st.stop()


# Sidebar mein logged-in user ki details
st.sidebar.write(f"Logged in: {user['username']}")
st.sidebar.caption(f"Role: {user['role']}")

# Logout button
if st.sidebar.button("🚪 Logout", key="main_logout_button"):
    st.session_state["authenticated"] = False
    st.session_state.pop("user", None)
    st.session_state.pop("chat_history", None)
    st.session_state.pop("voice_history", None)
    st.rerun()


st.title("🎧 Teckinfo AI Support Assistant")
st.caption("AI-powered technical support using RAG + Groq")

mode = st.sidebar.radio(
    "Choose Assistant",
    ["Chat Bot", "Voice Bot"]
)


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "voice_history" not in st.session_state:
    st.session_state.voice_history = []


if mode == "Chat Bot":
    st.subheader("💬 Chat Support")

    for i, message in enumerate(st.session_state.chat_history):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message["role"] == "assistant":
                if st.button("🔊 Listen", key=f"listen_{i}"):
                    with st.spinner("Speaking..."):
                        speak_answer(message["content"])

    question = st.chat_input("Ask your Teckinfo support question...")

    if question:
        st.session_state.chat_history.append({
            "role": "user",
            "content": question
        })

        with st.spinner("Finding the answer..."):
            try:
                answer = ask_rag(question)
            except Exception as error:
                answer = f"Could not get an answer: {error}"

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer
        })

        st.rerun()



elif mode == "Voice Bot":
    st.subheader("🎙️ Voice Support")
    st.write("Click below and ask your question by speaking.")

    # Show previous questions and answers first
    for i, item in enumerate(st.session_state.voice_history):
        with st.chat_message("user"):
            st.write(item["question"])

        with st.chat_message("assistant"):
            st.markdown(item["answer"])

            if st.button("🔊 Listen again", key=f"voice_listen_{i}"):
                speak_answer(item["answer"])

    # Keep Start Recording at the bottom
    if st.button("🎙️ Start Recording", type="primary", use_container_width=True):
        try:
            from stt import record_audio, transcribe_audio

            with st.spinner("Listening to your question..."):
                audio_path = record_audio()

            if audio_path:
                question = transcribe_audio(audio_path)

                if question:
                    with st.chat_message("user"):
                        st.write(question)

                    with st.spinner("Getting the answer..."):
                        answer = ask_rag(question)

                    st.session_state.voice_history.append({
                        "question": question,
                        "answer": answer
                    })

                    with st.chat_message("assistant"):
                        st.markdown(answer)

                    speak_answer(answer)
                    st.rerun()
                else:
                    st.warning("Speech was not recognized. Please try again.")
            else:
                st.warning("No speech detected. Please try again.")

        except Exception as error:
            st.error(f"Voice Bot Error: {error}")
