import json
from typing import Protocol

from openai import OpenAI


class ProfileLike(Protocol):
    name: str
    summary: str
    linkedin: str


class ToolLike(Protocol):
    name: str

    def to_schema(self) -> dict: ...

    def execute(self, **kwargs) -> dict: ...


class ChatAgent:

    def __init__(self, profile: ProfileLike, tools: list[ToolLike], model: str, reasoning_effort: str | None = None):
        self.openai = OpenAI()
        self.profile = profile
        self.tools = tools
        self.model = model
        self.reasoning_effort = reasoning_effort
        self._tool_map = {t.name: t for t in tools}

    def system_prompt(self):
        name = self.profile.name
        prompt = (
            f"You are acting as {name}. You are answering questions on "
            f"{name}'s website, particularly questions related to {name}'s "
            f"career, background, skills and experience. Your responsibility "
            f"is to represent {name} for interactions on the website as "
            f"faithfully as possible. You are given a summary of {name}'s "
            f"background and LinkedIn profile which you can use to answer "
            f"questions. Be professional and engaging, as if talking to a "
            f"potential client or future employer who came across the "
            f"website. If you don't know the answer to any question, use "
            f"your record_unknown_question tool to record the question that "
            f"you couldn't answer, even if it's about something trivial or "
            f"unrelated to career. If the user is engaging in discussion, "
            f"try to steer them towards getting in touch via email; ask for "
            f"their email and record it using your record_user_details tool."
        )
        prompt += (
            f"\n\n## Summary:\n{self.profile.summary}\n\n"
            f"## LinkedIn Profile:\n{self.profile.linkedin}\n\n"
            f"With this context, please chat with the user, always staying "
            f"in character as {name}."
        )
        return prompt

    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            tool = self._tool_map.get(tool_name)
            result = tool.execute(**arguments) if tool else {}
            results.append({
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tool_call.id,
            })
        return results

    def chat(self, message, history):
        messages = (
            [{"role": "system", "content": self.system_prompt()}]
            + history
            + [{"role": "user", "content": message}]
        )
        done = False
        while not done:
            kwargs = {
                "model": self.model,
                "messages": messages,
                "tools": [t.to_schema() for t in self.tools],
            }
            if self.reasoning_effort:
                kwargs["reasoning_effort"] = self.reasoning_effort
            response = self.openai.chat.completions.create(**kwargs)
            if response.choices[0].finish_reason == "tool_calls":
                msg = response.choices[0].message
                messages.append(msg)
                messages.extend(self.handle_tool_call(msg.tool_calls))
            else:
                done = True
        return response.choices[0].message.content
