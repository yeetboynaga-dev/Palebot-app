import streamlit as st
import google.generativeai as genai
import tempfile
import base64
import speech_recognition as sr
from time import sleep
import io 
from pypdf import PdfReader
from PIL import Image
import pyaudio
from gtts import gTTS

# Configure Gemini API key
genai.configure(api_key="AIzaSyCMsDp3FuHKmotvGk8LQpK4rbQmtyH1jxw")
model = genai.GenerativeModel("gemini-2.0-flash")

with st.sidebar:
    st.title("")
    image = Image.open("1000177253.png")
    new_width = 200
    new_height = 200
    resized_image = image.resize((new_width, new_height))
    st.image(resized_image)



st.set_page_config(page_title="Palébot Translator", layout="wide")

# Style
st.markdown("""
    <style>
    .block-container {padding-top: 2rem;}
    .title {text-align: center; font-size: 40px; font-weight: bold; color: #004d99;}
    .language-select {margin-top: 10px;}
    .button-row {text-align: center; margin-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

image2 = Image.open("Lucian flag.png")
new_width2 = 100
new_height2 = 75
resized_image2 = image2.resize((new_width2, new_height2))
st.image(resized_image2)


# Title
st.markdown(f'<div class="title">{image2}Palébot Translator</div>', unsafe_allow_html=True)

# Initialize session state defaults
if "source" not in st.session_state:
    st.session_state.source = "English"
if "target" not in st.session_state:
    st.session_state.target = "Kwéyòl"

# Handle swap button click BEFORE rendering widgets
if "swap_clicked" not in st.session_state:
    st.session_state.swap_clicked = False

if st.button("🔁 Swap"):
    st.session_state.source, st.session_state.target = st.session_state.target, st.session_state.source
    st.session_state.swap_clicked = True

# Now render language selectors
col1, col2, col3 = st.columns([3, 1, 3])

with col1:
    source_lang = st.selectbox("From:", ["English", "Kwéyòl"], key="source")
with col2:
    st.write("")  # Empty placeholder for layout alignment
with col3:
    target_lang = st.selectbox("To:", ["Kwéyòl", "English"], key="target")

# Input/Output Text Areas
input_col, output_col = st.columns(2)
with input_col:
    user_input = st.text_area("Enter Text", height=200)
with output_col:
    output_box = st.empty()

# Translator function
def translate_with_gemini(text, src, tgt):
    prompt = f"Translate the following {src} sentence into {tgt}, keeping cultural clarity: Give Direct translation to the given statement, phrase or text do not unnecessary information to the response \n\n'{text}'"
    try:
        result = model.generate_content(prompt)
        return result.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# TTS
def generate_tts(text, lang_code="en"):
    tts = gTTS(text, lang=lang_code)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        return fp.name

# Get language code for TTS
def lang_code(lang):
    return "fr" if lang == "Kwéyòl" else "en"

# Translation Button
if st.button("Translate ✨"):
    if user_input.strip() == "":
        st.warning("Please enter some text.")
    else:
        translated_text = translate_with_gemini(user_input, source_lang, target_lang)
        output_box.text_area("Translation", value=translated_text, height=200, disabled=True)

        # TTS Audio
        audio_path = generate_tts(translated_text, lang_code(target_lang))
        st.audio(audio_path)

        # Copy Button (optional for web)
        b64 = base64.b64encode(translated_text.encode()).decode()
        st.markdown(
            f'<a href="data:text/plain;base64,{b64}" download="translation.txt">'
            f'<button style="margin-top:10px">📄 Download Translation</button></a>',
            unsafe_allow_html=True
        )

st.markdown("""---""")
# Footer
st.markdown("""
<div style='text-align:center; font-size: 14px; color: white; margin-top: 20px'>
Built with ❤ by Team Gason Sent Lisi 2025 🇱🇨
</div>
""", unsafe_allow_html=True)

