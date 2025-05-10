# Chat with Applicant's Docs

A Streamlit app that allows you to chat with PDF documents (such as loan applicant KYC files) using Google's Gemini AI via LangChain.

Features:

* Upload PDF documents (e.g., KYC, loan forms)
* Ask natural language questions about the document
* Get intelligent, context-aware responses from Gemini Pro Flash
* Answers can be formatted in tables for clarity
* Friendly and professional response tone

Tech Stack:

* Python
* Streamlit
* PyMuPDF (fitz)
* LangChain with Google Gemini
* python-dotenv for environment management

Setup Instructions:

1. Clone the repository
2. (Optional) Create and activate a virtual environment
3. Install dependencies:
   pip install -r requirements.txt
4. Create a .env file in the root folder and add your API key:
   GOOGLE\_API\_KEY=your\_google\_api\_key\_here
5. Run the app:
   streamlit run app.py

Usage:

* Use the sidebar to upload a PDF document (only PDFs are supported)
* Once uploaded, ask any question based on the document content
* The AI will analyze the document and provide a relevant, clear answer

Prompt Behavior:
The app sets up the AI with a prompt to act like a skilled banker, responding concisely and only from the document context. It will present information in tables when helpful.


