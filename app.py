import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from google import genai

# -----------------------------
# Configuration
# -----------------------------
load_dotenv()

st.set_page_config(
    page_title="AI Finance Assistant",
    page_icon="💰",
    layout="wide"
)

st.title("💰 AI Finance Assistant")
st.write(
    "Analyze your financial data and get personalized AI-powered insights."
)

# -----------------------------
# Gemini Setup
# -----------------------------
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key not found. Please check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🤖 AI Finance Chat",
    "📊 Financial Data Analyzer",
    "📄 PDF Finance Assistant",
    "🔎 RAG Document Q&A",
    "🧠 AI Finance Agent"
])

# ============================================================
# TAB 1 - AI CHAT
# ============================================================

with tab1:

    st.subheader("🤖 Ask your Finance Assistant")

    question = st.text_input(
        "Ask a financial question:",
        placeholder="e.g. How can I reduce my monthly expenses?"
    )

    if question:

        with st.spinner("Thinking..."):

            try:

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=f"""
You are an AI Finance Assistant.

Give clear, practical and easy-to-understand financial guidance.

Important:
- Do not claim to be a certified financial advisor.
- Do not guarantee investment returns.
- Give educational and informational guidance.
- Use Indian Rupees (₹) when discussing money.

User question:
{question}
"""
                )

                st.subheader("🤖 AI Response")

                st.caption(
                    "Disclaimer: I am an AI, not a certified financial advisor. "
                    "This guidance is for educational and informational purposes."
                )

                st.markdown(response.text)

            except Exception as e:

                st.error(f"Something went wrong: {e}")


# ============================================================
# TAB 2 - FINANCIAL DATA ANALYZER
# ============================================================

