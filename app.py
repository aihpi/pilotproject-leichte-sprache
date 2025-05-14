import gradio as gr
from leichtesprache.core import simplify_text
from leichtesprache.llm import list_local_models
import leichtesprache.parameters as p
from leichtesprache.prompts import PROMPT_TEMPLATE, PROMPT_TEMPLATE_BASIC


pinfo = {
    # uebersetzt
    "Top k": "LLM-Parameter. Ein höherer Wert erzeugt einen abwechslungsreicheren Text",
    "Top p": "LLM-Parameter. Ein höherer Wert erzeugt einen abwechslungsreicheren Text",
    "Temp": "LLM-Parameter. Ein höhere Wert erhöht die Zufälligkeit der Antwort",
}

AVBL_LLMS = list_local_models()
AVBL_LLM_CHOICES = sorted(list(set(p.LLM_CHOICES) & set(AVBL_LLMS)))
DEFAULT_MODEL = (
    p.MODEL if (p.MODEL in AVBL_LLMS) else (AVBL_LLM_CHOICES[0] if AVBL_LLM_CHOICES else None)
)


# =======================================================
#  Logo LeiSA - hellblau
# =======================================================

with gr.Blocks(css="footer {visibility: hidden}") as demo:

    gr.Image(value="images/Logo-LeiSA-hellblau.png", show_label=False, height=80, elem_id="logo")

    # ======================================================================================================
    # Barrierefreiheit (analog Bsp. Bernau) - Kontrast (3 Modi) + Schriftgroessenaenderung + runde Buttons
    # ======================================================================================================
    gr.HTML(
        """
        <style>
            :root {
                --font-scale: 1;
            }

            * {
                font-size: calc(16px * var(--font-scale));
            }

            body, .gr-textbox, .gr-button, .gr-label {
                font-size: calc(16px * var(--font-scale));
            }

            #accessibility-bar {
                display: flex;
                justify-content: center;
                align-items: center;
                flex-wrap: wrap;
                width: 100%;
                gap: 12px;
                margin-bottom: 25px;
            }

            .accessibility-button{
                background-color: #0A286D;
                border: 2px solid #C5DAFF;
                border-radius: 30px;
                padding: 10px 16px;
                color: white;
                font-size: 16px;
                font-weight: bold;
                transistion: all 0.3s ease;
            }

            .accessibility-button:hover {
                background-color: #C5DAFF;
                color: #0A286D;
                border-color: white;
                cursor: pointer;
            }

            #logo {
                max-width: 100px;
            }
            
            #output-box .copy-button {
                font-size: 18px !important;
                padding: 8px 16px !important;
            }
        </style>

        <div id="accessibility-bar">
            <button class="accessibility-button" onclick="document.body.style.filter='none';">Kontrast: Normal</button>
            <button class="accessibility-button" onclick="document.body.style.filter='invert(1)';">Kontrast: Invertiert</button>
            <button class="accessibility-button" onclick="document.body.style.filter='grayscale(1)';">Kontrast: Graustufen</button>
            <button class="accessibility-button" onclick="document.documentElement.style.setProperty('--font-scale', '2');">A+</button>
            <button class="accessibility-button" onclick="document.documentElement.style.setProperty('--font-scale', '1')">A</button>
            <button class="accessibility-button" onclick="document.documentElement.style.setProperty('--font-scale', '0.5')">A-</button>
        </div>
    """
    )

    # ==============================================================
    # Hauptinterface
    # ==============================================================

    simplify_text,

    gr.Markdown(
        "<h2 style='text-align: center;'>KI-Prototyp Leichte-Sprache-Assistent (LeiSA)</h2>"
    )
    gr.Markdown(
        "Vereinfache Texte mit LLMs! - <a href='https://github.com/aihpi/leichte-sprache' target='_blank'>Zum Projekt auf GitHub</a>"
    )

    # Beispiel rausgenommen

    # Export-Button rausgenommen

    flagging_mode = ("never",)  # Export Button deaktiviert

    # Eingabetext u. Ausgabetext (in leichte Sprache)
    with gr.Row():
        input_text = gr.Textbox(label="Originaltext", lines=17, autoscroll=True)
        output_text = gr.Textbox(
            label="Leichte Sprache",
            lines=17,
            autoscroll=True,
            show_copy_button=True,
            elem_id="output-box",
        )
        copy_box = gr.Textbox(visible=False)

    gr.HTML(
        """
            <style>
                #output-box .svelte-1ipelgc {
                    transform: scale(1.3);
                    filter: drop-shadow(0 0 3px orange);
                    color: orange;
                    transition: 0.2s ease;
                }

               #output-box .svelte-1ipelgc:hover {
                background-color: #ffe8cc;
               } 
            </style>
        """
    )

    gr.Markdown("Hinweis zur Übersetzung: Dieser Text wurde mit einer KI erstellt.")
    gr.Markdown(
        "Bitte verarbeiten Sie keine personenbezogenen Daten mit dem Tool. Falls der Prototyp einmal nicht verfügbar sein sollte, kontaktieren Sie uns gern, wir kümmern uns darum."
    )

    # ausklappbare Einstellungen ausgeblendet vom Frontend
    with gr.Accordion(label="Einstellungen", open=False, visible=False):
        model = gr.Dropdown(
            choices=AVBL_LLM_CHOICES,
            value=DEFAULT_MODEL,
            label="KI-Modell auswählen",
            allow_custom_value=True,
        )
        use_rules = gr.Checkbox(
            value=p.USE_RULES,
            label="Advanced Prompt (verwende Regeln)",
            info="Verwende die Regeln zur Vereiinfachung",
            visible=False,
        )
        top_k = gr.Slider(1, 10, value=p.TOP_K, step=1, label="Top k", info=pinfo.get("Top k"))
        top_p = gr.Slider(0.1, 1, value=p.TOP_P, step=0.1, label="Top p", info=pinfo.get("Top p"))
        temp = gr.Slider(0.1, 10, value=p.TEMP, step=0.1, label="Temp", info=pinfo.get("Temp"))

    # Buttons: Vereinfachen, Kopieren und Loeschen
    with gr.Row():
        vereinfachen_btn = gr.Button("Vereinfachen!", variant="primary")
        vereinfachen_btn.click(
            fn=simplify_text,
            inputs=[input_text, model, use_rules, top_k, temp],
            outputs=[output_text],
        )
        clear_button = gr.Button("Löschen", variant="secondary")
        # clear_button.click(fn=lambda: "", outputs=input_text)   #leert nur Eingabe-Textbox
        clear_button.click(
            fn=lambda: ("", ""), outputs=[input_text, output_text]
        )  # leert beide Textfelder

    # Hinweis: Parameter bleiben unveraendert bei dieser Definition des clear-buttons

    # ==============================================================
    # Footer
    # ==============================================================

    gr.HTML(
        """
        <div style="text-align: center; margin-top: 40px;">
            <p style="font-size: 12px; color: #666;">Der KI-Prototyp LeiSA ist ein gemeinsames Projekt der DigitalAgentur Brandenburg GmbH<sup>1</sup> und des KI-Servicezentrums (KISZ) vom Hasso-Plattner-Institut<sup>2</sup></p>
            <p style="font-size: 10px; color: #999;"><sup>1</sup>Gefördert durch das Ministerium der Justiz und für Digitalisierung des Landes Brandenburg.</p>
            <p style="font-size: 10px; color: #999;"><sup>2</sup>Gefördert vom Bundesministerium für Bildung und Forschung.</p>
        </div>
    """
    )

# Start
if __name__ == "__main__":
    demo.launch()
