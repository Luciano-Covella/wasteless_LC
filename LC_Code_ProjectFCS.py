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

# CSS-Stil für den dicken Strich
st.markdown("""
    <style>
    .divider {
        border-top: 4px solid #444;
        margin: 20px 0;
    }
    .stButton > button.plus-button {
        border: 2px solid green !important;
        color: green !important;
    }
    .stButton > button.minus-button {
        border: 2px solid red !important;
        color: red !important;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit-Anwendung
st.title("Lebensmittel-Zuweisung an Benutzer")

# Zeige die Lebensmittelübersicht (Name, Preis, Anzahl der Käufe) ohne Zeilennummerierung
st.subheader("Lebensmittelübersicht")
st.dataframe(df[["Anzahl der Käufe", "Name", "Preis"]].reset_index(drop=True))

# Zuweisungsformular für jedes Lebensmittel
st.subheader("Lebensmittel einem Benutzer zuweisen")
for index, row in df.iterrows():
    # Gesamtmenge des Lebensmittels
    total_quantity = row["Menge"]

    # Berechne die aktuell zugewiesene Gesamtmenge
    zugewiesene_menge = sum([st.session_state.get(f"{benutzer_name}_{index}", 0) for benutzer_name in benutzer])
    remaining_quantity = total_quantity - zugewiesene_menge
    
    st.write(f"Zuweisung für {row['Name']} (Verfügbare Menge: {remaining_quantity})")
    
    # Erstelle eine horizontale Anordnung der Benutzer mit `st.columns`
    columns = st.columns(len(benutzer))
    
    # Benutzer einzeln die Anzahl zuweisen
    for col, benutzer_name in zip(columns, benutzer):
        with col:
            # Zeige den Benutzernamen
            st.write(benutzer_name)
            
            # Initialisiere den Zähler für die zugewiesene Anzahl von Einheiten, falls nicht vorhanden
            if f"{benutzer_name}_{index}" not in st.session_state:
                st.session_state[f"{benutzer_name}_{index}"] = 0

            # Zeige die aktuelle Anzahl
            einheiten = st.session_state[f"{benutzer_name}_{index}"]

            # Die "+" Taste ist nur aktiv, wenn noch Einheiten verfügbar sind
            plus_disabled = remaining_quantity <= 0
            if st.button("➕", key=f"plus_{index}_{benutzer_name}", disabled=plus_disabled):
                if einheiten < total_quantity:
                    einheiten += 1
                    st.session_state[f"{benutzer_name}_{index}"] = einheiten

            # Die "-" Taste ist nur aktiv, wenn die Anzahl größer als 0 ist
            minus_disabled = einheiten <= 0
            if st.button("➖", key=f"minus_{index}_{benutzer_name}", disabled=minus_disabled):
                if einheiten > 0:
                    einheiten -= 1
                    st.session_state[f"{benutzer_name}_{index}"] = einheiten

            # Aktualisiere die Zuweisungsliste entsprechend der Anzahl
            df.at[index, "Zugewiesen an"].extend([benutzer_name] * (einheiten - len(df.at[index, "Zugewiesen an"])))

            # Zeige die aktuelle Zuweisung für den Benutzer
            st.write(f"Anzahl für {benutzer_name}: {einheiten}")
    
    # Füge den dicken Strich als Trennlinie zwischen den Produkten ein
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Berechnung der anteiligen Kosten pro Benutzer
st.subheader("Kosten pro Benutzer")
kosten_pro_benutzer = {benutzer_name: 0 for benutzer_name in benutzer}

# Berechne die Kosten für jeden Benutzer basierend auf den zugewiesenen Einheiten der Lebensmittel
for index, row in df.iterrows():
    preis_pro_einheit = row["Preis"] / row["Menge"]
    for benutzer_name in benutzer:
        anzahl_einheiten = st.session_state.get(f"{benutzer_name}_{index}", 0)
        kosten_pro_benutzer[benutzer_name] += anzahl_einheiten * preis_pro_einheit

# Zeige die anteiligen Kosten für jeden Benutzer
for benutzer_name, kosten in kosten_pro_benutzer.items():
    st.write(f"{benutzer_name}: {kosten:.2f} €")
