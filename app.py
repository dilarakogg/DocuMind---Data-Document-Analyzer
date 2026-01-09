import streamlit as st
import datahelper 
import raghelper  


if "dataload" not in st.session_state:
    st.session_state.dataload = False

def activate_dataload():
    st.session_state.dataload = True

st.set_page_config(page_title="DocuMind 🤖", layout="wide")
st.title("AI Explorer: Data & Document Intelligence 🤖")
st.divider()


st.sidebar.subheader("Operation Menu")
app_mode = st.sidebar.selectbox("Select a Tool", ["📊 CSV Data Analysis", "📄 Document Intelligence (RAG)"])
st.sidebar.divider()


if app_mode == "📊 CSV Data Analysis":
    st.sidebar.subheader("Upload Your Dataset")
    loaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
    load_data_btn = st.sidebar.button(label="Load Data", on_click=activate_dataload, use_container_width=True)

    col_prework, col_dummy, col_interaction = st.columns([4,1,7])

    if st.session_state.dataload and loaded_file:
        @st.cache_data
        def summarize():
            loaded_file.seek(0)
            data_summary = datahelper.summarize_csv(data_file=loaded_file)
            return data_summary
        
        data_summary = summarize()

        with col_prework:
            st.info("DATA SUMMARY")
            st.subheader("Data Sample Preview:")
            st.write(data_summary["initial_data_sample"])
            st.divider()
            st.subheader("Variable Descriptions:")
            st.write(data_summary["column_descriptions"])
            st.divider()
            st.subheader("Missing Values Report:")
            st.write(data_summary["missing_values"])
            st.divider()
            st.subheader("Duplicate Entries Status:")
            st.write(data_summary["duplicate_values"])
            st.divider()
            st.subheader("Essential Metrics")
            st.write(data_summary["essential_metrics"])
            
        with col_dummy: st.empty()
        
        with col_interaction:
            st.info("DATA INTERACTION")
            variable_of_interest = st.text_input(label="Which variable would you like to analyze?")
            examine_btn = st.button(label="Analyze")
            st.divider()

            if variable_of_interest or examine_btn:
                loaded_file.seek(0)
                dataframe = datahelper.get_dataframe(data_file=loaded_file)
                st.bar_chart(data=dataframe, y=[variable_of_interest])
                st.divider()
                loaded_file.seek(0)
                trend_response = datahelper.analyze_trend(data_file=loaded_file, variable_of_interest=variable_of_interest)
                st.success(trend_response)

            free_question = st.text_input(label="What would you like to know about the data?")
            ask_btn = st.button(label="Ask")
            
            if free_question or ask_btn:
                loaded_file.seek(0)
                AI_Response = datahelper.ask_question(data_file=loaded_file, question=free_question)
                st.success(AI_Response)

elif app_mode == "📄 Document Intelligence (RAG)":
    st.subheader("Document Intelligence (RAG)")
    st.info("Upload a PDF or Text file to ask questions based on its content.")
    
    rag_file = st.file_uploader("Upload File (PDF/TXT)", type=["pdf", "txt"])
    rag_query = st.text_input("What would you like to ask the document?")
    rag_btn = st.button("Query Document")

    if rag_btn and rag_file and rag_query:
        with st.spinner("Analyzing document..."):
            answer, sources = raghelper.run_rag_logic(rag_file, rag_query)
            st.markdown("###Answer:")
            st.success(answer)
            
            with st.expander("View Source Context"):
                for doc in sources:
                    st.write(doc.page_content)
                    st.divider()