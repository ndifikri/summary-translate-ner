# import necessary libraries
import os
import streamlit as st
from langchain_openai import ChatOpenAI


st.title("Translation Apps")
# Set the page configuration
api_key = st.text_input("Enter your API Key:", type="password") # API key input

if api_key:
    os.environ["OPENAI_API_KEY"] = api_key

    llm = ChatOpenAI(
        model="gpt-4o-mini", # Use "gpt-4o-mini" model
        temperature=0.5 # Set temperature to 0.5 for more creative output
    )

    options = ["English", "Indonesia"] # Language options for translation
    selection = st.segmented_control(
        "Choose Language Target", options, selection_mode="single", default="English" # Default selection is "English"
    )
    st.markdown(f"Your selected language: {selection}.") # Display the selected language

    if selection:
        # System prompt for the translation task
        sys_prompt = f'''Harap terjemahkan teks berikut ke bahasa {selection}.
        Pastikan terjemahan ini akurat, mengalir dengan alami, dan mempertahankan makna serta nuansa asli dari teks sumber. Perhatikan gaya bahasa, konteks, dan istilah spesifik apa pun untuk memastikan terjemahan yang tepat.
        Tidak perlu terjemahkan istilah khusus atau istilah teknis yang ada dalam bacaan.
        Cukup tuliskan hasil terjemahannya saja sebagai respon jawaban kamu.'''

    user_query = st.text_area("Input Text Here") # Input text area for user queries
    if user_query:
        prompt = f"{sys_prompt}\n'''\n{user_query}\n'''" # Construct the prompt for the LLM
        if st.button("Running Translate"):
            response = llm.invoke(prompt) # Invoke the LLM with the constructed prompt

            st.markdown("## Translation Result:") # Display the translation result header
            st.markdown(response.content) # Display the response content from the LLM

            input_tokens = response.response_metadata["token_usage"]["prompt_tokens"] # Get the number of input tokens used
            output_tokens = response.response_metadata["token_usage"]["completion_tokens"] # Get the number of output tokens used
            model_used = response.response_metadata["model_name"] # Get the model name used for the response
            with st.expander("See Usage Details"): # Expandable section for usage details
                st.code(f"input_tokens: {input_tokens}") # Display input tokens
                st.code(f"output_tokens: {output_tokens}") # Display output tokens
                st.code(f"model: {model_used}") # Display model name used