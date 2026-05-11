import os

from dotenv import load_dotenv


class Config:

    def __init__(self):
        load_dotenv(override=True)
        self.pushover_token = os.getenv("PUSHOVER_TOKEN")
        self.pushover_user = os.getenv("PUSHOVER_USER")
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.openai_reasoning_effort = os.getenv("OPENAI_REASONING_EFFORT")
        self.profile_name = os.getenv("PROFILE_NAME", "Jesse Rodrigues")
        self.linkedin_path = os.getenv("LINKEDIN_PATH", "me/linkedin.pdf")
        self.summary_path = os.getenv("SUMMARY_PATH", "me/summary.txt")
        self.system_prompt_path = os.getenv("SYSTEM_PROMPT_PATH", "prompts/system.md")
        self.max_message_length = int(
            os.getenv("MAX_MESSAGE_LENGTH", "1000")
        )
        self.max_session_messages = int(
            os.getenv("MAX_SESSION_MESSAGES", "20")
        )
        self.token_policy_enabled = (
            os.getenv("TOKEN_POLICY_ENABLED", "true").lower() == "true"
        )
        self.max_tokens = int(
            os.getenv("MAX_TOKENS", "512")
        )
        self.max_tool_iterations = int(
            os.getenv("MAX_TOOL_ITERATIONS", "5")
        )
