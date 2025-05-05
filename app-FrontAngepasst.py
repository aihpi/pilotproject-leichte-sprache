import gradio as gr
from leichtesprache.core import simplify_text
from leichtesprache.llm import list_local_models
import leichtesprache.parameters as p


pinfo = {
    #uebersetzt
    "Top k": "LLM-Parameter. Ein höherer Wert erzeugt einen abwechslungsreicheren Text",
    "Top p": "LLM-Parameter. Ein höherer Wert erzeugt einen abwechslungsreicheren Text",
    "Temp": "LLM-Parameter. Ein höhere Wert erhöht die Zufälligkeit der Antwort",
}

AVBL_LLMS = list_local_models()
AVBL_LLM_CHOICES = sorted(list(set(p.LLM_CHOICES) & set(AVBL_LLMS)))
DEFAULT_MODEL = p.MODEL if (p.MODEL in AVBL_LLMS) else (AVBL_LLM_CHOICES[0] if AVBL_LLM_CHOICES else None)


# =======================================================
# Barrierefreiheit (analog Bsp. Bernau) - Kontrast (3 Modi) + Schriftgroessenaenderung + runde Buttons
# =======================================================

# ============================================================
# Platzhalter Logo (optional)
# ============================================================
logo_placeholder = gr.HTML(
    """
    <!-- Logo kann hier eingefuegt werden -->
    <!-- Bsp:
    <div style='text-align: center; margin-bottom: 10px;'>
        <img src='pfad-zum-logo.png' alt='Logo' style='heigth:80px;'>
    </div>
    -->
    """
)

# ==============================================================
# Hauptinterface
# ==============================================================



with gr.Blocks(css="""
    :root {
                --font-scale: 1;
            }

            body, .gr-block, .gr-box, .gr.label, .gr-textbox, .gr-button, .gr-slider, .gr-accordion {
                font-size: calc(16px * var(--font-scale));
            }

            #accessibility-bar {
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 12px;
                margin-bottom: 20px;
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
""") as demo:
    gr.HTML("""
    <style>
        footer {visibility: hidden;}
    </style>
        <script>
        window.addEventListener('DOMContentLoaded', () => {
            window.currentFontScale = 1.0;

            window.updateFontSize = function() {
                 document.documentElement.style.setProperty('--font-scal', window.currentFontScale.toFixed(2));
            }

            window.increaseFontSize = function () {
                window.currentFontScale += 0.1;
                window.updateFontSize();
            }
            window.resetFontSize = function() {
                window.currentFontScale = 1;
                window.updateFontSize();
            }
            window.decreaseFontSize = function() {
                window.currentFontScale = Math.max(0.5, currentFontScale - 0.1);
                window.updateFontSize();
            }
            document.documentElement.style.setProperty('--font-scale', currentFontScale.toFixed(2));   
        });
        </script>

        <div id="accessibility-bar">
            <button class="accessibility-button" onclick="document.body.style.filter='none';">Kontrast: Normal</button>
            <button class="accessibility-button" onclick="document.body.style.filter='invert(1)';">Kontrast: Invertiert</button>
            <button class="accessibility-button" onclick="document.body.style.filter='grayscale(1)';">Kontrast: Graustufen</button>
            <button class="accessibility-button" onclick="window.increaseFontSize()">A+</button>
            <button class="accessibility-button" onclick="window.resetFontSize()">A</button>
            <button class="accessibility-button" onclick="window.decreaseFontSize()">A-</button>
        </div>
    """)

    simplify_text,

    gr.Markdown("<h2 style='text-align: center;'>KI-Prototyp Leichte-Sprache-Assistent (LeiSA)</h2>")
    gr.Markdown("Vereinfache Texte mit LLMs! - <a href='https://github.com/aihpi/leichte-sprache' target='_blank'>Zum Projekt auf GitHub</a>")

    #examples=[[p.EXAMPLE, DEFAULT_MODEL, p.USE_RULES, 5, 0.9, 0.3]], # kompletter Examples-Bereich im Frontend
    #Export-Button Funktion ausblenden: (Originalcode -> neuen Code)
    #flagging_mode="manual",
    #flagging_dir=p.EXPORT_PATH,
    #flagging_options=[("Export", "export")],
    flagging_mode="never",  # Export Button deaktiviert

    with gr.Row():
        input_text = gr.Textbox(label="Originaltext", lines = 17, autoscroll=True)
        output_text = gr.Textbox(label="Leichte Sprache", lines=17, autoscroll=True, show_copy_button=True)

    

    with gr.Accordion(label="Einstellungen", open=False, visible=False):
        model = gr.Dropdown(choices=AVBL_LLM_CHOICES, value=DEFAULT_MODEL, label="KI-Modell auswählen", allow_custom_value=True)
        use_rules = gr.Checkbox(value=p.USE_RULES, label="Advanced Prompt (verwende Regeln)", info="Verwende die Regeln zur Vereiinfachung", visible=False)
        top_k = gr.Slider(1, 10, value=p.TOP_K, step=1, label="Top k", info=pinfo.get("Top k"))
        top_p = gr.Slider(0.1, 1, value=p.TOP_P, step=0.1, label="Top p", info=pinfo.get("Top p"))
        temp = gr.Slider(0.1, 10, value=p.TEMP, step=0.1, label ="Temp", info=pinfo.get("Temp"))


    with gr.Row():
        vereinfachen_btn = gr.Button("Vereinfachen!", variant="primary")
        vereinfachen_btn.click(fn=simplify_text, inputs=[input_text, model, use_rules, top_k, temp], outputs=[output_text])
        clear_button = gr.Button("Löschen", variant="secondary")
        #clear_button.click(fn=lambda: "", outputs=input_text)   #leert nur Eingabe-Textbox
        clear_button.click(fn=lambda: ("", ""), outputs=[input_text, output_text])  # leert beide Textfelder
        
   



