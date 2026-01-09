import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
load_dotenv()
my_key_openai = os.getenv("openai_apikey")

def run_rag_logic(uploaded_file, question):
    # Create temporary file
    with open("temp_doc", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Load
    if uploaded_file.name.endswith(".pdf"):
        loader = PyPDFLoader("temp_doc")
    else:
        loader = TextLoader("temp_doc")
    
    raw_documents = loader.load()

    # Split
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splitted_documents = text_splitter.split_documents(raw_documents)

    # Embeddings & Vectorstore (FAISS)
    embeddings = OpenAIEmbeddings(api_key=my_key_openai)
    vectorstore = FAISS.from_documents(splitted_documents, embeddings)
    
    # Retrieval
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    relevant_docs = retriever.invoke(question) 
    context_data = " ".join([doc.page_content for doc in relevant_docs])

    # Generation (GPT-4o)
    llm = ChatOpenAI(model="gpt-4o", api_key=my_key_openai, temperature=0)
    
    final_prompt = f"Question: {question}\n\nContext: {context_data}\n\nPlease answer ONLY based on the context."
    response = llm.invoke(final_prompt)
    
    return response.content, relevant_docs