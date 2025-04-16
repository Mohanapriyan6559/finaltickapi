# # import streamlit as st
# # from youtube import youmain
# # from front import fmain
# # from speechtovoice import speech
# # from mcq import cqmain
# # from bad import bads

# #################111111111##########################
# client = Client()

# # Function for the Llama3.2 Chatbot
# # def chatbots():
# #     st.subheader("Tick-pick-AI Chat Interface")
# #     user_message = st.text_input("Enter your message:", "")

# #     if st.button("Send"):
# #         if user_message:
# #             # Display loading message
# #             with st.spinner("Tick-pic-AI is thinking..."):
# #                 try:
# #                     # Format input as a list of message objects
# #                     messages = [{"role": "user", "content": user_message}]
                    
# #                     # Stream responses
# #                     response = client.chat(
# #                         model="llama3.2",  # Specify the model name
# #                         messages=messages,  # Corrected to 'messages'
# #                         stream=True  # Enable streaming
# #                     )
                    
# #                     # Initialize response_text to collect output
# #                     response_text = ""
                    
# #                     # Placeholder for progressive updates
# #                     text_placeholder = st.empty()

# #                     for chunk in response:
# #                         # Check if the chunk contains a message with content
# #                         if chunk.message and chunk.message.content:
# #                             response_text += chunk.message.content
# #                             text_placeholder.text(response_text)  # Update text progressively
# #                         else:
# #                             st.write("No content in this chunk.")  # Debugging
                        
# #                     # Final display of the complete response
# #                     if response_text:
# #                         st.success("Response received!")
# #                     else:
# #                         st.warning("The model did not generate any content.")
# #                 except Exception as e:
# #                     st.error(f"An error occurred: {e}")
# #         else:
# #             st.warning("Please enter a message before sending.")










# #####################################################################################################################
# import speech_recognition as sr

# def transcribes():
#     """Record and transcribe audio from the microphone."""
#     recognizer = sr.Recognizer()
#     try:
#         with sr.Microphone() as source:
#             st.info("Adjusting for ambient noise... Please wait.")
#             recognizer.adjust_for_ambient_noise(source, duration=1)
#             st.info("Listening... Speak now!")
#             # Listen for the audio input
#             audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=500)
#             st.success("Recording complete. Transcribing...")
#             # Transcribe using Google's Speech Recognition API
#             text = recognizer.recognize_google(audio_data)
#             return text
#     except sr.WaitTimeoutError:
#         st.error("No speech detected. Please try again.")
#     except sr.UnknownValueError:
#         st.error("Speech was not clear enough. Could not transcribe.")
#     except sr.RequestError as e:
#         st.error(f"Error connecting to the Speech-to-Text service: {e}")
#     except Exception as e:
#         st.error(f"An unexpected error occurred: {e}")
#     return None

# def speech_to_text_ui():
#     """UI for Speech-to-Text functionality."""
#     st.title("Speech to Text")
#     st.markdown("Click the button below and start speaking. Your speech will be transcribed into text.")

#     if st.button("Start Recording"):
#         st.info("Preparing to record...")
#         with st.spinner("Recording..."):
#             transcription = transcribes()
#         if transcription:
#             st.write("**Transcription:**")
#             st.success(transcription)
#         else:
#             st.warning("No transcription available. Try again.")
# ##############################################################################################################################3

# def main():
#     st.title("SMART LERANING AI")
#     st.subheader("Your Personalized Tutor")

#     # Sidebar for app selection
#     st.sidebar.title("Navigation")
#     app_selection = st.sidebar.selectbox(
#         "Select Service",
#         [
#             "About",
#             "Unlimited Chatbot",
#             "Text to Speech",
#             "Speech-to-Text",
#             "Youtube-Text",
#             "Idea-File-Compress",
#             "MCQ",
#             "HATE SPEECH"
            
            
            
#         ]
#     )

#     # Display selected functionality
#     if app_selection == "About":
#         fmain()
#     elif app_selection == "Text-Shorty":
#         spmain()
#     elif app_selection == "Youtube-Text":
#         youmain()
#     elif app_selection == "Idea-File-Compress":
#         pdfsummerizermain()
#     elif app_selection == "Text to Speech":
#         speech()
#     elif app_selection == "Speech-to-Text":
#         speech_to_text_ui()
#     elif app_selection == "Unlimited Chatbot":
#         chatbots() 
#     elif app_selection=="MCQ":
#         cqmain()
#     elif app_selection=="HATE SPEECH":
#         bads()



# if __name__ == "__main__":
#     main()


import streamlit as st
import os
import joblib
from gtts import gTTS
from youtube_transcript_api import YouTubeTranscriptApi
import speech_recognition as sr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

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
    if st.button("Start Recording"):
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                st.info("Listening...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                st.success("Transcribing...")
                text = recognizer.recognize_google(audio)
                st.success(f"Transcription: {text}")
        except sr.WaitTimeoutError:
            st.error("Timeout: No speech detected.")
        except sr.UnknownValueError:
            st.error("Could not understand the speech.")
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

