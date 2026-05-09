import os

from dotenv import load_dotenv

load_dotenv(override=True)

PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")
PUSHOVER_USER = os.getenv("PUSHOVER_USER")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_REASONING_EFFORT = os.getenv("OPENAI_REASONING_EFFORT")
PROFILE_NAME = os.getenv("PROFILE_NAME", "John Doe")
LINKEDIN_PATH = os.getenv("LINKEDIN_PATH", "me/linkedin.pdf")
SUMMARY_PATH = os.getenv("SUMMARY_PATH", "me/summary.txt")
