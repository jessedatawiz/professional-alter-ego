import gradio as gr
from openai import OpenAI
from typing import Protocol

from config import Config
from agent import ChatAgent, Provider
from user_profile import Profile
from pushover import PushoverClient
from tools import Tool
from knowledge_base import KnowledgeBase
from observability import setup_phoenix


class Notifiable(Protocol):

    def send(self, message: str) -> None: ...


def build_tools(pushover: Notifiable, knowledge_base: KnowledgeBase):
    record_user_details = Tool(
        name="record_user_details",
        description=(
            "Use this tool to record that a user is interested in being "
            "in touch and provided an email address"
        ),
        parameters={
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "description": "The email address of this user",
                },
                "name": {
                    "type": "string",
                    "description": "The user's name, if they provided it",
                },
                "notes": {
                    "type": "string",
                    "description": (
                        "Any additional information about the conversation "
                        "that's worth recording to give context"
                    ),
                },
            },
            "required": ["email"],
            "additionalProperties": False,
        },
        handler=lambda email, name="Name not provided", notes="not provided":
            pushover.send(f"Recording {name} with email {email} and notes {notes}"),
    )

    record_unknown_question = Tool(
        name="record_unknown_question",
        description=(
            "Always use this tool to record any question that couldn't be "
            "answered as you didn't know the answer"
        ),
        parameters={
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The question that couldn't be answered",
                },
            },
            "required": ["question"],
            "additionalProperties": False,
        },
        handler=lambda question: pushover.send(f"Recording {question}"),
    )

    search_profile = Tool(
        name="search_profile",
        description=(
            "Search the profile owner's professional documents (summary, "
            "LinkedIn, etc.) for details relevant to the user's question. "
            "Returns the most relevant excerpts."
        ),
        parameters={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "What to look up about the profile owner's "
                        "background, skills, or experience"
                    ),
                },
            },
            "required": ["query"],
            "additionalProperties": False,
        },
        handler=lambda query: {"context": knowledge_base.retrieve(query)},
    )

    return [record_user_details, record_unknown_question, search_profile]


def main():
    cfg = Config()
    setup_phoenix(
        cfg.phoenix_enabled,
        cfg.phoenix_project_name,
        cfg.phoenix_project_description,
        cfg.phoenix_working_dir,
    )
    pushover = PushoverClient(cfg.pushover_token, cfg.pushover_user)
    profile = Profile(cfg.profile_name)
    knowledge_base = KnowledgeBase(
        cfg.docs_dir,
        cfg.qdrant_path,
        cfg.qdrant_collection,
        cfg.embedding_model,
        cfg.rag_top_k,
        rebuild=cfg.rag_rebuild,
    )
    tools = build_tools(pushover, knowledge_base)

    # providers in order of use
    openai_client = OpenAI()
    groq_client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=cfg.groq_api_key,
    )

    providers = [
        Provider(client=openai_client, model=cfg.openai_model, name="openai",
                 reasoning_effort=cfg.openai_reasoning_effort,
                 max_tokens_param=cfg.openai_max_tokens_param),
        Provider(client=groq_client, model=cfg.groq_model, name="groq"),
    ]
    with open(cfg.system_prompt_path, "r") as f:
        system_prompt_template = f.read()

    agent = ChatAgent(
        profile,
        tools,
        providers,
        system_prompt_template,
        max_message_length=cfg.max_message_length,
        max_session_messages=cfg.max_session_messages,
        token_policy_enabled=cfg.token_policy_enabled,
        max_tokens=cfg.max_tokens,
        max_tool_iterations=cfg.max_tool_iterations,
    )
    gr.ChatInterface(agent.chat).launch()


if __name__ == "__main__":
    main()
