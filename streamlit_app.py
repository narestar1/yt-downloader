import streamlit as st
from pytube import YouTube
import os
import logging


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
            logging.info(url)
        else:
            st.error(message)
    else:
        st.error("Please provide a URL.")
