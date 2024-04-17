import streamlit as st
from dotenv import load_dotenv

load_dotenv() ##load all the environment variables
import os
import re
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are Youtube video summarizer. You will be taking the transcript of the video
and summarizing the entir video and providing the important information in points within
250 words. the summary will be in professional format. please provide the summary of the text
given here: """


def extract_video_id(youtube_video_url):
    
    # Regular expression pattern to match YouTube video URL formats
    pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:[^/]+/.+/|(?:v|e(?:mbed)?)/|.*[?&]v=)|youtu\.be/)([^"&?/\s]{11})'

    # Attempt to find the video ID using the regex pattern
    match = re.search(pattern, youtube_video_url)

    if match:
        return match.group(1)  # Extracted video ID
    else:
        return None  # No video ID found


    
##geting the transcript of the video
def extract_transcript_details(youtube_video_url):
    try:
        video_id= extract_video_id(youtube_video_url)
        transcript_text= YouTubeTranscriptApi.get_transcript(video_id)
        
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]
            
        return transcript
        
        
    except Exception as e:
        raise e


## getting the summary based on the prompt from google gemini pro
def generate_gemini_content(transcript_text, prompt):
    
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+transcript_text)
    return response.text


st.title("YouTube Video Summarizer")
youtube_link = st.text_input("Enter YouTube video Link:")

if youtube_link:  # Check if the text input is not empty
    video_id = extract_video_id(youtube_link)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Summary"):
    # Ensure youtube_video_url is defined before calling extract_transcript_details
    transcript_text = extract_transcript_details(youtube_link)
    
    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Detailed Summary: ")
        st.write(summary)