if __name__ == "__main__":

    demo.launch(server_port=7862,	#Original auf Port 7860 -> somit nicht ueberschrieben
        inbrowser=True,			# automatisch Browser oeffnen
        share=False
    )
import gradio as gr
from leichtesprache.core import simplify_text
from leichtesprache.llm import list_local_models
import leichtesprache.parameters as p


pinfo = {
    #uebersetzt
    "Top k": "LLM-Parameter. Ein höherer Wert erzeugt einen abwechslungsreicheren Text",
    "Top p": "LLM-Parameter. Ein höherer Wert erzeugt einen abwechslungsreicheren Text",
    "Temp": "LLM-Parameter. Ein höhere Wert erhöht die Zufälligkeit der Antwort",
}

AVBL_LLMS = list_local_models()
AVBL_LLM_CHOICES = sorted(list(set(p.LLM_CHOICES) & set(AVBL_LLMS)))
DEFAULT_MODEL = p.MODEL if (p.MODEL in AVBL_LLMS) else (AVBL_LLM_CHOICES[0] if AVBL_LLM_CHOICES else None)


# =======================================================
# Barrierefreiheit (analog Bsp. Bernau) - Kontrast (3 Modi) + Schriftgroessenaenderung + runde Buttons
# =======================================================



# ============================================================
# Platzhalter Logo (optional)
# ============================================================
logo_placeholder = gr.HTML(
    """
    <!-- Logo kann hier eingefuegt werden -->
    <!-- Bsp:
    <div style='text-align: center; margin-bottom: 10px;'>
        <img src='pfad-zum-logo.png' alt='Logo' style='heigth:80px;'>
    </div>
    -->
    """
)


# ==============================================================
# Hauptinterface
# ==============================================================



