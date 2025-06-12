import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pytesseract
from googletrans import Translator
from gtts import gTTS
from langdetect import detect
import tempfile
import os
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # For Linux

# Streamlit page config
st.set_page_config(page_title="Smart Signboard Translator", page_icon="📷", layout="centered")
st.title("📷 Smart Signboard Translator")
st.caption("Upload any signboard image to extract, translate, and speak out the message!")

# Upload image
uploaded_file = st.file_uploader("Upload a Signboard Image", type=["jpg", "jpeg", "png"])

# Target language selection
target_language = st.selectbox(
    "Select Target Language for Translation",
    options=["en", "hi", "fr", "es", "de", "zh-cn"],
    format_func=lambda x: {
        "en": "English", "hi": "Hindi", "fr": "French", 
        "es": "Spanish", "de": "German", "zh-cn": "Chinese"
    }[x]
)

translator = Translator()

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.medianBlur(gray, 3)
    return blurred

def get_text_region(image):
    # Convert to grayscale and threshold
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshed = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    
    contours, _ = cv2.findContours(threshed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Assume largest contour with text
    largest_contour = max(contours, key=cv2.contourArea) if contours else None
    if largest_contour is not None:
        x, y, w, h = cv2.boundingRect(largest_contour)
        cropped = image[y:y+h, x:x+w]
        return cropped, (x, y)
    else:
        return image, (30, 50)

def speak_text(text, lang_code):
    tts = gTTS(text=text, lang=lang_code)
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_audio.name)
    return temp_audio.name

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image_np = np.array(image)

    st.image(image_np, caption="Uploaded Image", use_column_width=True)

    with st.spinner("Processing image..."):
        cropped_img, position = get_text_region(image_np)
        preprocessed_img = preprocess_image(cropped_img)

        # OCR
        extracted_text = pytesseract.image_to_string(preprocessed_img)

        if not extracted_text.strip():
            st.warning("No text detected. Try with another image.")
            st.stop()

        # Language Detection
        try:
            detected_lang = detect(extracted_text)
        except:
            detected_lang = "unknown"

        st.subheader("📝 Extracted Text")
        st.code(extracted_text)

        st.markdown(f"**Detected Language:** `{detected_lang.upper()}`")

        # Translate
        translated = translator.translate(extracted_text, dest=target_language)
        translated_text = translated.text

        st.subheader("🌐 Translated Text")
        st.success(translated_text)

        # Overlay on image
        overlay_img = image_np.copy()
        x, y = position
        cv2.putText(overlay_img, translated_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255), 2)

        st.image(overlay_img, caption="📌 Translated Signboard", use_column_width=True)

        # Text-to-speech
        st.subheader("🔊 Listen to Translation")
        audio_path = speak_text(translated_text, target_language)
        st.audio(audio_path, format='audio/mp3')

        # Download translated image
        result_img = Image.fromarray(overlay_img)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_img:
            result_img.save(tmp_img.name)
            st.download_button("📥 Download Translated Image", data=open(tmp_img.name, 'rb'),
                               file_name="translated_signboard.png", mime="image/png")

        # Download text
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w') as txt_file:
            txt_file.write(f"Extracted: {extracted_text}\nTranslated: {translated_text}")
            st.download_button("📄 Download Extracted + Translated Text",
                               data=open(txt_file.name, 'rb'),
                               file_name="translation.txt", mime="text/plain")
else:
    st.info("Upload an image to begin.")

