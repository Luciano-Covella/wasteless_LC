import streamlit as st
import pandas as pd

# Beispiel-Daten (diese könnten aus einer Datenbank geladen werden)
lebensmittel_data = [
    {"Name": "Apfel", "Preis": 2.5, "Menge": 1, "Ablaufdatum": "2024-11-10"},
    {"Name": "Milch", "Preis": 1.2, "Menge": 1, "Ablaufdatum": "2024-11-05"},
    {"Name": "Brot", "Preis": 3.0, "Menge": 1, "Ablaufdatum": "2024-11-03"}
]

# Beispiel-Benutzerliste
benutzer = ["Alice", "Bob", "Charlie"]

# Konvertiere die Lebensmittel-Daten in ein DataFrame
df = pd.DataFrame(lebensmittel_data)

# Erstelle eine Spalte für die Benutzerzuweisung im DataFrame
df["Zugewiesen an"] = None

# Streamlit-Anwendung
st.title("Lebensmittel-Zuweisung an Benutzer")

# Zeige die Tabelle mit den Lebensmitteln
st.subheader("Lebensmittelübersicht")
st.dataframe(df)

# Benutzer-Auswahl
st.subheader("Lebensmittel einem Benutzer zuweisen")
lebensmittel_option = st.selectbox("Wähle ein Lebensmittel", df["Name"])
benutzer_option = st.selectbox("Wähle einen Benutzer", benutzer)

# Button zum Zuweisen
if st.button("Zuweisen"):
    # Finde den Index des ausgewählten Lebensmittels
    index = df[df["Name"] == lebensmittel_option].index[0]
    # Weise den Benutzer zu
    df.at[index, "Zugewiesen an"] = benutzer_option
    st.success(f"{lebensmittel_option} wurde {benutzer_option} zugewiesen.")

# Zeige die aktualisierte Tabelle
st.subheader("Aktualisierte Lebensmittelübersicht")
st.dataframe(df)

# Berechnung der anteiligen Kosten für jeden Benutzer
st.subheader("Anteiliges Bezahlen")
kosten_pro_benutzer = {}

for b in benutzer:
    # Summiere die Preise für die Lebensmittel, die dem Benutzer zugewiesen wurden
    gesamtpreis = df[df["Zugewiesen an"] == b]["Preis"].sum()
    kosten_pro_benutzer[b] = gesamtpreis

# Zeige die Kosten für jeden Benutzer
for b, kosten in kosten_pro_benutzer.items():
    st.write(f"{b}: {kosten} €")
