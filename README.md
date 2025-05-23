# 📄 Ask Your PDF — Powered by GROQ LLM

Ask Your PDF is a smart and lightweight Streamlit-based app that lets you upload any PDF and ask questions about its content in real-time using GROQ's blazing-fast large language models (LLMs).

![Streamlit](https://img.shields.io/badge/Built%20With-Streamlit-red?style=flat-square&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)
![LLM](https://img.shields.io/badge/Powered%20By-GROQ%20LLM-black?style=flat-square&logo=data)

---

## 🚀 Features

- 🔍 Upload any PDF and interactively query its contents
- 🤖 Uses GROQ LLM (Meta LLaMA 4) for intelligent, lightning-fast responses
- 💬 Maintains chat history with timestamps
- 🧠 Context-aware answers within 16,000 tokens
- 💾 Download chat logs as `.json`, `.txt`, or `.pdf` (coming soon)
- 🎨 Minimal, intuitive Streamlit UI

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Varun-Wagle/ask-your-pdf.git
cd ask-your-pdf

# 2. Set Up a Virtual Environment (optional but recommended)
python -m venv venv
venv\Scripts\activate   # On Windows

# 3. Install Requirements
pip install -r requirements.txt

# 4. Create a .env File
GROQ_API_KEY=your_groq_api_key_here
 
# ▶️ Run the App
streamlit run app1.py

# 🛠️ Built With
Streamlit
GROQ API
PyPDF2
Python-dotenv
Requests

📚 Example Usage
1. Upload a PDF file using the sidebar

2. Ask a natural-language question like:
  • "What is the summary of Chapter 3?"
  • "Who is the author and what are their main findings?"

3. Get context-aware answers from the AI

📂 Project Structure
bash
Copy
Edit
ask-your-pdf/
│
├── app1.py                # Main Streamlit app
├── requirements.txt       # Python dependencies
├── .env                   # Contains your GROQ API key (excluded from Git)
├── .gitignore             # Prevents committing sensitive/unnecessary files
└── README.md              # You're reading it!

📄 License
This project is licensed under the MIT License.

🤝 Contributions
Contributions, issues and feature requests are welcome!
Feel free to ⭐️ the repo and open an issue.

✨ Author
Varun Wagle
GitHub
