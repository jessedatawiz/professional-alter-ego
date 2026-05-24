from pathlib import Path
from typing import Callable

import gradio as gr

from config import Config

_CSS = """
footer { display: none !important; }
.gradio-container { max-width: 1280px !important; margin: 0 auto; }
#profile-card { padding: 4px 8px; }
#profile-card h1 { font-size: 1.25rem; margin-bottom: 0.25rem; }
#profile-card h2 { font-size: 0.95rem; opacity: 0.7; }
#profile-card h2:last-of-type { font-size: 0.8rem; }
#profile-card ul:last-of-type { font-size: 0.8rem; opacity: 0.7; }
"""


def _warm_soft() -> gr.themes.Soft:
    return gr.themes.Soft(primary_hue="orange", neutral_hue="stone").set(
        body_background_fill="#faf7f2",
        background_fill_primary="#fffdf9",
        block_background_fill="#fffdf9",
        block_border_color="#ece6dd",
    )


_FORCE_LIGHT_JS = """
() => {
    const url = new URL(window.location);
    if (url.searchParams.get('__theme') !== 'light') {
        url.searchParams.set('__theme', 'light');
        window.location.href = url.href;
    }
}
"""

_THEME_MAP = {
    "soft": _warm_soft(),
    "monochrome": gr.themes.Monochrome(),
    "glass": gr.themes.Glass(),
    "base": gr.themes.Base(),
}


def _read_profile_doc(cfg: Config) -> str:
    path = Path(cfg.ui_profile_doc)
    return path.read_text(encoding="utf-8") if path.exists() else ""


def build_interface(fn: Callable, cfg: Config) -> gr.Blocks:
    profile = _read_profile_doc(cfg)
    with gr.Blocks(title=cfg.ui_title, fill_height=True) as demo:
        with gr.Row(equal_height=False):
            with gr.Column(scale=1, min_width=260):
                gr.Markdown(profile, elem_id="profile-card")
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(
                    height=620,
                    placeholder=(
                        "Ask me anything about my background, "
                        "skills, or experience."
                    ),
                )
                textbox = gr.Textbox(
                    placeholder="Type a message...",
                    show_label=False,
                )
                gr.ChatInterface(
                    fn,
                    chatbot=chatbot,
                    textbox=textbox,
                    description=cfg.ui_description or None,
                    autofocus=True,
                    fill_height=True,
                    examples=[
                        "What's your professional background?",
                        "What technologies do you specialize in?",
                        "Tell me about a recent project you've worked on.",
                    ],
                    cache_examples=False,
                )
    return demo


def launch_interface(fn: Callable, cfg: Config) -> None:
    theme = _THEME_MAP.get(cfg.ui_theme, _warm_soft())
    build_interface(fn, cfg).launch(theme=theme, css=_CSS, js=_FORCE_LIGHT_JS)
