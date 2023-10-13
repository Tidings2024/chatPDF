import streamlit as st
from dotenv import load_dotenv
import pickle
from PyPDF2 import PdfReader
from streamlit_extras.add_vertical_space import add_vertical_space
from pathlib import Path

import os
import json 
import io
# Sidebar contents
with st.sidebar:
    st.title('🤗💬 LLM Chat App')
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [LangChain](https://python.langchain.com/)
    - [OpenAI](https://platform.openai.com/docs/models) LLM model
 
    ''')
    add_vertical_space(5)
    st.write('Made with ❤️ by [Prompt Engineer](https://youtube.com/@engineerprompt)')
 
load_dotenv()
 
def main():
    st.header("Chat with PDF 💬")
 
 
    # upload a PDF file
   
  
    # To read file as bytes:
    uploaded_file = st.file_uploader("Choose a file")
    

    


    if uploaded_file is not None:
        path_data = Path(uploaded_file.name)
        st.write(path_data)

        # Split the text file into 500 word chunks.
        chunks = split_text_file_into_chunks("./Data/epdf.tips_asimov-isaac-foundation-trilogy.txt", 500)

        # Export the chunks to a JSON file.
        export_chunks_to_json(chunks, "./output.json")

        if st.button('Enter'):
          title = st.text_input('Chat with doc', '')
          results = search_json_file_for_string("./output.json", title)
          for result in results:
            st.write(result)
            print(result)
        



def split_text_file_into_chunks(text_file_path, chunk_size):
  """Splits a text file into chunks of the specified size.

  Args:
    text_file_path: The path to the text file to split.
    chunk_size: The size of each chunk in words.

  Returns:
    A list of strings, where each string is a chunk of the text file.
  """

  text_file = open(text_file_path, "r")
  text = text_file.read()
  text_file.close()

  # Split the text into words.
  words = text.split()

  # Split the words into chunks.
  chunks = []
  chunk = []
  for word in words:
    chunk.append(word)
    if len(chunk) == chunk_size:
      chunks.append(" ".join(chunk))
      chunk = []

  # Add the remaining words to the last chunk.
  if len(chunk) > 0:
    chunks.append(" ".join(chunk))

  return chunks

def export_chunks_to_json(chunks, json_file_path):
  """Exports a list of strings to a JSON file as elements of an array.

  Args:
    chunks: A list of strings.
    json_file_path: The path to the JSON file to export to.
  """

  with open(json_file_path, "w") as json_file:
    json.dump(chunks, json_file, indent=4)

# Get the path to the text file to split.
text_file_path = "/path/to/text/file.txt"

# Get the path to the JSON file to export to.
json_file_path = "/path/to/json/file.json"





def search_json_file_for_string(json_file_path, search_string):
    """Searches an entire JSON file for a specific string of text and outputs the data block that the word is contained in.

    Args:
        json_file_path: The path to the JSON file.
        search_string: The string of text to search for.

    Returns:
        A list of data blocks that contain the search string.
    """
    
    results = []
    with open(json_file_path, "r") as json_file:
        json_data = json.load(json_file)

        def recursive_search(json_data, search_string):
            if isinstance(json_data, dict):
                for key, value in json_data.items():
                    recursive_search(value, search_string)

            elif isinstance(json_data, list):
                for item in json_data:
                    recursive_search(item, search_string)

            elif isinstance(json_data, str) and search_string in json_data:
                results.append(json_data)

        recursive_search(json_data, search_string)

    return results





  

  
 
if __name__ == '__main__':
    main()