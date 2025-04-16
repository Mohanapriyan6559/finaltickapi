import streamlit as st
from gtts import gTTS
import os

def speech():
    st.title("Text to Speech Converter")
    st.image("https://miro.medium.com/v2/resize:fit:1100/format:webp/0*PIm4S-fLsefifYAg.jpeg")

    input_text = st.text_area("Enter your text", height=200)

    if st.button("Convert to Speech"):
        if input_text:
            tts = gTTS(text=input_text, lang='en')
            tts.save("output.mp3")
            st.success("Text converted to speech!")
            st.audio("output.mp3", format="audio/mp3")
        else:
            st.warning("Please enter some text to convert.")

if __name__ == "__main__":
    speech()
