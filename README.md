# The Equalizer AI (FairPlay AI)

An AI-powered rights advocate designed to democratize legal and bureaucratic assistance. The Equalizer interprets complex legalese, identifies risks, and helps users take formal action.

## 🚀 Features
- **Risk Detector**: Upload documents (PDF/Images/Text) to identify high, medium, and low-level risks.
- **Simplifier**: Translates complex legalese into clear, 5th-grade level summaries.
- **Action Engine**: Generates formal appeals, contest letters, and legal documents.
- **Multilingual Support**: Advice provided in multiple languages.

---

## 🛠️ Setup & Installation

### 1. Prerequisites
- **Python 3.9+**
- **Google Gemini API Key** (Get it from [Google AI Studio](https://aistudio.google.com/))

### 2. Clone the Repository
```bash
git clone https://github.com/msraghavendra/The-Equalizer-AI.git
cd The-Equalizer-AI
```

### 3. Create a Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 4. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Create a `.env` file in the root directory and add your API key:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

---

## 🏃 How to Run

To start the local development server:
```powershell
uvicorn app.main:app --port 8000 --reload
```

Once the server is running, open your browser and navigate to:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 📂 Project Structure
- `app/main.py`: The entry point of the FastAPI application.
- `app/core/`: Brain of the AI (Risk Detector, Simplifier, Action Engine).
- `app/static/`: Frontend files (HTML, CSS, JS).
- `app/templates/`: Legal document templates used by the Action Engine.
- `app/compliance/`: Tools for PII redaction and data privacy.

---

## 📜 Disclaimer
*This tool is designed for educational and informational purposes only. It does not provide legal advice. Always consult with a qualified legal professional for serious matters.*
