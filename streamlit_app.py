import streamlit as st
from pytube import YouTube
import os
import logging
import sys

# Configure the logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)  # Ensure logs are sent to stdout
    ]
)

# Create a logger object
logger = logging.getLogger(__name__)

def download_video(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path="downloads")
        return f"downloads/{stream.default_filename}", yt.title
    except Exception as e:
        return None, f"Error: {e}"


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        return f"File {file_path} deleted."
    else:
        return f"File {file_path} not found."


# Streamlit UI
st.title("YouTube Downloader Naresh")
logger.info("Some body logged in")

url = st.text_input("Enter YouTube Video URL:")

if st.button("Download"):
    if url:
        file_path, message = download_video(url)
        if file_path:
            with open(file_path, "rb") as file:
                btn = st.download_button(
                    label="Download Video",
                    data=file,
                    file_name=os.path.basename(file_path),
                    mime="video/mp4",
                    on_click=delete_file,
                    args=(file_path,),
                )
            st.success(f"Downloaded: {message}")
            logger.info(url)
        else:
            st.error(message)
            logger.info(url)
    else:
        st.error("Please provide a URL.")
