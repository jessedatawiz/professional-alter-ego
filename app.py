import gradio as gr
from openai import OpenAI
from typing import Protocol

from config import Config
from agent import ChatAgent, Provider
from user_profile import Profile
from pushover import PushoverClient
from tools import Tool


class Notifiable(Protocol):

    def send(self, message: str) -> None: ...


def build_tools(pushover: Notifiable):
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

    return [record_user_details, record_unknown_question]


def main():
    cfg = Config()
    pushover = PushoverClient(cfg.pushover_token, cfg.pushover_user)
    profile = Profile(cfg.profile_name, cfg.linkedin_path, cfg.summary_path)
    tools = build_tools(pushover)

    # providers in order of use
    openai_client = OpenAI()
    groq_client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=cfg.groq_api_key,
    )

    providers = [
        Provider(client=openai_client, model=cfg.openai_model, name="openai",
                 reasoning_effort=cfg.openai_reasoning_effort),
        Provider(client=groq_client, model=cfg.groq_model, name="groq"),
    ]
    with open(cfg.system_prompt_path, "r") as f:
        system_prompt_template = f.read()

    agent = ChatAgent(profile, tools, providers, system_prompt_template)
    gr.ChatInterface(agent.chat).launch()


if __name__ == "__main__":
    main()
