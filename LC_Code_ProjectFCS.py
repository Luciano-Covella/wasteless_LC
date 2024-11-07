import streamlit as st
import pandas as pd
import streamlit_dragndrop as dnd

# Beispiel-Daten
lebensmittel_data = [
    {"Name": "Apfel", "Preis": 2.5, "Menge": 1, "Ablaufdatum": "2024-11-10"},
    {"Name": "Milch", "Preis": 1.2, "Menge": 1, "Ablaufdatum": "2024-11-05"},
    {"Name": "Brot", "Preis": 3.0, "Menge": 1, "Ablaufdatum": "2024-11-03"}
]

# Beispiel-Benutzerliste
benutzer = ["Alice", "Bob", "Charlie"]

# Konvertiere die Lebensmittel-Daten in ein DataFrame
df = pd.DataFrame(lebensmittel_data)

# Streamlit-Anwendung
st.title("Lebensmittel-Zuweisung per Drag-and-Drop")

# Drag-and-Drop-Funktion
st.subheader("Ziehen Sie Lebensmittel zu den Benutzern")

# Erstelle die Drag-and-Drop-Zonen
zuweisungen = {}

for b in benutzer:
    st.write(f"Lebensmittel für {b}:")
    zuweisungen[b] = dnd.dropzone(accepted_types=["text"], key=b)

# Zeige die Liste der Lebensmittel, die per Drag-and-Drop zugewiesen werden können
st.subheader("Lebensmittel:")
for lebensmittel in df["Name"]:
    dnd.draggable(label=lebensmittel, value=lebensmittel)

# Speichern und Anzeigen der Zuweisungen
st.subheader("Zugewiesene Lebensmittel")
for b in benutzer:
    st.write(f"{b}: {zuweisungen[b]}")