with tab2:

    st.subheader("📊 Analyze Your Financial Data")

    st.write(
        "Upload a CSV containing your transaction or financial data."
    )

    uploaded_file = st.file_uploader(
        "Upload CSV file",
        type=["csv", "txt"]
    )

    if uploaded_file:

        try:

            df = pd.read_csv(uploaded_file)
            st.session_state.finance_df = df.copy()


            st.success("CSV uploaded successfully! ✅")

            # -----------------------------
            # Preview
            # -----------------------------

            st.subheader("📄 Data Preview")

            st.dataframe(
                df.head(10),
                use_container_width=True
            )

            # -----------------------------
            # Basic Information
            # -----------------------------

            st.subheader("📌 Dataset Information")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Transactions",
                    len(df)
                )

            with col2:
                st.metric(
                    "Columns",
                    len(df.columns)
                )

            with col3:
                st.metric(
                    "Missing Values",
                    int(df.isnull().sum().sum())
                )

            # -----------------------------
            # Detect Amount Column
            # -----------------------------

            amount_candidates = [
                "amount",
                "Amount",
                "expense",
                "Expense",
                "transaction_amount",
                "Transaction Amount",
                "value",
                "Value"
            ]

            amount_col = None

            for col in amount_candidates:

                if col in df.columns:
                    amount_col = col
                    break

            # -----------------------------
            # Detect Category Column
            # -----------------------------

            category_candidates = [
                "category",
                "Category",
                "type",
                "Type",
                "expense_category",
                "Expense Category"
            ]

            category_col = None

            for col in category_candidates:

                if col in df.columns:
                    category_col = col
                    break

            # -----------------------------
            # Amount Analysis
            # -----------------------------

            if amount_col:

                df[amount_col] = pd.to_numeric(
                    df[amount_col],
                    errors="coerce"
                )

                df_clean = df.dropna(
                    subset=[amount_col]
                )

                total_amount = df_clean[amount_col].sum()

                average_amount = df_clean[amount_col].mean()

                max_amount = df_clean[amount_col].max()

                st.subheader("💰 Financial Summary")

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Total Amount",
                        f"₹{total_amount:,.2f}"
                    )

                with col2:

                    st.metric(
                        "Average Transaction",
                        f"₹{average_amount:,.2f}"
                    )

                with col3:

                    st.metric(
                        "Highest Transaction",
                        f"₹{max_amount:,.2f}"
                    )

                # -----------------------------
                # Category Analysis
                # -----------------------------

                if category_col:

                    st.subheader("📊 Spending by Category")

                    category_summary = (
                        df_clean
                        .groupby(category_col)[amount_col]
                        .sum()
                        .sort_values(
                            ascending=False
                        )
                    )

                    st.bar_chart(
                        category_summary
                    )

                    # -----------------------------
                    # Top Category
                    # -----------------------------

                    top_category = (
                        category_summary.index[0]
                    )

                    top_category_amount = (
                        category_summary.iloc[0]
                    )

                    percentage = (
                        top_category_amount
                        / total_amount
                        * 100
                    )

                    st.info(
                        f"💡 Your highest spending category is "
                        f"**{top_category}**, accounting for "
                        f"**₹{top_category_amount:,.2f} "
                        f"({percentage:.1f}%)** of the total."
                    )

                # -----------------------------
                # AI Financial Analysis
                # -----------------------------

                st.subheader("🤖 AI Financial Insights")

                if st.button(
                    "✨ Analyze My Finances with AI"
                ):

                    with st.spinner(
                        "AI is analyzing your financial data..."
                    ):

                        if category_col:

                            category_text = (
                                category_summary
                                .to_string()
                            )

                        else:

                            category_text = (
                                "Category information "
                                "was not available."
                            )

                        prompt = f"""
You are an AI Finance Assistant.

Analyze the following financial transaction data.

Total amount:
₹{total_amount:,.2f}

Average transaction:
₹{average_amount:,.2f}

Highest transaction:
₹{max_amount:,.2f}

Category-wise spending:
{category_text}

Provide:

1. A short financial summary.
2. The highest spending category.
3. Potential areas where spending could be reduced.
4. Three practical budgeting suggestions.
5. One important financial habit to develop.

Do not claim to be a certified financial advisor.
Do not guarantee investment returns.
Keep the advice educational and practical.
"""

                        try:

                            response = client.models.generate_content(
                                model="gemini-3.6-flash",
                                contents=prompt
                            )

                            st.markdown(
                                response.text
                            )

                        except Exception as e:

                            st.error(
                                f"AI analysis failed: {e}"
                            )

            else:

                st.warning(
                    "I couldn't find an Amount column. "
                    "Please use a column such as "
                    "`Amount`, `amount`, `Expense`, or `Transaction Amount`."
                )

        except Exception as e:

            st.error(
                f"Could not read the CSV file: {e}"
            )
            # ============================================================
# TAB 3 - PDF FINANCE ASSISTANT
# ============================================================

with tab3:

    st.subheader("📄 Chat with Your Financial PDF")

    st.write(
        "Upload a financial statement or report and ask questions about it."
    )

    pdf_file = st.file_uploader(
        "Upload Financial PDF",
        type=["pdf"],
        key="financial_pdf"
    )

    if pdf_file:

        st.success("PDF uploaded successfully! ✅")

        st.info(
            f"📄 File: {pdf_file.name} | "
            f"Size: {pdf_file.size / 1024:.1f} KB"
        )

        pdf_question = st.text_input(
            "Ask a question about this PDF:",
            placeholder="e.g. What are the major expenses mentioned in this statement?",
            key="pdf_question"
        )

        if pdf_question:

            with st.spinner("🔍 Reading your financial document..."):

                try:

                    import io

                    pdf_data = io.BytesIO(
                        pdf_file.getvalue()
                    )

                    uploaded_pdf = client.files.upload(
                        file=pdf_data,
                        config={
                            "mime_type": "application/pdf"
                        }
                    )

                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=[
                            """
You are an AI Finance Document Assistant.

Analyze the uploaded financial PDF and answer the user's
question using information from the document.

Rules:
- Use information from the uploaded document.
- If the answer is not present in the document, clearly say so.
- Do not invent financial information.
- Explain numbers clearly.
- Do not claim to be a certified financial advisor.
- Do not guarantee investment returns.
- Keep the response educational and informational.
""",
                            uploaded_pdf,
                            f"""
User Question:

{pdf_question}
"""
                        ]
                    )

                    st.subheader("🤖 AI Document Answer")

                    st.caption(
                        "Disclaimer: I am an AI, not a certified financial advisor. "
                        "This analysis is for educational and informational purposes."
                    )

                    st.markdown(response.text)

                except Exception as e:

                    st.error(
                        f"PDF analysis failed: {e}"
                    )
                    # ============================================================
