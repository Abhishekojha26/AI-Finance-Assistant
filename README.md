💰 AI Finance Assistant

An AI-powered personal finance application built with Gemini,LangGraph, RAG, ChromaDB, Pandas, and Streamlit.

🚀 Live Demo

Open AI FinanceAssistant

The live demo may be affected by Gemini API quota limits.

✨ Features

🤖 AI Finance Chat --- Ask general personal-finance questionsand get AI-powered educational guidance.

📊 Financial Data Analyzer --- Upload CSV transaction data andanalyze spending, totals, transactions, missing values, andcategories.

📄 PDF Finance Assistant --- Upload and work with financial PDFdocuments.

🔎 RAG Document Q&A --- Retrieve relevant information fromuploaded financial documents before generating answers.

🧠 LangGraph AI Finance Agent --- Routes questions to CSV,PDF/RAG, or GENERAL tools.

💬 Conversation Memory --- Keeps recent agent conversationsavailable for follow-up questions.

🏗️ Architecture

                    User
                      │
                      ▼
             Streamlit Interface
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
      AI Chat      CSV Data     PDF / RAG
                     │             │
                   Pandas       ChromaDB
          └───────────┼─────────────┘
                      ▼
               LangGraph Agent
                      │
                      ▼
             Gemini Intent Router
              ┌───────┼────────┐
              ▼       ▼        ▼
             CSV     PDF     GENERAL
              └───────┼────────┘
                      ▼
                   Gemini
                      │
                      ▼
                Final Answer
                      │
                      ▼
             Conversation Memory

🧠 Agent Workflow

User Question
      ↓
Gemini Intent Router
      ↓
 ┌────┼─────┐
 ▼    ▼     ▼
CSV  PDF  GENERAL
 ▼    ▼     ▼
Pandas RAG  Gemini
 └────┼─────┘
      ↓
 Final Answer

🛠️ Tech Stack

Technology      Purpose

Python          Core programmingStreamlit       Web applicationGoogle Gemini   Generative AILangChain       LLM/RAG ecosystemLangGraph       Agent workflow and routingChromaDB        Vector storage for RAGPandas          Financial data analysisPyPDF           PDF processingGit & GitHub    Version control

📁 Project Structure

AI-Finance-Assistant/
│
├── app.py
├── requirements.txt
├── .gitignore
├── .env
├── data/
│   └── finance_data.csv
├── chroma_db/
└── screenshots/
    ├── ai-chat.png
    ├── financial-analyzer.png
    ├── pdf-assistant.png
    ├── rag-qa.png
    └── ai-agent.png

Do not commit .env or your Gemini API key to GitHub.

⚙️ Installation

git clone https://github.com/Abhishekojha26/AI-Credit-Risk-predictor.git
cd AI-Credit-Risk-predictor
python -m venv .venv

Windows:

.venv\Scriptsctivate

Install dependencies:

pip install -r requirements.txt

🔑 Environment Variables

Create .env:

GEMINI_API_KEY=your_gemini_api_key

▶️ Run Locally

python -m streamlit run app.py

📸 Screenshots

Add your screenshots to the screenshots/ folder and then use:

![AI Finance Chat]<img width="1339" height="656" alt="image" src="https://github.com/user-attachments/assets/f6116dfc-f818-4c88-a005-47348b9db2b7" />


![Financial Data Analyzer]<img width="1352" height="654" alt="image" src="https://github.com/user-attachments/assets/5ab2b02a-1fa1-485f-b26d-857370b7ed4a" />


![PDF Finance Assistant]<img width="1352" height="645" alt="image" src="https://github.com/user-attachments/assets/b6df3679-f91d-4ffb-b7b9-11fc25107319" />


![RAG Document Q&A]<img width="1350" height="628" alt="image" src="https://github.com/user-attachments/assets/436d5308-ba06-4289-aab2-19cd0f81b7f8" />


![AI Finance Agent]<img width="1342" height="625" alt="image" src="https://github.com/user-attachments/assets/e3b9df06-4bce-483c-9217-9524890cf3ff" />


🔐 Disclaimer

This application provides educational and informational financialguidance and is not a substitute for advice from a certified financialadvisor.

🔮 Future Improvements

Expense forecasting

Budget recommendations

Spending anomaly detection

Financial goal tracking

Multi-document RAG

More advanced finance agents

Improved dashboards and visualizations

👨‍💻 Author

Abhishek Ojha

GitHub: https://github.com/Abhishekojha26
