import streamlit as st
import urllib.parse

# Path to the PDF file inside the app folder
pdf_path = "KweyolDictionary.pdf"

# Encode spaces or special characters if needed
encoded_pdf_path = urllib.parse.quote(pdf_path)

# Create a clickable Markdown link
st.markdown(
    f"[📘 Click here to open the Lucian Kwéyòl Dictionary]({encoded_pdf_path})"
)
