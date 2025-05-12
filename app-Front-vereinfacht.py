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

accessibility_bar = gr.HTML(
        """

        <div id="accessibility-bar" style="background-color: #003366; padding: 10px; display: flex; gap: 10px; justify-content: center;">
            <button onclick="increaseFontSize()" style="width: 40px; height: 40px; font-size: 16px; border-radius: 50%;>A+</button>
            <button onclick="decreaseFontSize()" style="width: 40px; height: 40px; font-size: 16px; border-radius: 50%;>A-</button>
            <button onclick="resetFontSize()" style="width: 40px; height: 40px; font-size: 16px; border-radius: 50%;>A</button>
            <button onclick="toggleCOntrast()" style="width: 40px; height: 40px; font-size: 14px; border-radius: 50%;>*</button>
        </div>

        <script>
        var currentFontSize = 16;
        var contrastMode = 0; // 0 = normal, 1 = hoher Kontrast, 2 = negativ

        function increaseFontSize(){
            currentFontSize += 2;
            document.body.style.fontSize = currentFontSize + "px";
        }

        function decreaseFontSize(){
            currentFontSize = Math.max(10, currentFontSize -2);
            document.body.style.fontSize = currentFontSize + "px";
        }

        function resetFontSize(){
            currentFontSize = 16;
            document.body.style.fontSize = currentFontSize + "px";
        }

        function toggleContrast(){
            contrastMode = (contrastMode + 1) % 3;
            if (contrastMode === 0) {
                //Normal
                document.body.style.backgrounColor = "white";
                document.body.style.color = "black";
            }
            else if (contrastMode === 1) {
                //Hoher KOntrast: schwarz/weiss
                document.body.style.backgrounColor = "black";
                document.body.style.color = "white";
            }
            else if (contrastMode === 3) {
                //Negativ: gelb auf schwarz
                document.body.style.backgrounColor = "black";
                document.body.style.color = "yellow";
            }
        }
        </script>
        """
)


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


ls_ui = gr.Interface(
    simplify_text,
    gr.Textbox(label="Original Text", lines=17, autoscroll=True),
    gr.Textbox(
        label="Leichte Sprache", lines=17, autoscroll=True, show_label=True, show_copy_button=True
    ),
    #title="KI-Prototyp: Leichte Sprache für die Verwaltung",
    title="KI-Prototyp Leichte-Sprache-Assistent (LeiSA)",
    #uebersetzt
    description="Vereinfache Texte mit LLMs! - <a href='https://github.com/aihpi/leichte-sprache' target='_blank'>Zum Projekt auf GitHub</a>",
    #examples=[[p.EXAMPLE, DEFAULT_MODEL, p.USE_RULES, 5, 0.9, 0.3]], # kompletter Examples-Bereich im Frontend
    #Export-Button Funktion ausblenden: (Originalcode -> neuen Code)
    #flagging_mode="manual",
    #flagging_dir=p.EXPORT_PATH,
    #flagging_options=[("Export", "export")],
    flagging_mode=None,
    flagging_dir=None,
    flagging_options=None,
    additional_inputs=[
        gr.Dropdown(
            #uebersetzt
            choices=AVBL_LLM_CHOICES, value=DEFAULT_MODEL, label="KI-Modell auswählen", allow_custom_value=True
        ),
        gr.Checkbox(
            value=p.USE_RULES,
            label="Advanced Prompt (verwende Regeln)",
            info="Verwende die Regeln zur Vereinfachung",
            visible=False   #Use Rules Button im Frontend nicht sichtbar, aber da vielleicht Infos noch gebraucht nur ausgeblendet
        ),
        gr.Slider(1, 10, value=p.TOP_K, step=1, label="Top k", info=pinfo.get("Top k")),
        gr.Slider(
            0.1, 1, value=p.TOP_P, step=0.1, label="Top p", info=pinfo.get("Top p"), visible=False
        ),
        gr.Slider(0.1, 1, value=p.TEMP, step=0.1, label="Temp", info=pinfo.get("Temp")),
    ],
    #uebersetzt
    #additional_inputs_accordion=gr.Accordion(label="Einstellungen", open=False),
    additional_inputs_accordion=None,   #Settings-Sektion ausgeblendet
    submit_btn="Vereinfachen!",
    css="footer {visibility: hidden}",
)

if __name__ == "__main__":

#    ls_ui.launch()


    with gr.BLocks() as app:
        accessibility_bar   #Barrierefreiheitsleiste
        logo_placeholder    #Logo-Position (wenn Logo einfuegen -> muss noch aktiviert werden)
        ls_ui.render()      #Hauptinterface


    app.launch()
