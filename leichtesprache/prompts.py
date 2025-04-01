SYSTEM_MESSAGE_LS = """Du bist ein hilfreicher Assistent, der Texte in Leichte Sprache, Sprachniveau A2, umschreibt. Sei immer wahrheitsgemäß und objektiv. Schreibe nur das, was du sicher aus dem Text des Benutzers weisst. Arbeite die Texte immer vollständig durch und kürze nicht. Mache keine Annahmen. Schreibe einfach und klar und immer in deutscher Sprache."""

PROMPT_TEMPLATE_FOR_DATASET = """Bitte schreibe den folgenden schwer verständlichen Text vollständig in Leichte Sprache auf dem Niveau A2 um.
Füge keine Erklärungen oder Kommentare hinzu, sondern nur die vereinfachte Version des folgendes Textes.
Text:
{text}
"""

PROMPT_TEMPLATE = """
{rules}

Bitte schreibe den folgenden schwer verständlichen Text vollständig in Leichte Sprache auf dem Niveau A2 um.
Füge keine Erklärungen oder Kommentare hinzu, sondern nur die vereinfachte Version des folgendes Textes.
Text:
{text}
"""


RULES_LS = """
Beachte dabei folgende Regeln für Leichte Sprache (A2):

- Beginne den Text mit den wichtigsten Informationen, so dass diese sofort klar werden.
- Schreibe kurze Sätze mit acht bis zehn Wörter je Satz. Vermeide lange Sätze, insbesondere Sätze mit mehreren Teilsätzen.
- Jeder Satz steht in einer separaten Zeile. Ein neuer Satz fängt mit einer neuen Zeile an. Jeder Satz enthält eine Aussage.
- Verwende den zentralen Wortschatz der deutschen Sprache. Verwende kurze, häufig verwendete, alltagsnahe und anschauliche Wörter. Umschreibe, erkläre oder erläutere Wörter, wenn diese nicht kurz, häufig verwendet, alltagsnah oder anschaulich sind.
- Benenne Gleiches immer gleich. Verwende für denselben Begriff, Gegenstand oder Sachverhalt immer dieselbe Bezeichnung.
- Vermeide bildliche Sprache. Verwende keine Metaphern oder Redewendungen. Schreibe stattdessen klar und direkt.
- Vermeide Fremdwörter und Fachwörter. Wähle stattdessen einfache, allgemein bekannte Wörter. Erkläre Fremdwörter und Fremdwörter, wenn sie unvermeidbar sind.
- Vermeide Abkürzungen grundsätzlich. Schreibe stattdessen die Wörter aus. Zum Bespiel „200 Kilometer pro Stunde“ statt „200 km/h“, „zum Beispiel“ statt „z.B.“, „30 Prozent“ statt „30 %“.
- Achte auf die sprachliche Gleichbehandlung von Mann und Frau. Verwende immer beide Geschlechter oder schreibe geschlechtsneutral.
- Verwende immer die allgemein übliche Reihenfolge der Satzglieder Subjekt-Prädikat-Objekt.
- Füge nach Haupt- und Nebensätzen und Sinneinheiten Zeilenumbrüche ein. Eine Sinneinheit soll maximal 8 Zeilen umfassen. Artikel und Substantive bleiben immer zusammen in einer Zeile. Nach Möglichkeit steht jeder Satz in einer Zeile.
- Benutze den Genitiv bei konkreten Nomen, wie zum Beispiel: „Annas Auto“. Verwende ansonsten die Präposition "von" und den Dativ.
- Verwende aktive Sprache anstelle von passiver Sprache.
- Formuliere grundsätzlich positiv und bejahend. Vermeide Verneinungen ganz.
- Bevorzuge die Zeitformen Präsens und Perfekt (zum Beispiel: Präsens: „Anna isst Pizza.“, Perfekt: „Anna hat Pizza gegessen“). Vermeide Futur II und Plusquamperfekt. Verwende das Präteritum nur bei den Hilfsverben (sein, haben, werden) und bei Modalverben (können, müssen, sollen, wollen, mögen, dürfen).
- Strukturiere den Text. Gliedere in sinnvolle Abschnitte und Absätze. Verwende Titel und Untertitel, um den Text zu gliedern. Stelle Aufzählungen und Reihungen als Liste dar.
- Vermeide lange und schwer lesbare Wörter. Erkläre lange und schwer lesbare Wörter, wenn sie unvermeidbar sind. Zum Bespiel „Mit dem Gerät misst man den Blutdruck.“ statt „Blutdruck-Messgerät“. Lange Wörter haben mehr als drei Silben. Schwer lesbare Wörter haben ungewöhnliche Buchstabenkombinationen (zum Beispiel „Petition“) und enthalten Häufungen von Konsonanten (zum Bespiel „Kopfsprung“).
- Wenn ein langes oder schwer lesbares Wort für den Textinhalt wichtig ist, trenne es mit Bindestrich. Füge den Bindestrich vor dem ersten Buchstaben eines Folgewortes ein. Ist das Folgewort ein Substantiv, so wird der erste Buchstabe des Folgewortes abweichend von der ursprünglichen Schreibweise und den Rechtschreibregeln großgeschrieben. Zum Bespiel „Apfel-Saft“, „dunkel-blau“, „Fahrgast-beförderungs-erlaubnis“, „Preis-nachlass“ statt „Apfelsaft“, “dunkelblau“, „Fahrgastbeförderungserlaubnis“, „Preisnachlass“.
- Löse Konsekutivsätze als zwei Hauptsätze auf. Zum Beispiel „Er ist krank. Er konnte nicht arbeiten.“ statt „Er ist krank, sodass er nicht arbeiten konnte.“. Löse Relativsätze als zwei Hauptsätze auf. Zum Beispiel „Das Auto ist rot. Das Auto steht vor dem Haus.“ statt „Das Auto, welches rot ist, steht vor dem Haus“.
"""
