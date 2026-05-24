---
title: Professional Alter Ego
emoji: 🐠
colorFrom: gray
colorTo: pink
sdk: gradio
sdk_version: 6.14.0
app_file: app.py
pinned: false
license: apache-2.0
short_description: A chatbot that emulates my professional profile.
---

# Professional Alter Ego

A conversational AI that answers questions about my professional background — built with RAG over my profile docs, tool use, and a Gradio interface.

## How it works

- **RAG** — profile documents (`me/`) are embedded with OpenAI and indexed in Qdrant; relevant chunks are retrieved on each turn
- **Tool use** — the agent can record interested visitors (via Pushover notification) and log unanswered questions
- **Multi-provider** — routes through OpenAI (primary) and Groq (fallback) using the OpenAI-compatible API
- **Observability** — traces sent to Arize Phoenix when enabled

## Stack

| Layer | Tech |
|---|---|
| UI | Gradio |
| LLM | OpenAI / Groq |
| Embeddings | `text-embedding-3-small` |
| Vector store | Qdrant |
| Notifications | Pushover |
| Observability | Arize Phoenix |

## Run locally

```bash
cp .env.example .env  # fill in your keys
uv sync
uv run python app.py
```

**Required env vars:** `OPENAI_API_KEY`, `GROQ_API_KEY`, `PUSHOVER_TOKEN`, `PUSHOVER_USER`

## Customize for yourself

1. Replace files in `me/` with your own background docs
2. Update `prompts/system.md` with your persona
3. Set `PROFILE_NAME` in `.env`
