# # import streamlit as st
# # from youtube import youmain



import streamlit as st
import os
import joblib
import openai
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
def speech_to_text():
    st.title("Speech to Text")

    uploaded_file = st.file_uploader("Upload an audio file (WAV format recommended)", type=["wav", "mp3"])
    if uploaded_file:
        recognizer = sr.Recognizer()
        with sr.AudioFile(uploaded_file) as source:
            audio = recognizer.record(source)
            st.info("Transcribing...")
            try:
                text = recognizer.recognize_google(audio)
                st.success(f"Transcription: {text}")
            except sr.UnknownValueError:
                st.error("Could not understand the audio.")
            except sr.RequestError as e:
                st.error(f"Google API Error: {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")
 


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
openai.api_key = st.secrets.get("OPENAI_API_KEY", "")

def chatbots():
    st.title("AI Chatbot")
    user_input = st.text_input("Ask something:", "")

    if st.button("Send") and user_input:
        with st.spinner("Thinking..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",  # Or gpt-4 if available
                    messages=[
                        {"role": "user", "content": user_input}
                    ]
                )
                reply = response['choices'][0]['message']['content']
                st.success(reply)
            except Exception as e:
                st.error(f"❌ Error: {e}")

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

