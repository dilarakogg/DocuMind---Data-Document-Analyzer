import pandas as pd
from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI 
import os 
from dotenv import load_dotenv
load_dotenv()

my_key_openai = os.getenv("openai_apikey")
my_key_google = os.getenv("google_apikey") 


llm_gpt = ChatOpenAI(api_key=my_key_openai, model="gpt-4o", temperature=0) 
llm_gemini = ChatGoogleGenerativeAI(api_key=my_key_google, model="gemini-pro", temperature=0)

selected_llm = llm_gpt

#summarize data

def summarize_csv(data_file):

    df = pd.read_csv(data_file, low_memory=False)

    pandas_agent = create_pandas_dataframe_agent(
    selected_llm, 
    df, 
    verbose=True, 
    allow_dangerous_code=True, 
    agent_executor_kwargs={"handle_parsing_errors": True}
)
    data_summary = {}

    data_summary["initial_data_sample"] = df.head()

    data_summary["column_descriptions"] = pandas_agent.run(" Create a table showing the columns of the dataset. For each column, provide its name and a brief description of what kind of data it contains. Format the output as a markdown table with two columns: 'Column Name' and 'Description'.")

    data_summary["missing_values"] = pandas_agent.run(" Identify any columns in the dataset that contain missing values. If so, provide the column name and the count of missing values. Format the output as a markdown table with two columns: 'Column Name' and 'Missing Values Count'.")

    data_summary["duplicate_values"] = pandas_agent.run("Is there any duplicate data in this dataset? If so, how many duplicates are there? Answer in the format 'There are X duplicate entries in this dataset'.")

    data_summary["essential_metrics"] = df.describe()

    return data_summary



def get_dataframe(data_file):

    df = pd.read_csv(data_file, low_memory=False)

    return df


def analyze_trend(data_file, variable_of_interest):

    df = pd.read_csv(data_file, low_memory=False)

    pandas_agent = create_pandas_dataframe_agent(selected_llm, df, verbose=True, agent_executor_kwargs= {"handle_parsing_errors":"True"})

    trend_response = pandas_agent.run(f"Analyze the trend of the variable {variable_of_interest}. Do not refuse to analyze. Since the rows in the dataset are based on dates from the past to today, you can analyze them. Answer in English.")

    return trend_response


def ask_question(data_file, question):

    df = pd.read_csv(data_file, low_memory=False)

    pandas_agent = create_pandas_dataframe_agent(selected_llm, df, verbose=True, agent_executor_kwargs= {"handle_parsing_errors":"True"})

    AI_Response = pandas_agent.run(f"{question}  Answer in English.")

    return AI_Response
