import fitz  # PyMuPDF
from dotenv import load_dotenv
import os
import time
import tempfile
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI


st.set_page_config(page_title="Chat with Applicant's Docs", layout="wide")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Welcome! Pls upload any document of the Loan Applicant to get started."}]

if "initial" not in st.session_state:
    st.session_state.initial = False

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

def stream_data(str):
        for word in str.split(" "):
            yield word + " "
            time.sleep(0.1)

# Configure the API Key
load_dotenv()
api_key = os.environ["GOOGLE_API_KEY"]

chat_model = ChatGoogleGenerativeAI(
    model="models/gemini-2.0-flash-001",
    temperature=0.2,
    google_api_key=api_key,
   )


def ask_gemini(question, context: str = ""):

    if not st.session_state.initial:

        st.session_state.messages.append({"role": "user", "content": f'''Act as an experienced banker specializing in information verification. Carefully analyze the provided context
        and respond strictly based on the question asked.
        Give the answer in table if you think it will be helpful for the user.
        Now, analyze the context and provide an answer that is precise, relevant, and strictly within the scope of the question.

        Context: {context}
        Question: {question}

        Respond in a friendly yet professional tone, ensuring clarity and ease of understanding. Keep your response concise and to the point,
        answering only what is asked without adding unnecessary details.
        '''})

        st.session_state.initial = True
        
    response = chat_model.invoke(st.session_state.messages[1:])
    print(response)
    return response.content
    

st.title("Chat with Applicant's Docs")

for msg in st.session_state.messages:
    if not msg["content"].startswith("Act as an experienced"):
        st.chat_message(msg["role"]).write(msg["content"])


# File Upload
uploaded_file = st.sidebar.file_uploader("Upload a KYC Document (PDF)", type=["pdf"])

if uploaded_file :

    with st.spinner("Uploading PDF & Processing..."):
        
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_pdf_path = temp_file.name

        # Extract text from the PDF
        st.session_state.pdf_text = extract_text_from_pdf(temp_pdf_path)

    st.sidebar.success("PDF Uploaded & Processed Successfully!")

# Display the extracted text
if prompt := st.chat_input(disabled=not uploaded_file):

    if not uploaded_file:
        st.info("Please upload a KYC doc to continue.")
        st.stop()

    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        
        with st.spinner("Generating Response..."):
            response = ask_gemini(prompt, st.session_state.pdf_text)
        
        st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        