# TAB 4 - RAG DOCUMENT Q&A
# ============================================================

with tab4:

    st.subheader("🔎 RAG Document Q&A")

    st.write(
        "Upload a financial PDF and ask questions using "
        "Retrieval-Augmented Generation."
    )

    rag_pdf = st.file_uploader(
        "Upload PDF for RAG",
        type=["pdf"],
        key="rag_pdf"
    )

    if rag_pdf:

        st.success("PDF uploaded successfully! ✅")

        if st.button("🔨 Build RAG Knowledge Base"):

            with st.spinner(
                "Reading, chunking and indexing your document..."
            ):

                try:

                    import os
                    import tempfile

                    from langchain_community.document_loaders import PyPDFLoader
                    from langchain_text_splitters import RecursiveCharacterTextSplitter
                    from langchain_google_genai import GoogleGenerativeAIEmbeddings
                    from langchain_chroma import Chroma

                    # Save uploaded PDF temporarily
                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".pdf"
                    ) as temp_file:

                        temp_file.write(
                            rag_pdf.getvalue()
                        )

                        temp_path = temp_file.name

                    # -----------------------------
                    # 1. Load PDF
                    # -----------------------------

                    loader = PyPDFLoader(temp_path)

                    documents = loader.load()

                    # -----------------------------
                    # 2. Split into chunks
                    # -----------------------------

                    splitter = RecursiveCharacterTextSplitter(
                        chunk_size=1000,
                        chunk_overlap=150
                    )

                    chunks = splitter.split_documents(
                        documents
                    )

                    # -----------------------------
                    # 3. Create embeddings
                    # -----------------------------

                    embeddings = GoogleGenerativeAIEmbeddings(
                        model="gemini-embedding-001"
                    )

                    # -----------------------------
                    # 4. Create vector database
                    # -----------------------------

                    vector_store = Chroma.from_documents(
                        documents=chunks,
                        embedding=embeddings,
                        collection_name="finance_rag",
                        persist_directory="./chroma_db"
                    )

                    # Store in Streamlit session
                    st.session_state.rag_vector_store = vector_store
                    st.session_state.rag_ready = True

                    # Remove temporary file
                    os.remove(temp_path)

                    st.success(
                        f"✅ RAG knowledge base created! "
                        f"{len(chunks)} chunks indexed."
                    )

                except Exception as e:

                    st.error(
                        f"RAG setup failed: {e}"
                    )

        # ====================================================
        # QUESTION ANSWERING
        # ====================================================

        if st.session_state.get(
            "rag_ready",
            False
        ):

            st.divider()

            st.subheader(
                "💬 Ask questions about your document"
            )

            rag_question = st.text_input(
                "Your question:",
                placeholder=(
                    "e.g. What are the major expenses "
                    "mentioned in this document?"
                ),
                key="rag_question"
            )

            if rag_question:

                with st.spinner(
                    "🔎 Retrieving relevant information..."
                ):

                    try:

                        vector_store = (
                            st.session_state
                            .rag_vector_store
                        )

                        # -----------------------------
                        # Retrieve relevant chunks
                        # -----------------------------

                        retrieved_docs = (
                            vector_store
                            .similarity_search(
                                rag_question,
                                k=4
                            )
                        )

                        context = "\n\n".join(
                            [
                                doc.page_content
                                for doc in retrieved_docs
                            ]
                        )

                        # -----------------------------
                        # Send retrieved context to Gemini
                        # -----------------------------

                        prompt = f"""
You are an AI Finance Document Assistant.

Answer the user's question using ONLY the
retrieved document context below.

If the answer cannot be found in the context,
say clearly:

"I couldn't find this information in the document."

Do not invent numbers or financial information.

Retrieved document context:
----------------------------

{context}

----------------------------

User question:
{rag_question}

Give a clear and concise answer.
"""

                        response = client.models.generate_content(
                            model="gemini-3.6-flash",
                            contents=prompt
                        )

                        st.subheader(
                            "🤖 RAG Answer"
                        )

                        st.markdown(
                            response.text
                        )

                        # -----------------------------
                        # Show retrieved sources
                        # -----------------------------

                        with st.expander(
                            "📚 Retrieved Document Chunks"
                        ):

                            for i, doc in enumerate(
                                retrieved_docs,
                                start=1
                            ):

                                st.markdown(
                                    f"**Chunk {i}**"
                                )

                                st.write(
                                    doc.page_content
                                )

                                if doc.metadata:

                                    st.caption(
                                        f"Source: "
                                        f"Page {doc.metadata.get('page', 'N/A')}"
                                    )

                    except Exception as e:

                        st.error(
                            f"RAG question failed: {e}"
                        )
                        # ============================================================
