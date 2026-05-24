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
        self.openai_max_tokens_param = os.getenv(
            "OPENAI_MAX_TOKENS_PARAM", "max_completion_tokens"
        )
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
        self.docs_dir = os.getenv("DOCS_PATH", "me")
        self.embedding_model = os.getenv(
            "EMBEDDING_MODEL", "text-embedding-3-small"
        )
        self.qdrant_path = os.getenv("QDRANT_PATH", "storage/qdrant")
        self.qdrant_collection = os.getenv("QDRANT_COLLECTION", "profile")
        self.rag_top_k = int(os.getenv("RAG_TOP_K", "4"))
        self.rag_rebuild = (
            os.getenv("RAG_REBUILD", "false").lower() == "true"
        )
        self.phoenix_enabled = (
            os.getenv("PHOENIX_ENABLED", "true").lower() == "true"
        )
        self.phoenix_project_name = os.getenv(
            "PHOENIX_PROJECT_NAME", "professional-alter-ego"
        )
        self.phoenix_project_description = os.getenv(
            "PHOENIX_PROJECT_DESCRIPTION",
            "Chatbot emulating Jesse's professional profile (RAG over me/ docs).",
        )
