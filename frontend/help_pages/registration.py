# register.py
import streamlit as st
import requests

API_URL = "http://tvoj-api-url"  # Zamenjaj s pravim URL-jem

def register_page():
    st.title("Registracija")
    with st.container(border=True):
        username = st.text_input("Uporabniško ime")
        email = st.text_input("Email")
        password = st.text_input("Geslo", type="password")
        confirm_password = st.text_input("Potrdi geslo", type="password")

    if st.button("Registracija"):
        if username == "" or email == "" or password == "" or confirm_password == "":
            st.warning("Prosimo, izpolnite vsa polja.")
        elif password != confirm_password:
            st.warning("Gesli se ne ujemata.")
        else:
            data = {
                "username": username,
                "email": email,
                "password": password
            }
            response = requests.post(f"{API_URL}/register", json=data)

            if response.status_code == 200 or response.status_code == 201:
                st.success("Uspešno registrirani! Sedaj se lahko prijavite.")
            else:
                error_detail = response.json().get('detail', 'Neznana napaka')
                st.error(f"Napaka pri registraciji: {error_detail}")