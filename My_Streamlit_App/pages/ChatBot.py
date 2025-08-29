import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import tempfile
import speech_recognition as sr
from time import sleep
import io 
from pypdf import PdfReader


# --- Configuration ---
genai.configure(api_key="AIzaSyCMsDp3FuHKmotvGk8LQpK4rbQmtyH1jxw")
model = genai.GenerativeModel("gemini-2.0-flash")
st.set_page_config(page_title="Palébot Translator", layout="wide", page_icon="🇱🇨")

primaryColor = "#575fe8"


# --- Custom Styles ---
st.markdown("""
    <style>
    body {
        background-color: #E1F5FE;
        color: white;
    }
    .main-container {
        background: #0F0F0F;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 0 15px rgba(0,0,0,0.3);
    }
    .title {
        font-size: 40px;
        font-weight: 700;
        color: #f1c40f;
        text-align: center;
        margin-bottom: 1rem;
    }
    .chat-bubble {
        padding: 12px 18px;
        margin-bottom: 12px;
        border-radius: 12px;
        font-size: 16px;
        max-width: 80%;
    }
    .user {
        background-color: #0072C6;
        color: white;
        margin-left: auto;
        text-align: right;
    }
    .bot {
        background-color: #34495e;
        color: white;
        margin-right: auto;
        text-align: left;
    }
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Flag_of_Saint_Lucia.svg/640px-Flag_of_Saint_Lucia.svg.png", width=100)
    st.title("Palébot")
    st.markdown("🇱🇨 *Kwéyòl Translator Chatbot*")
    st.markdown("---")
    st.markdown("---")
    st.caption("Made with ❤️ in Saint Lucia.")
    
    
# --- Header ---
st.markdown('<div class="title">Palébot Translator 🇱🇨</div>', unsafe_allow_html=True)

# --- Chat Memory ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Input Box ---
user_input = st.chat_input("Type your message in English...")

#----PDF reader----
#uploaded_file = st.file_uploader("Upload a document for the chatbot", type=["pdf", "txt", "csv"])

#if uploaded_file is not None:
    # Process the uploaded file
    #if uploaded_file.type == "application/pdf":
      #  reader = PdfReader(uploaded_file)
     #   text = ""
    #    for page in reader.pages:
  #          text += page.extract_text()
      #  st.write("PDF content extracted. Chatbot can now use this information.")
            # Further steps: chunking, embedding, storing in vector database
   # elif uploaded_file.type == "text/plain":
       # text = uploaded_file.read().decode("utf-8")
       # st.write("Text file content extracted.")
            # Further steps: chunking, embedding, storing in vector database
        # ... handle other file types









# --- Translation Logic ---
def translate_with_gemini(text):
    prompt = f"Translate this English sentence into Saint Lucian Kwéyòl clearly and culturally Be in a clear explanitory tone Provide pronunciation: {text}.  \n"
   # reader = PdfReader("KweyolDictionary.pdf")
    #number_of_pages = len(reader.pages)
    #first_page = reader.pages[370]
    #text = first_page.extract_text()
    #prompt = text
    try:
        result = model.generate_content(prompt)
        return result.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# --- TTS Logic ---
#def generate_tts(text):
 #   tts = gTTS(text, lang="fr")
  #  with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
    #    tts.save(fp.name)
     #   return fp.name
def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        st.info("Listening.....")
        audio = recognizer.listen(source, timeout=5.0)

    try:
        text = recognizer.recognize_google(audio)
        st.session_state.messages.append(("user",text))
        reply = translate_with_gemini(text)
        st.session_state.messages.append(("bot", reply))
        st.success("You said: "+ text)
        return text
    except Exception as e:
        st.error("Could not understand")
        return ""
# --- Handle Chat ---

if user_input:
    st.session_state.messages.append(("user", user_input))
    reply = translate_with_gemini(user_input)
    st.session_state.messages.append(("bot", reply))
st.write("")
st.write("")

# --- Chat Display ---

chat_container = st.container()
with chat_container:
    for sender, msg in st.session_state.messages:
        bubble_class = "user" if sender == "user" else "bot"
        st.markdown(f"<div class='chat-bubble {bubble_class}'>{msg}</div>", unsafe_allow_html=True)
        if sender == "bot":
           # st.audio(generate_tts(msg))


# --- Expression of the Day ---
            st.markdown("----")
st.markdown("""🌟 **Expression of the Day:** *Tout bèt ni manjé yo.*  
> “Every animal has its own food — everyone has their own path.”""")

# --- Footer ---
st.markdown("""
<div style='text-align:center; font-size: 13px; color: lightgray; margin-top: 25px'>
Built by Team Gason Sent Lisi 2025 | National Innovation Challenge 🇱🇨
</div>
""", unsafe_allow_html=True)

if st.button("Speak In",help = "Speech to text"):
    transcribed = recognize_speech()
    st.session_state.input = transcribed
    
    st.rerun()
