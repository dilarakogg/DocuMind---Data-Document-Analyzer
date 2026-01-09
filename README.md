
# DocuMind---Data-Document-Analyzer
DocuMind, an AI-powered analytics platform, that performs natural language data analysis on CSV files and leverages RAG  for intelligent document querying using GPT-4o and Gemini.

This project is a comprehensive artificial intelligence tool designed to perform advanced analysis and querying on structured data (CSV) and unstructured documents (PDF/TXT). By integrating Pandas Agents and Retrieval-Augmented Generation (RAG) architectures, the system enables users to interact with their data seamlessly using natural language.


-Key Features-

1)Structured Data Intelligence (CSV Analysis)

The system leverages the langchain_experimental Pandas Agent to bridge the gap between raw dataframes and natural language processing.

*Automated Data Profiling: Generates instant summaries including column descriptions, missing value reports, and duplicate entry status.

*Statistical Analysis: Provides descriptive statistics using the describe() method integrated with LLM reasoning.

*Dynamic Visualization: Automatically generates bar charts based on user-selected variables.

*Natural Language Querying: Users can ask complex questions about the dataset, and the agent generates and executes Python code in real-time to provide precise answers.


2)Unstructured Document Intelligence (RAG)

The application implements a robust RAG pipeline to allow users to "chat" with their documents. The workflow follows these technical stages:

*Ingestion: Supports PDF and TXT formats using PyPDFLoader and TextLoader.

*Segmentation: Documents are processed using RecursiveCharacterTextSplitter with optimized chunk sizes and overlaps to maintain semantic context.

*Vector Embeddings: Text chunks are transformed into high-dimensional vectors via OpenAIEmbeddings.

*Vector Store: Utilizes FAISS (Facebook AI Similarity Search) for efficient, high-speed similarity searches.

*Contextual Generation: The system retrieves the top-K relevant document segments and injects them into the GPT-4o prompt, ensuring the model's response is grounded strictly in the provided context to minimize hallucinations.


-Tech Stack-

Framework: Streamlit (UI)

Orchestration: LangChain

LLMs: OpenAI (GPT-4o), Google Gemini (Pro)

Vector Database: FAISS

Data Manipulation: Pandas



-System Architecture-


The project is modularized into three core components:

*app.py: The main entry point managing the Streamlit interface, session states, and UI layouts.

*datahelper.py: Handles logic for the Pandas Agent, including the trend analysis and data summarization functions.

*raghelper.py: Manages the end-to-end RAG pipeline, from document loading to vector retrieval and final generation.



Setup & Installation
Clone the repository.

Install dependencies:
pip install -r requirements.txt


Configure Environment: Create a .env file in the root directory:
openai_apikey=your_key_here
google_apikey=your_key_here


Run the application:
streamlit run app.py

  
