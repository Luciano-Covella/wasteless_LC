import streamlit as st
import json
import os

# Beispiel für eine einfache Benutzerregistrierung (ohne Verschlüsselung, nur zur Demonstration)
# In einer echten App solltest du sichere Methoden und Passwörter verwenden!

# Funktion, um Benutzer zu registrieren und zu speichern
def register_user(username, password):
    if os.path.exists("users.json"):
        with open("users.json", "r") as file:
            users = json.load(file)
    else:
        users = {}

    if username in users:
        st.error("Benutzername existiert bereits!")
        return False
    else:
        users[username] = password
        with open("users.json", "w") as file:
            json.dump(users, file)
        return True

# Funktion, um Benutzer anzumelden
def login_user(username, password):
    if os.path.exists("users.json"):
        with open("users.json", "r") as file:
            users = json.load(file)
    else:
        st.error("Keine Benutzer gefunden! Bitte registriere dich zuerst.")
        return False

    if username in users and users[username] == password:
        return True
    else:
        st.error("Falscher Benutzername oder falsches Passwort!")
        return False

# Benutzerregistrierung oder -anmeldung
st.title("WG-Manager App")

menu = st.sidebar.selectbox("Menü", ["Anmelden", "Registrieren"])
username = st.sidebar.text_input("Benutzername")
password = st.sidebar.text_input("Passwort", type="password")

if menu == "Registrieren":
    if st.sidebar.button("Registrieren"):
        if register_user(username, password):
            st.success("Erfolgreich registriert! Bitte melde dich an.")
elif menu == "Anmelden":
    if st.sidebar.button("Anmelden"):
        if login_user(username, password):
            st.success(f"Willkommen, {username}!")
            # Nach erfolgreicher Anmeldung werden die WG-Daten geladen
            data_file = f"{username}_data.json"

            if os.path.exists(data_file):
                with open(data_file, "r") as file:
                    st.session_state["data"] = json.load(file)
            else:
                st.session_state["data"] = {}

            # Beispiel für Datenverarbeitung
            st.write("Hier kannst du deine WG-Daten eingeben und bearbeiten.")
            wg_name = st.text_input("Name der WG", st.session_state["data"].get("wg_name", ""))
            mitbewohner = st.text_area("Mitbewohner (Komma getrennt)", ", ".join(st.session_state["data"].get("mitbewohner", [])))

            if st.button("Daten speichern"):
                st.session_state["data"]["wg_name"] = wg_name
                st.session_state["data"]["mitbewohner"] = mitbewohner.split(", ")
                with open(data_file, "w") as file:
                    json.dump(st.session_state["data"], file)
                st.success("Daten gespeichert!")
