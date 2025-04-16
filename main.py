# # import streamlit as st
# # from youtube import youmain



import streamlit as st
import os
import joblib
from gtts import gTTS
from youtube_transcript_api import YouTubeTranscriptApi
import speech_recognition as sr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from pydub import AudioSegment
import tempfile
# ----------------- PAGE CONFIG -----------------
st.set_page_config(page_title="Smart Learning AI", layout="wide")

# ----------------- ABOUT PAGE -----------------
def about():
    st.title("Welcome to Smart Learning GEN AI")
    st.subheader("Your Personalized Tutor")
    st.markdown("""
        #### Empowering Education with Artificial Intelligence

        Welcome to our AI-EdTech, your ultimate learning companion! Our platform combines the power of artificial intelligence with education to provide you with a personalized and engaging learning experience.

        #### Features:
        - 📚 **Smart Content**
        - 🔍 **Personalized Learning**
        - 📹 **Video Summarization**
        - 🔊 **Text-to-Speech & Speech-to-Text**
        - 💬 **Chatbot Assistant**
        - ❓ **MCQ Generator**
        - 🚫 **Hate Speech Detection**
    """)
    st.markdown("***")

# ----------------- TEXT TO SPEECH -----------------
def text_to_speech():
    st.title("Text to Speech Converter")
    input_text = st.text_area("Enter text here:", height=150)
    if st.button("Convert to Speech"):
        if input_text.strip():
            tts = gTTS(text=input_text, lang='en')
            tts.save("output.mp3")
            st.audio("output.mp3", format="audio/mp3")
        else:
            st.warning("Please enter some text.")

# ----------------- SPEECH TO TEXT -----------------
import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import tempfile

def speech_to_text():
    st.title("Speech to Text")
    st.markdown("Upload a WAV/MP3 audio file and get it transcribed.")

    uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "flac", "ogg"])

    if uploaded_file:
        try:
            # Save uploaded file temporarily
            temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            
            # Convert to WAV using pydub
            audio = AudioSegment.from_file(uploaded_file)
            audio.export(temp_audio.name, format="wav")

            # Transcribe using SpeechRecognition
            recognizer = sr.Recognizer()
            with sr.AudioFile(temp_audio.name) as source:
                st.info("Processing and transcribing...")
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
                st.success("Transcription:")
                st.write(text)

        except Exception as e:
            st.error(f"❌ Error: {e}")


# ----------------- YOUTUBE TRANSCRIPT -----------------
def youtube_transcript():
    st.title("YouTube Transcript Viewer")
    video_id = st.text_input("Enter YouTube Video ID:")
    if st.button("Get Transcript"):
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            full_text = "\n".join([x['text'] for x in transcript])
            st.text_area("Transcript", full_text, height=300)
        except Exception as e:
            st.error(f"Error: {str(e)}")

# ----------------- HATE SPEECH DETECTION -----------------
def hate_speech_checker():
    st.title("Hate Speech Detection")
    user_input = st.text_area("Enter text to check:", height=150)
    if st.button("Analyze Text"):
        try:
            model = joblib.load("hate_speech_model.pkl")
            vectorizer = joblib.load("tfidf_vectorizer.pkl")
            vectorized = vectorizer.transform([user_input])
            prediction = model.predict(vectorized)
            if prediction[0] == 1:
                st.error("⚠️ This text contains hate speech.")
            else:
                st.success("✅ No hate speech detected.")
        except Exception as e:
            st.error(f"Model Error: {e}")

# ----------------- PLACEHOLDER FOR OTHER FUNCTIONS -----------------
def chatbot_ui():
    st.title("Unlimited AI Chatbot")
    st.info("🔧 Chatbot functionality placeholder (LLM API needed).")

def idea_file_compress():
    st.title("Idea & File Compression")
    st.info("🔧 PDF summarizer placeholder.")

def mcq_generator():
    st.title("MCQ Generator")
    st.info("🔧 MCQ generation logic placeholder.")

# ----------------- MAIN APP -----------------
def main():
    st.sidebar.title("SMART LEARNING AI")
    selection = st.sidebar.selectbox(
        "Choose a Feature",
        [
            "About",
            "Text to Speech",
            "Speech to Text",
            "YouTube Transcript",
            "Unlimited Chatbot",
            "Idea-File-Compress",
            "MCQ",
            "Hate Speech Detection"
        ]
    )

    if selection == "About":
        about()
    elif selection == "Text to Speech":
        text_to_speech()
    elif selection == "Speech to Text":
        speech_to_text()
    elif selection == "YouTube Transcript":
        youtube_transcript()
    elif selection == "Unlimited Chatbot":
        chatbot_ui()
    elif selection == "Idea-File-Compress":
        idea_file_compress()
    elif selection == "MCQ":
        mcq_generator()
    elif selection == "Hate Speech Detection":
        hate_speech_checker()

if __name__ == "__main__":
    main()

