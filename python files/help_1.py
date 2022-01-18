from pathlib import Path
import streamlit as st


# Functions

def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()


def app():
    st.title('Home')


    intro_markdown = read_markdown_file("help.md")
    st.markdown(intro_markdown, unsafe_allow_html=True)


