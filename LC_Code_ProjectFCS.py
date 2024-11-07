import streamlit as st
import pandas as pd

# Beispiel-Daten: Liste der Lebensmittel mit allen Details
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

# Zeige die Lebensmittelübersicht (nur Name und Preis)
st.subheader("Lebensmittelübersicht")
st.dataframe(df[["Name", "Preis"]])

# Zuweisungsformular für jedes Lebensmittel
st.subheader("Lebensmittel einem Benutzer zuweisen")
for index, row in df.iterrows():
    benutzer_option = st.selectbox(
        f"Zuweisung für {row['Name']}:", 
        ["Niemand"] + benutzer, 
        index=0,
        key=index
    )
    # Aktualisiere die Zuweisung im DataFrame
    df.at[index, "Zugewiesen an"] = benutzer_option if benutzer_option != "Niemand" else None

# Zeige die aktualisierte Tabelle (nur Name und Preis)
st.subheader("Aktualisierte Lebensmittelübersicht")
st.dataframe(df[["Name", "Preis"]])

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
