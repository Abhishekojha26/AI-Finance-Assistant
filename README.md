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

![AI Finance Chat](screenshots/ai-chat.png)

![Financial Data Analyzer](screenshots/financial-analyzer.png)

![PDF Finance Assistant](screenshots/pdf-assistant.png)

![RAG Document Q&A](screenshots/rag-qa.png)

![AI Finance Agent](screenshots/ai-agent.png)

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