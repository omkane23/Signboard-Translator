
# 📷 Smart Signboard Translator

An intelligent and interactive Streamlit web app that reads text from real-world signboard images, translates it into your preferred language, and speaks it out loud using text-to-speech.

---

## 🌟 Features

- 🖼️ **Upload Signboard Image**: Supports `.jpg`, `.jpeg`, and `.png` formats.
- 🧠 **Smart Text Detection**: Uses OpenCV and Tesseract OCR to extract text from signboard areas.
- 🌐 **Language Translation**: Supports translation to:
  - English (en)
  - Hindi (hi)
  - French (fr)
  - Spanish (es)
  - German (de)
  - Chinese (zh-cn)
- 🔊 **Text-to-Speech (TTS)**: Speaks out the translated message using gTTS.
- 📝 **Downloadable Output**:
  - Translated image with overlay
  - Text file containing original + translated text

---

## 🛠 Built With

- Python
- [Streamlit](https://streamlit.io/) – Web App Framework
- [OpenCV](https://opencv.org/) – Image Processing
- [Pytesseract](https://github.com/madmaze/pytesseract) – OCR Engine
- [Googletrans](https://pypi.org/project/googletrans/) – Translation API
- [gTTS](https://pypi.org/project/gTTS/) – Google Text-to-Speech
- [langdetect](https://pypi.org/project/langdetect/) – Language Detection
- [Pillow](https://pillow.readthedocs.io/) – Image Manipulation

---

## ⚙️ Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/smart-signboard-translator.git
cd smart-signboard-translator

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🖼 Example Output

- Translated overlay on image
- Spoken translation
- Text file download of extracted and translated text

---

## 📁 Project Structure

```
smart-signboard-translator/
├── app.py               # Main application script
├── README.md            # Documentation file
├── requirements.txt     # Python package dependencies
```

---

## 💡 Future Improvements

- Support multiple text regions and paragraphs
- Allow manual region selection
- Offline TTS support
- Real-time webcam mode

---

## 👨‍💻 Author

**Om** – Made with ❤️ using Python and Streamlit

---

## 📜 License

This project is licensed under the MIT License.
