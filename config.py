"""
configure your youtube client here
"""

from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()

# obtain api key from Google Developer Console
api_key = os.getenv("API_KEY")
client = build('youtube', 'v3', developerKey=api_key)