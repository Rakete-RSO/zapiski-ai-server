# login.py
import streamlit as st
import requests

API_URL = "http://tvoj-api-url"  # Zamenjaj s pravim URL-jem

def login_page():
    st.title("Prijava")

    with st.container(border=True):
        username = st.text_input("Uporabniško ime ali email")
        password = st.text_input("Geslo", type="password")

    if st.button("Prijava"):
        if username == "" or password == "":
            st.warning("Prosimo, izpolnite vsa polja.")
        else:
            data = {"username": username, "password": password}
            response = requests.post(f"{API_URL}/login", json=data)

            if response.status_code == 200:
                access_token = response.json().get("access_token")
                st.session_state['access_token'] = access_token
                st.session_state['logged_in'] = True
                st.success("Uspešno prijavljeni!")
                st.experimental_rerun()  # Osvežimo aplikacijo
            else:
                st.error("Neuspešna prijava. Preverite svoje podatke.")