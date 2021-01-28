from pathlib import Path
import streamlit as st


# Functions

def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()


def app():
    st.title('About')

    # video_file = open('/Users/olayile/Bioprocess-tool/Images/Green Connection Icon Internet Logo.mp4', 'rb')
    # video_bytes = video_file.read()

    # st.video(video_bytes)


    intro_markdown = read_markdown_file("about.md")
    st.markdown(intro_markdown, unsafe_allow_html=True)

