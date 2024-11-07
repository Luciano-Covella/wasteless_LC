import streamlit as st
import pandas as pd

# Beispiel-Daten: Liste der Lebensmittel mit Name, Preis, Menge und Ablaufdatum
lebensmittel_data = [
    {"Name": "Apfel", "Preis": 2.5, "Menge": 1, "Ablaufdatum": "2024-11-10"},
    {"Name": "Milch", "Preis": 1.2, "Menge": 1, "Ablaufdatum": "2024-11-05"},
    {"Name": "Brot", "Preis": 3.0, "Menge": 1, "Ablaufdatum": "2024-11-03"}
]

# Liste der Benutzer
benutzer = ["Alice", "Bob", "Charlie"]

# Konvertiere die Lebensmittel-Daten in ein Pandas DataFrame
df = pd.DataFrame(lebensmittel_data)

# Füge eine Spalte für die Benutzerzuweisung hinzu
df["Zugewiesen an"] = None

# Streamlit-Anwendung
st.title("Lebensmittel-Zuweisung an Benutzer")

# Zeige die Lebensmittelübersicht in einer Tabelle
st.subheader("Lebensmittelübersicht")
st.dataframe(df)

# Auswahlboxen zur Zuweisung eines Lebensmittels an einen Benutzer
st.subheader("Lebensmittel einem Benutzer zuweisen")
lebensmittel_option = st.selectbox("Wähle ein Lebensmittel", df["Name"])
benutzer_option = st.selectbox("Wähle einen Benutzer", benutzer)

# Button zur Bestätigung der Zuweisung
if st.button("Zuweisen"):
    # Finde den Index des ausgewählten Lebensmittels und weise den Benutzer zu
    index = df[df["Name"] == lebensmittel_option].index[0]
    df.at[index, "Zugewiesen an"] = benutzer_option
    st.success(f"{lebensmittel_option} wurde {benutzer_option} zugewiesen.")

# Zeige die aktualisierte Tabelle mit den Zuweisungen
st.subheader("Aktualisierte Lebensmittelübersicht")
st.dataframe(df)

# Berechnung der anteiligen Kosten pro Benutzer
st.subheader("Anteiliges Bezahlen")
kosten_pro_benutzer = {}

# Berechne die Kosten für jeden Benutzer basierend auf den zugewiesenen Lebensmitteln
for b in benutzer:
    gesamtpreis = df[df["Zugewiesen an"] == b]["Preis"].sum()
    kosten_pro_benutzer[b] = gesamtpreis

# Zeige die anteiligen Kosten für jeden Benutzer
st.subheader("Kosten pro Benutzer")
for b, kosten in kosten_pro_benutzer.items():
    st.write(f"{b}: {kosten:.2f} €")