with gr.Blocks(css="""
    :root {
                --font-scale: 1;
            }

            body, .gr-block, .gr-box, .gr.label, .gr-textbox, .gr-button, .gr-slider, .gr-accordion {
                font-size: calc(16px * var(--font-scale));
            }

            #accessibility-bar {
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 12px;
                margin-bottom: 20px;
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
""") as demo:
    gr.HTML("""
    <style>
        footer {visibility: hidden;}
    </style>
        <script>
        window.addEventListener('DOMContentLoaded', () => {
            window.currentFontScale = 1.0;

            window.updateFontSize = function() {
                 document.documentElement.style.setProperty('--font-scal', window.currentFontScale.toFixed(2));
            }

            window.increaseFontSize = function () {
                window.currentFontScale += 0.1;
                window.updateFontSize();
            }
            window.resetFontSize = function() {
                window.currentFontScale = 1;
                window.updateFontSize();
            }
            window.decreaseFontSize = function() {
                window.currentFontScale = Math.max(0.5, currentFontScale - 0.1);
                window.updateFontSize();
            }
            document.documentElement.style.setProperty('--font-scale', currentFontScale.toFixed(2));   
        });
        </script>

        <div id="accessibility-bar">
            <button class="accessibility-button" onclick="document.body.style.filter='none';">Kontrast: Normal</button>
            <button class="accessibility-button" onclick="document.body.style.filter='invert(1)';">Kontrast: Invertiert</button>
            <button class="accessibility-button" onclick="document.body.style.filter='grayscale(1)';">Kontrast: Graustufen</button>
            <button class="accessibility-button" onclick="window.increaseFontSize()">A+</button>
            <button class="accessibility-button" onclick="window.resetFontSize()">A</button>
            <button class="accessibility-button" onclick="window.decreaseFontSize()">A-</button>
        </div>
    """)

    simplify_text,

    gr.Markdown("<h2 style='text-align: center;'>KI-Prototyp Leichte-Sprache-Assistent (LeiSA)</h2>")
    gr.Markdown("Vereinfache Texte mit LLMs! - <a href='https://github.com/aihpi/leichte-sprache' target='_blank'>Zum Projekt auf GitHub</a>")

    #examples=[[p.EXAMPLE, DEFAULT_MODEL, p.USE_RULES, 5, 0.9, 0.3]], # kompletter Examples-Bereich im Frontend
    #Export-Button Funktion ausblenden: (Originalcode -> neuen Code)
    #flagging_mode="manual",
    #flagging_dir=p.EXPORT_PATH,
    #flagging_options=[("Export", "export")],
    flagging_mode="never",  # Export Button deaktiviert

    with gr.Row():
        input_text = gr.Textbox(label="Originaltext", lines = 17, autoscroll=True)
        output_text = gr.Textbox(label="Leichte Sprache", lines=17, autoscroll=True, show_copy_button=True)

    

    with gr.Accordion(label="Einstellungen", open=False, visible=False):
        model = gr.Dropdown(choices=AVBL_LLM_CHOICES, value=DEFAULT_MODEL, label="KI-Modell auswählen", allow_custom_value=True)
        use_rules = gr.Checkbox(value=p.USE_RULES, label="Advanced Prompt (verwende Regeln)", info="Verwende die Regeln zur Vereiinfachung", visible=False)
        top_k = gr.Slider(1, 10, value=p.TOP_K, step=1, label="Top k", info=pinfo.get("Top k"))
        top_p = gr.Slider(0.1, 1, value=p.TOP_P, step=0.1, label="Top p", info=pinfo.get("Top p"))
        temp = gr.Slider(0.1, 10, value=p.TEMP, step=0.1, label ="Temp", info=pinfo.get("Temp"))


    with gr.Row():
        vereinfachen_btn = gr.Button("Vereinfachen!", variant="primary")
        vereinfachen_btn.click(fn=simplify_text, inputs=[input_text, model, use_rules, top_k, temp], outputs=[output_text])
        clear_button = gr.Button("Löschen", variant="secondary")
        #clear_button.click(fn=lambda: "", outputs=input_text)   #leert nur Eingabe-Textbox
        clear_button.click(fn=lambda: ("", ""), outputs=[input_text, output_text])  # leert beide Textfelder
        
   



if __name__ == "__main__":

    demo.launch(server_port=7862,	#Original auf Port 7860 -> somit nicht ueberschrieben
        inbrowser=True,			# automatisch Browser oeffnen
        share=False
    )
