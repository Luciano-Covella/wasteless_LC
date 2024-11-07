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
    st.write(f"Zuweisung für {row['Name']} (Verfügbare Menge: {row['Menge']})")
    
    # Benutzer auswählen
    remaining_quantity = row["Menge"] - len(row["Zugewiesen an"])  # Verbleibende Menge
    if remaining_quantity > 0:
        benutzer_option = st.selectbox(
            f"Wähle einen Benutzer für {row['Name']} (Verbleibend: {remaining_quantity}):",
            ["Niemand"] + benutzer,
            index=0,
            key=f"user_select_{index}_{remaining_quantity}_{row['Name']}"
        )

        if benutzer_option != "Niemand":
            # Anzahl der Einheiten auswählen
            einheiten = st.number_input(
                f"Anzahl der Einheiten für {benutzer_option} (Max: {remaining_quantity}):",
                min_value=1, 
                max_value=remaining_quantity,
                value=1,
                key=f"units_input_{index}_{remaining_quantity}_{row['Name']}"
            )

            # Button zur Bestätigung der Zuweisung
            if st.button(f"{einheiten} Einheiten zuweisen", key=f"assign_button_{index}_{remaining_quantity}_{row['Name']}"):
                # Füge die Benutzerzuweisungen hinzu
                for _ in range(einheiten):
                    df.at[index, "Zugewiesen an"].append(benutzer_option)
                st.success(f"{einheiten} Einheiten von {row['Name']} wurden {benutzer_option} zugewiesen.")

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
