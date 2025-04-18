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
from mcq import cqmain
import random
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from heapq import nlargest
import fitz
from streamlit_mic_recorder import mic_recorder
import io

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
    st.title("Speech-to-Text Converter")

    # Record audio from the microphone
    audio_data = mic_recorder(start_prompt="Start Recording", stop_prompt="Stop Recording")

    if audio_data:
        st.audio(audio_data['bytes'], format='audio/wav')

        # Initialize the recognizer
        recognizer = sr.Recognizer()

        # Use the recorded audio data for transcription
        with sr.AudioFile(io.BytesIO(audio_data['bytes'])) as source:
            audio = recognizer.record(source)

        try:
            # Transcribe the audio using Google's speech recognition
            transcription = recognizer.recognize_google(audio)
            st.write("Transcribed Text:")
            st.success(transcription)
        except sr.UnknownValueError:
            st.error("Could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"Could not request results; {e}")
 


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

# ----------------- MCQ -----------------
def mcq_generator():
    st.title("MCQ Generator")
    input_text = st.text_area("Enter educational content:", height=300)
    if st.button("Generate MCQs"):
        if input_text.strip():
            sentences = sent_tokenize(input_text)
            words = word_tokenize(input_text.lower())
            stop_words = set(stopwords.words("english"))
            word_freq = {}
            for word in words:
                if word.isalpha() and word not in stop_words:
                    word_freq[word] = word_freq.get(word, 0) + 1
            keywords = nlargest(5, word_freq, key=word_freq.get)
            
            st.subheader("Generated Questions:")
            for i, keyword in enumerate(keywords):
                for sent in sentences:
                    if keyword in sent.lower():
                        question = sent.replace(keyword, "______")
                        st.markdown(f"**Q{i+1}:** {question}")
                        options = random.sample(keywords, 3)
                        if keyword not in options:
                            options[random.randint(0, 2)] = keyword
                        random.shuffle(options)
                        for idx, opt in enumerate(options):
                            st.markdown(f"- {chr(65+idx)}. {opt}")
                        break
        else:
            st.warning("Please enter some text to generate MCQs.")
#------------------- FILE COMPRESE---------
def idea_file_compress():
    st.title("Idea & File Compression (PDF Summarizer)")
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded_file is not None:
        try:
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            if text:
                summarized = summarize_text(text)
                st.subheader("Summarized Content:")
                st.text_area("Summary", summarized, height=300)
            else:
                st.warning("No readable text found in PDF.")
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
#----summarize text---
def summarize_text(text, max_sentences=5):
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words("english"))
    word_freq = {}
    for word in words:
        if word.isalpha() and word not in stop_words:
            word_freq[word] = word_freq.get(word, 0) + 1
    sentence_scores = {}
    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in word_freq:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + word_freq[word]
    summary = nlargest(max_sentences, sentence_scores, key=sentence_scores.get)
    return " ".join(summary)

#----hate speech------
def hate_speech_checker():
    st.title("Hate Speech Detection")
    user_input = st.text_area("Enter text to check:", height=150)
    if st.button("Analyze Text"):
        if not user_input.strip():
            st.warning("Please enter some text.")
            return
        try:
            model = joblib.load("hate_speech_model.pkl")
            vectorizer = joblib.load("tfidf_vectorizer.pkl")

            vectorized = vectorizer.transform([user_input])
            prediction = model.predict(vectorized)
            prob = model.predict_proba(vectorized)[0]

            if prediction[0] == 1:
                st.error(f"⚠️ Hate Speech Detected (Confidence: {prob[1]*100:.2f}%)")
            else:
                st.success(f"✅ No Hate Speech Detected (Confidence: {prob[0]*100:.2f}%)")

        except FileNotFoundError:
            st.error("❌ Model or vectorizer file not found. Please upload 'hate_speech_model.pkl' and 'tfidf_vectorizer.pkl'.")
        except Exception as e:
            st.error(f"🔧 Error during analysis: {e}")


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
        chatbots()
    elif selection == "Idea-File-Compress":
        idea_file_compress()
    elif selection == "MCQ":
        mcq_generator()
    elif selection == "Hate Speech Detection":
        hate_speech_checker()

if __name__ == "__main__":
    main()

