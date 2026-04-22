# Import necessary libraries
import os
import streamlit as st
from langchain_openai import ChatOpenAI

# System prompt for the summarization task
sys_prompt = '''Harap buat ringkasan yang komprehensif dari teks yang diberikan.
Pastikan ringkasan ini tidak hanya merefleksikan ide utama dan argumen kunci, tetapi juga mempertahankan konteks dan nuansa orisinal dari bacaan.
Fokuslah untuk menyajikan poin-poin paling penting dan informasi esensial tanpa menambahkan interpretasi baru atau menghilangkan detail krusial yang dapat memengaruhi pemahaman menyeluruh terhadap teks asli.
Cukup tuliskan hasil ringkasan saja sebagai respon jawabanmu.'''

st.title("Summarization Apps")
# Set the page configuration
api_key = st.text_input("Enter your API Key:", type="password") # API key input
# Check if the API key is provided
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key # Set the OpenAI API key in the environment

    llm = ChatOpenAI(
        model="gpt-4o-mini", # Use "gpt-4o-mini" model
        temperature=0.5 # Set temperature to 0.5 for more creative output
    )

    user_query = st.text_area("Input Text Here") # Input text area for user queries
    if user_query:
        prompt = f"{sys_prompt}\n'''\nUser: {user_query}\n'''" # Construct the prompt for the LLM
        if st.button("Running Summarization"):
            response = llm.invoke(prompt) # Invoke the LLM with the constructed prompt

            st.markdown("## Summarization Result:") # Display the summarization result header
            st.markdown(response.content) # Display the response content from the LLM

            input_tokens = response.response_metadata["token_usage"]["prompt_tokens"] # Get the number of input tokens used
            output_tokens = response.response_metadata["token_usage"]["completion_tokens"] # Get the number of output tokens used
            model_used = response.response_metadata["model_name"] # Get the model name used for the response
            with st.expander("See Usage Details"): # Expandable section for usage details
                st.code(f"input_tokens: {input_tokens}") # Display input tokens
                st.code(f"output_tokens: {output_tokens}") # Display output tokens
                st.code(f"model: {model_used}") # Display model name used