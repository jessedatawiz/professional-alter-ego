import gradio as gr

import config
from agent import ChatAgent
from user_profile import Profile
from pushover import PushoverClient
from tools import Tool


def build_tools(pushover):
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
    pushover = PushoverClient(config.PUSHOVER_TOKEN, config.PUSHOVER_USER)
    profile = Profile(config.PROFILE_NAME, config.LINKEDIN_PATH, config.SUMMARY_PATH)
    tools = build_tools(pushover)
    agent = ChatAgent(profile, tools, config.OPENAI_MODEL, config.OPENAI_REASONING_EFFORT)
    gr.ChatInterface(agent.chat).launch()


if __name__ == "__main__":
    main()