# TAB 5 - AI FINANCE AGENT
# ============================================================

with tab5:

    st.subheader("🧠 AI Finance Agent")
    if "agent_history" not in st.session_state:
        st.session_state.agent_history = []

    st.write(
        "Ask a question and the agent will decide "
        "how to answer it."
    )

    agent_question = st.text_input(
        "Ask your Finance Agent:",
        placeholder="e.g. What is my highest spending category?",
        key="agent_question"
    )

    if agent_question:

        from langgraph.graph import StateGraph, START, END
        from typing import TypedDict

        class AgentState(TypedDict):
            question: str
            route: str
            context: str
            answer: str

        # -----------------------------------------
        # Decide which source to use
        # -----------------------------------------

        def decide_route(state):

            question = state["question"]

            csv_available = (
                st.session_state.get("finance_df") is not None
            )

            pdf_available = (
                st.session_state.get("rag_vector_store") is not None
            )

            routing_prompt = f"""
You are the routing brain of an AI Finance Assistant.

Available sources:

CSV data available: {csv_available}
PDF/RAG data available: {pdf_available}

Choose exactly ONE route:

CSV
PDF
GENERAL

Choose CSV for questions about uploaded transaction data.

Choose PDF for questions about information inside
the uploaded financial document.

Choose GENERAL for normal financial questions.

Return ONLY CSV, PDF, or GENERAL.

User question:
{question}
"""

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=routing_prompt
            )

            route = response.text.strip().upper()

            if "CSV" in route:
                route = "CSV"

            elif "PDF" in route:
                route = "PDF"

            else:
                route = "GENERAL"

            return {
                "route": route
            }

        # -----------------------------------------
        # CSV Tool
        # -----------------------------------------

        def csv_tool(state):

            df = st.session_state.get("finance_df")

            if df is None:

                return {
                    "context": (
                        "No CSV has been uploaded. "
                        "Please upload financial CSV data first."
                    )
                }

            amount_col = None
            category_col = None

            for col in [
                "Amount",
                "amount",
                "Expense",
                "expense"
            ]:

                if col in df.columns:

                    amount_col = col
                    break

            for col in [
                "Category",
                "category",
                "Type",
                "type"
            ]:

                if col in df.columns:

                    category_col = col
                    break

            if amount_col is None:

                return {
                    "context": "Amount column not found."
                }

            df = df.copy()

            df[amount_col] = pd.to_numeric(
                df[amount_col],
                errors="coerce"
            )

            df = df.dropna(
                subset=[amount_col]
            )

            total = df[amount_col].sum()

            context = f"""
Total transactions: {len(df)}

Total spending: ₹{total:,.2f}
"""

            if category_col:

                category_summary = (
                    df.groupby(category_col)[amount_col]
                    .sum()
                    .sort_values(ascending=False)
                )

                context += f"""

Category-wise spending:

{category_summary.to_string()}
"""

            return {
                "context": context
            }

        # -----------------------------------------
        # PDF / RAG Tool
        # -----------------------------------------

        def pdf_tool(state):

            vector_store = st.session_state.get(
                "rag_vector_store"
            )

            if vector_store is None:

                return {
                    "context": (
                        "No PDF RAG knowledge base is available."
                    )
                }

            docs = vector_store.similarity_search(
                state["question"],
                k=4
            )

            context = "\n\n".join(
                doc.page_content
                for doc in docs
            )

            return {
                "context": context
            }

        # -----------------------------------------
        # General Tool
        # -----------------------------------------

        def general_tool(state):

            return {
                "context": (
                    "This is a general financial question."
                )
            }

        # -----------------------------------------
        # Final Gemini Answer
        # -----------------------------------------

        def final_answer(state):

            history = st.session_state.get(
                "agent_history",
                []
            )

            previous_conversation = ""

            for chat in history[-5:]:

                previous_conversation += f"""
User: {chat['user']}
Assistant: {chat['assistant']}
"""

            prompt = f"""
You are an AI Finance Assistant.

Answer the user's current question using the
available context and previous conversation.

Previous conversation:
{previous_conversation}

Current user question:
{state["question"]}

Available context:
{state["context"]}

Rules:
- Use financial data accurately.
- Use previous conversation when it helps understand
  follow-up questions.
- Do not invent financial information.
- Do not guarantee investment returns.
- Give educational and informational guidance.
- Keep the answer clear and concise.
"""

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            return {
                "answer": response.text
            }
        # -----------------------------------------
        # Route
        # -----------------------------------------

        def route(state):

            if state["route"] == "CSV":
                return "csv"

            if state["route"] == "PDF":
                return "pdf"

            return "general"

        # -----------------------------------------
        # Build LangGraph
        # -----------------------------------------

        graph = StateGraph(AgentState)

        graph.add_node(
            "decide",
            decide_route
        )

        graph.add_node(
            "csv",
            csv_tool
        )

        graph.add_node(
            "pdf",
            pdf_tool
        )

        graph.add_node(
            "general",
            general_tool
        )

        graph.add_node(
            "final",
            final_answer
        )

        graph.add_edge(
            START,
            "decide"
        )

        graph.add_conditional_edges(
            "decide",
            route,
            {
                "csv": "csv",
                "pdf": "pdf",
                "general": "general"
            }
        )

        graph.add_edge(
            "csv",
            "final"
        )

        graph.add_edge(
            "pdf",
            "final"
        )

        graph.add_edge(
            "general",
            "final"
        )

        graph.add_edge(
            "final",
            END
        )

        agent = graph.compile()

        # -----------------------------------------
        # Run Agent
        # -----------------------------------------

        with st.spinner(
            "🧠 Agent is analyzing..."
        ):

            result = agent.invoke(
                {
                    "question": agent_question,
                    "route": "",
                    "context": "",
                    "answer": ""
                }
            )
            st.session_state.agent_history.append(
    {
        "user": agent_question,
        "assistant": result["answer"]
    }
)

        st.subheader(
            "🤖 Agent Answer"
        )

        st.markdown(
            result["answer"]
        )

        st.success(
            f"Agent selected: {result['route']}"
        )
        st.divider()

st.subheader("💬 Conversation History")

for chat in st.session_state.agent_history:

    st.markdown(
        f"**You:** {chat['user']}"
    )

    st.markdown(
        f"**🤖 Agent:** {chat['assistant']}"
    )
                      