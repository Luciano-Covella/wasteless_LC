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
    # Verbleibende Menge berechnen
    remaining_quantity = row["Menge"] - len(row["Zugewiesen an"])
    
    # Nur fortfahren, wenn noch Einheiten verfügbar sind
    if remaining_quantity > 0:
        st.write(f"Zuweisung für {row['Name']} (Verfügbare Menge: {remaining_quantity})")
        
        # Erstelle eine horizontale Anordnung der Benutzer mit `st.columns`
        columns = st.columns(len(benutzer))
        
        # Benutzer einzeln die Anzahl zuweisen
        for col, benutzer_name in zip(columns, benutzer):
            with col:
                # Zeige den Benutzernamen
                st.write(benutzer_name)
                
                # Slider zur Zuweisung der Anzahl der Einheiten
                einheiten = st.slider(
                    f"Anzahl der Einheiten für {benutzer_name}",
                    min_value=0,
                    max_value=remaining_quantity,
                    value=0,
                    key=f"slider_{index}_{benutzer_name}"
                )
                
                # Wenn Einheiten zugewiesen werden, füge sie zur Zuweisungsliste hinzu
                if einheiten > 0:
                    df.at[index, "Zugewiesen an"].extend([benutzer_name] * einheiten)
                    remaining_quantity -= einheiten

    else:
        # Wenn keine Einheiten mehr verfügbar sind, informiere den Benutzer
        st.write(f"Alle {row['Name']} sind zugewiesen.")

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
