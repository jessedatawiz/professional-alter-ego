import json
from dataclasses import dataclass
from typing import Protocol

from openai import OpenAI


class ProfileLike(Protocol):
    name: str
    summary: str
    linkedin: str


@dataclass
class Provider:
    client: OpenAI
    model: str
    name: str = ""
    reasoning_effort: str | None = None


class ToolLike(Protocol):
    name: str

    def to_schema(self) -> dict: ...

    def execute(self, **kwargs) -> dict: ...


class ChatAgent:

    def __init__(self, profile: ProfileLike, tools: list[ToolLike],
                 providers: list[Provider],
                 system_prompt_template: str | None = None):
        self.profile = profile
        self.tools = tools
        self.providers = providers
        self._tool_map = {t.name: t for t in tools}
        self.system_prompt_template = system_prompt_template

    def system_prompt(self):
        return self.system_prompt_template.format(
            name=self.profile.name,
            summary=self.profile.summary,
            linkedin=self.profile.linkedin,
        )

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

    def _complete(self, messages, preferred=None):
        """Try providers in order, return first successful response."""
        ordered = []
        if preferred:
            ordered.append(preferred)
        for p in self.providers:
            if p not in ordered:
                ordered.append(p)
        for provider in ordered:
            try:
                kwargs = {
                    "model": provider.model,
                    "messages": messages,
                    "tools": [t.to_schema() for t in self.tools],
                }
                if provider.reasoning_effort:
                    kwargs["reasoning_effort"] = provider.reasoning_effort
                response = provider.client.chat.completions.create(**kwargs)
                return response, provider
            except Exception as e:
                print(f"Provider '{provider.name}' failed: {e}", flush=True)
                continue
        raise RuntimeError("All providers failed")

    def chat(self, message, history):
        messages = (
            [{"role": "system", "content": self.system_prompt()}]
            + history
            + [{"role": "user", "content": message}]
        )
        done = False
        active = None
        while not done:
            response, active = self._complete(messages, active)
            if response.choices[0].finish_reason == "tool_calls":
                msg = response.choices[0].message
                messages.append(msg)
                messages.extend(self.handle_tool_call(msg.tool_calls))
            else:
                done = True
        return response.choices[0].message.content
