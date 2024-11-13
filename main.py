import streamlit as st
from streamlit_option_menu import option_menu
import os
from dotenv import load_dotenv
import google.generativeai as gen_ai
from PIL import Image
import pandas as pd
import numpy as np
import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
import tempfile
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://dm0qx8t0i9gc9.cloudfront.net/thumbnails/image/rDtN98Qoishumwih/abstract-blue-light-background_SvZPryOnfl_thumb.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        height: 100vh; /* Extend background to full viewport height */
    }
    
    /* Header background */
    [data-testid="stHeader"] {
        background-image: url("https://dm0qx8t0i9gc9.cloudfront.net/thumbnails/image/rDtN98Qoishumwih/abstract-blue-light-background_SvZPryOnfl_thumb.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    
    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-image: url("https://img.freepik.com/free-vector/simple-blue-gradient-background-vector-business_53876-171631.jpg?ga=GA1.1.1906695768.1722986479&semt=ais_hybrid");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    /* Additional styling for header or top bar if any padding/margin issue occurs */
    .css-1d391kg { 
        padding-top: 0; /* Remove extra top padding if needed */
    }
    body {
        color: white;
    }
   
    </style>
    """,
    unsafe_allow_html=True
)
GROQ_API_KEY = "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"

# Initialize global variable for vector database
vectordb = None

def process_pdf(file_obj):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(file_obj.read())
            temp_pdf.flush()

            loader = UnstructuredPDFLoader(temp_pdf.name)
            documents = loader.load()

            if not documents:
                st.error("No documents loaded from the PDF.")
                return None

            text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=50)
            texts = text_splitter.split_documents(documents)

            if not texts:
                st.error("No text chunks were generated.")
                return None

            embeddings = HuggingFaceEmbeddings()

            global vectordb
            vectordb = Chroma.from_documents(texts, embeddings, persist_directory=".")

            if not vectordb:
                st.error("Failed to initialize Chroma vector DB.")
                return None

            st.success("PDF processed successfully!")
            return vectordb

    except Exception as e:
        st.error(f"Error processing PDF: {e}")
        return None


with st.sidebar:
    st.title("Feature Contents🌟")
    selected = option_menu(
        menu_title=None,  # required
        options=["🏠Home", "🩺Health Assist", "💪Fitness Assist"],
        default_index=0,
    )
    st.write('𝐒𝐞𝐥𝐞𝐜𝐭 𝐀𝐧𝐲 One Feature')

if selected == "🏠Home":
    st.markdown(
        """
        <h1 style='color: white;'>
            AI-Powered Personalized Health and Fitness Plans or Counsel
        </h1>
        """,
        unsafe_allow_html=True
    )
    st.image(r"C:\Users\Dell\Pictures\FY_Project\156Z_2306.w017.n001.59A.p22.59.jpg")

import streamlit as st
import os
import tempfile
import time


def reset_vectordb():
    global vectordb
    vectordb = None  # Reset vectordb to ensure fresh state


import streamlit as st
import tempfile
import time


def reset_vectordb():
    global vectordb
    vectordb = None  # Reset vectordb to ensure a fresh state


if selected == "🩺Health Assist":

    st.markdown(
        """
        <h1 style='color: white;'>
            𝐇𝐞𝐚𝐥𝐭𝐡 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 𝐀𝐬𝐬𝐢𝐬𝐭
        </h1>
        """,
        unsafe_allow_html=True
    )


    # File uploader for PDF
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

    if uploaded_file is not None:
        # Reset vectordb to ensure we don't reuse old data
        reset_vectordb()

        # Process the PDF file
        st.info("Processing the PDF... Please wait.")

        try:
            if process_pdf(uploaded_file):  # Pass the file object directly
                st.success("PDF processed successfully!")
            else:
                st.error("Failed to process the PDF. Please try again.")
        except AttributeError as e:
            st.error(f"Error processing PDF: {e}")

    # Input field for user query
    user_query = st.text_input("Ask a question about the PDF:")

    # Button to submit the query
    if st.button("Submit Query"):
        if not vectordb:
            st.error("Please upload and process a PDF before querying.")
        elif not user_query:
            st.error("Please enter a query.")
        else:
            try:
                # Initialize the retriever
                retriever = vectordb.as_retriever()

                # Initialize the language model with the GROQ API key
                llm = ChatGroq(model='Llama3-8b-8192', temperature=0, groq_api_key=GROQ_API_KEY)

                # Set up the question-answering chain
                qa_chain = RetrievalQA.from_chain_type(
                    llm=llm,
                    chain_type="stuff",
                    retriever=retriever,
                    return_source_documents=True
                )

                # Get response from the QA chain
                response = qa_chain.invoke({"query": user_query})

                st.markdown(
                    """
                    <style>
                    /* Apply white color to text displayed by st.write */
                    .stMarkdown, .stText {
                        color: white;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown(
                    """
                    <style>
                    /* Style the Result header and its icon to be white */
                    h3#result, h3#result a {
                        color: white !important;
                    }
                    /* Ensure all text and subheaders appear white */
                    .stMarkdown h3, .stText, .stMarkdown div {
                        color: white !important;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )
                # Display the response
                st.write("### Result:")
                st.write(response['result'])

            except Exception as e:
                st.error(f"Error during query: {e}")

if selected == "💪Fitness Assist":
    st.markdown(
        """
        <h1 style='color: white;'>
            𝐅𝐢𝐭𝐧𝐞𝐬𝐬 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 𝐀𝐬𝐬𝐢𝐬𝐭
        </h1>
        """,
        unsafe_allow_html=True
    )

    GOOGLE_API_KEY = "AIzaSyAdvFMPLqVykZfKUU-chpnKQBQzKU9Avgc"
    genai.configure(api_key=GOOGLE_API_KEY)
    st.markdown(
        """
        <style>
        /* Apply white color to all label texts */
        .stNumberInput label {
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    steps_count = st.number_input("Enter the number of steps:", min_value=0)
    distance_covered = st.number_input("Enter the distance covered (km):", min_value=0.0)
    calories_burned = st.number_input("Enter calories burned:", min_value=0)
    heart_rate = st.number_input("Enter heart rate (bpm):", min_value=0)
    sleep_duration = st.number_input("Enter sleep duration (hours):", min_value=0.0)

    # Button to submit inputs
    if st.button("Analyze"):
        input_data = (
            f"Steps: {steps_count} steps, "
            f"Distance: {distance_covered} km, "
            f"Calories: {calories_burned} kcal, "
            f"Heart Rate: {heart_rate} bpm, "
            f"Sleep Duration: {sleep_duration} hours."
        )

        # Define a fixed prompt
        fixed_prompt = "Analyze the user's health data based on steps, distance, calories, heart rate, and sleep duration."

        # Generate response using the model with the fixed prompt
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(fixed_prompt)

        st.markdown(
            """
            <style>
            /* Make all subheaders and st.write text white */
            .stMarkdown, .stText, .stSubheader {
                color: white;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        # Display the output in a specific text area
        st.markdown(
            """
            <style>
            /* Style subheader text and its icon to be white */
            h3#generated-analysis {
                color: white !important;
            }
            h3#generated-analysis a {
                color: white !important;
            }
            .stText, .stMarkdown div {
                color: white !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.subheader("Generated Analysis:")
        st.write(response.text)


