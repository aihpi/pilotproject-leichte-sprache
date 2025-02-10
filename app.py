import gradio as gr
from leichtesprache.core import simplify_text
from leichtesprache.llm import list_local_models
import leichtesprache.parameters as p


pinfo = {
    "Top k": "LLM Parameter. A higher value will produce more varied text",
    "Top p": "LLM Parameter. A higher value will produce more varied text",
    "Temp": "LLM Parameter. Higher values increase the randomness of the answer",
}

AVBL_LLMS = list_local_models()
AVBL_LLM_CHOICES = sorted(list(set(p.LLM_CHOICES) & set(AVBL_LLMS)))
DEFAULT_MODEL = (
    p.MODEL if (p.MODEL in AVBL_LLMS) else (AVBL_LLM_CHOICES[0] if AVBL_LLM_CHOICES else None)
)

ls_ui = gr.Interface(
    simplify_text,
    gr.Textbox(label="Original Text", lines=17, autoscroll=True),
    gr.Textbox(
        label="Leichte Sprache", lines=17, autoscroll=True, show_label=True, show_copy_button=True
    ),
    title="KI-Prototyp: Leichte Sprache für die Verwaltung",
    description="Simplify Text with LLMs! - <a href='https://github.com/aihpi/leichte-sprache' target='_blank'>Check the repository to install it locally</a>",
    examples=[[p.EXAMPLE, DEFAULT_MODEL, p.USE_RULES, 5, 0.9, 0.3]],
    flagging_mode="never",
    additional_inputs=[
        gr.Dropdown(
            choices=AVBL_LLM_CHOICES, value=DEFAULT_MODEL, label="Model", allow_custom_value=True
        ),
        gr.Checkbox(
            value=p.USE_RULES,
            label="Advanced Prompt (Use Rules)",
            info="Use rules for simplification",
        ),
        gr.Slider(1, 10, value=p.TOP_K, step=1, label="Top k", info=pinfo.get("Top k")),
        gr.Slider(
            0.1, 1, value=p.TOP_P, step=0.1, label="Top p", info=pinfo.get("Top p"), visible=False
        ),
        gr.Slider(0.1, 1, value=p.TEMP, step=0.1, label="Temp", info=pinfo.get("Temp")),
    ],
    additional_inputs_accordion=gr.Accordion(label="Settings", open=False),
    submit_btn="Simplify!",
    css="footer {visibility: hidden}",
)

if __name__ == "__main__":

    ls_ui.launch()
