# Import necessary libraries
import os, ast
import streamlit as st
from annotated_text import annotated_text

from langchain_openai import ChatOpenAI

# Example output for the NER task
example_output = (
    ("Elon Musk", "PERSON"),
    " dari ",
    ("Tesla", "ORG"),
    " mengumumkan bahwa mobil listrik terbaru, ",
    ("Cybertruck", "PRODUCT"),
    ", akan diluncurkan pada ",
    ("10 September 2024", "DATE"),
    " di ",
    ("Austin, Texas", "LOC"),
    " dalam sebuah ",
    ("konferensi pers tahunan", "EVENT"),
    "."
) 
# System prompt for the NER task
sys_prompt = f'''Tugas Anda adalah melakukan Named Entity Recognition (NER) pada teks yang diberikan dan mengembalikan hasilnya dalam format yang dicontohkan di bawah ini.

Input : Elon Musk dari Tesla mengumumkan bahwa mobil listrik terbaru, Cybertruck, akan diluncurkan pada 10 September 2024 di Austin, Texas dalam sebuah konferensi pers tahunan.
Output : {str(example_output)}

'''

# Streamlit app setup
st.title("NER Apps")
# Set the page configuration
# API key input
api_key = st.text_input("Enter your API Key:", type="password")

if api_key:
    os.environ["OPENAI_API_KEY"] = api_key

    llm = ChatOpenAI(
        model="gpt-5.4-nano", #use model
        temperature=0 # Set temperature to 0 for deterministic output
    )

    user_query = st.text_area("Input Text Here") # Input text area for user queries
    if user_query:
        prompt = f"{sys_prompt}\nInput: {user_query}\nOutput: " # Construct the prompt for the LLM
        if st.button("Running NER"): # Button to trigger the NER task
            response = llm.invoke(prompt) # Invoke the LLM with the constructed prompt
            response_string = response.content # Get the response content from the LLM
            formatted_response = ast.literal_eval(response_string) # Parse the response string into a Python object
            annotated_text(*formatted_response) # Display the annotated text using annotated_text library

            input_tokens = response.response_metadata["token_usage"]["prompt_tokens"] # Get the number of input tokens used
            output_tokens = response.response_metadata["token_usage"]["completion_tokens"] # Get the number of output tokens used
            model_used = response.response_metadata["model_name"] # Get the model name used for the response
            with st.expander("See Usage Details"): # Expandable section for usage details
                st.code(f"input_tokens: {input_tokens}") # Display input tokens
                st.code(f"output_tokens: {output_tokens}") # Display output tokens
                st.code(f"model: {model_used}") # Display model name used