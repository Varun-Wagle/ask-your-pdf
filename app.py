import streamlit as st
from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv
import requests
from datetime import datetime
import json
import io
from reportlab.pdfgen import canvas

#Load API Key from .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print("Loaded API key:", GROQ_API_KEY[:6], "..." if GROQ_API_KEY else "❌ Not Loaded")

#Function to extract text from PDF
def extract_pdf_text(pdf_file):
    pdf = PdfReader(pdf_file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text() or ""
    return text

#Function to ask GROQ LLM
def ask_groq(question, context):
    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",  # OR use a direct key here for testing
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",  # You can change to gemma-7b-it or others
        "messages": [
            {"role": "system", "content": "You are a helpful assistant. Answer based on the provided context."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
        ]
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.text}"
    
#Streamlit UI
st.title("📄Ask your PDF(GROQ Edition)")
st.write("Upload a PDF and ask any questions about its content.")

#Initialize Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

#Display Chat History in a collapsible box
with st.expander("📜Chat History (Click to expand)", expanded=False):
    for chat in st.session_state.chat_history:
        timestamp = chat["timestamp"]
        role = chat["role"]
        message = chat["message"]

        if role == "user":
            st.markdown(f"""
                        <div style="background-color:e1f5fe; padding:10px; border-radius:8px; margin-bottom:5px;")
                        🧑‍💬<b>You</b> <small style="color:gray;"({timestamp})</small><br>{message}
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                        <div style="background-color:e8f5e9; padding:10px; border-radius:8px; margin-bottom:5px;")
                        🤖<b>GroqMate</b> <small style="colo`r:gray;"({timestamp})</small><br>{message}
                        </div>
                    """, unsafe_allow_html=True)
    
    #Clear chat History
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()
    
    #Download chat log buttons
    def generate_text():
        return "\n\n".join([f"[{c['timestamp']}] {c['role'].capitalize()}: {c['message']}" for c in st.session_state.chat_history])
    
    def generate_json():
        return json.dumps(st.session_state.chat_history, indent=2)
    
    def generate_pdf():
        buf = io.BytesIO()
        c = canvas.Canvas(buf)
        text_obj = c.beginText(40, 800)
        text_obj.setFont("Helvetica", 10)
        for item in st.session_state.chat_history:
            text_obj.textLine(f"[{item['timestamp']}] {item['role'].capitalize()}: {item['message']}")
        c.drawText(text_obj)
        c.showPage()
        c.save()
        buf.seek(0)
        return buf
    st.download_button("⬇Download .txt", generate_text(), file_name="chat_history.txt")
    st.download_button("⬇Download .json", generate_json(), file_name="chat_history.json")

    try:
        st.download_button("⬇Download .pdf", generate_pdf(), file_name="chat_history.pdf")
    except Exception as e:
        st.warning("Install reportlab for PDF export: 'pip install reportlab'")

if "context_text" not in st.session_state:
    st.session_state.context_text = ""

#Upload the PDF
pdf_file = st.file_uploader("Upload your PDF File", type=["pdf"])

if pdf_file:
    with st.spinner("Reading PDF..."):
        context_text = extract_pdf_text(pdf_file)
        st.success("PDF uploaded and processed successfully!")

    #Once PDF is loaded, allow users to ask questions
    question = st.text_input("Ask a question about the PDF:")

    if question:
        with st.spinner("Thinking..."):
            answer = ask_groq(question, context_text[:16000]) #Trimmed to avoid token overload 
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.chat_history.append({"role": "user", "message": question, "timestamp": timestamp})
        st.session_state.chat_history.append({"role": "assistant", "message": answer, "timestamp": timestamp})

        st.markdown("**Answer:**")
        st.write(answer)
else:
    st.warning("Please upload a PDF to begin.")