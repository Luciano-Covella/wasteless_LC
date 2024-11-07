import streamlit as st
import pandas as pd

# Beispiel-Daten: Liste der Lebensmittel mit allen Details
lebensmittel_data = [
    {"Name": "Apfel", "Preis": 2.5, "Menge": 5, "Ablaufdatum": "2024-11-10", "Anzahl der Käufe": 5},
    {"Name": "Milch", "Preis": 1.2, "Menge": 3, "Ablaufdatum": "2024-11-05", "Anzahl der Käufe": 3},
    {"Name": "Brot", "Preis": 3.0, "Menge": 7, "Ablaufdatum": "2024-11-03", "Anzahl der Käufe": 7}
]

# Liste der Benutzer
benutzer = ["Alice", "Bob", "Charlie"]

# Konvertiere die Lebensmittel-Daten in ein Pandas DataFrame
df = pd.DataFrame(lebensmittel_data)

# Füge eine Spalte für die Benutzerzuweisung hinzu
df["Zugewiesen an"] = [[] for _ in range(len(df))]  # Leere Listen für Zuweisungen

# Streamlit-Anwendung
st.title("Lebensmittel-Zuweisung an Benutzer")

# Zeige die Lebensmittelübersicht (Name, Preis, Anzahl der Käufe) ohne Zeilennummerierung
st.subheader("Lebensmittelübersicht")
st.dataframe(df[["Anzahl der Käufe", "Name", "Preis"]].reset_index(drop=True))

# Zuweisungsformular für jedes Lebensmittel
st.subheader("Lebensmittel einem Benutzer zuweisen")
for index, row in df.iterrows():
    # Gesamtmenge und verbleibende Menge berechnen
    total_quantity = row["Menge"]
    remaining_quantity = total_quantity - len(row["Zugewiesen an"])
    
    st.write(f"Zuweisung für {row['Name']} (Verfügbare Menge: {remaining_quantity})")
    
    # Erstelle eine horizontale Anordnung der Benutzer mit `st.columns`
    columns = st.columns(len(benutzer))
    
    # Benutzer einzeln die Anzahl zuweisen
    for col, benutzer_name in zip(columns, benutzer):
        with col:
            # Zeige den Benutzernamen
            st.write(benutzer_name)
            
            # Initialisiere den Zähler für die zugewiesene Anzahl von Einheiten
            if f"{benutzer_name}_{index}" not in st.session_state:
                st.session_state[f"{benutzer_name}_{index}"] = 0

            # Zeige die aktuelle Anzahl
            einheiten = st.session_state[f"{benutzer_name}_{index}"]

            # Die "+" Taste erhöht die Anzahl, aber nur, wenn die Gesamtanzahl nicht überschritten wird
            if st.button("➕", key=f"plus_{index}_{benutzer_name}", disabled=remaining_quantity <= 0):
                if einheiten < total_quantity:
                    einheiten += 1
                    st.session_state[f"{benutzer_name}_{index}"] = einheiten
                    remaining_quantity -= 1  # Verringere die verfügbare Menge

            # Die "-" Taste verringert die Anzahl, aber nur, wenn die Anzahl größer als 0 ist
            if st.button("➖", key=f"minus_{index}_{benutzer_name}", disabled=einheiten <= 0):
                if einheiten > 0:
                    einheiten -= 1
                    st.session_state[f"{benutzer_name}_{index}"] = einheiten
                    remaining_quantity += 1  # Erhöhe die verfügbare Menge

            # Aktualisiere die Zuweisungsliste entsprechend der Anzahl
            zugewiesen = [benutzer_name] * einheiten
            df.at[index, "Zugewiesen an"] = zugewiesen

            # Zeige die aktuelle Zuweisung für den Benutzer
            st.write(f"Anzahl für {benutzer_name}: {einheiten}")

# Zeige die aktualisierte Tabelle (Name, Preis, Anzahl der Käufe) ohne Zeilennummerierung
st.subheader("Aktualisierte Lebensmittelübersicht")
st.dataframe(df[["Anzahl der Käufe", "Name", "Preis"]].reset_index(drop=True))

# Berechnung der anteiligen Kosten pro Benutzer
st.subheader("Kosten pro Benutzer")
kosten_pro_benutzer = {benutzer: 0 for benutzer in benutzer}

# Berechne die Kosten für jeden Benutzer basierend auf den zugewiesenen Einheiten der Lebensmittel
for index, row in df.iterrows():
    preis_pro_einheit = row["Preis"] / row["Menge"]
    for zugewiesener_benutzer in row["Zugewiesen an"]:
        kosten_pro_benutzer[zugewiesener_benutzer] += preis_pro_einheit

# Zeige die anteiligen Kosten für jeden Benutzer
for b, kosten in kosten_pro_benutzer.items():
    st.write(f"{b}: {kosten:.2f} €")
