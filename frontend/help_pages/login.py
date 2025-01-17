import time

import requests
import streamlit as st

from config import AUTH_BASE_URL


def login_user(username: str, password: str, cookie_controller) -> None:
    """Handles the login process by sending a request to the auth server."""
    # Check if fields are empty
    if username == "" or password == "":
        st.warning("Prosimo, izpolnite vsa polja.")
        return

    # Create the request payload
    data = {"username": username, "email": username, "password": password}

    try:
        # Send a POST request to the authentication server
        response = requests.post(f"{AUTH_BASE_URL}/login", json=data)
        # Handle the response
        if response.status_code == 200:
            # Extract the access token and update session state
            access_token = response.json().get("access_token")
            if access_token:
                st.session_state["access_token"] = access_token
                cookie_controller.set("access_token", access_token)
                st.session_state["logged_in"] = True
                st.success("Uspešno prijavljeni!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Napaka strežnika: Dostopni žeton ni bil vrnjen.")
        else:
            st.error("Neuspešna prijava. Preverite svoje podatke.")
    except requests.exceptions.RequestException as e:
        # Handle any exceptions during the request
        st.error(f"Napaka pri povezovanju s strežnikom: {str(e)}")


def login_page(cookie_controller):
    """Renders the login page."""
    st.title("Prijava")

    with st.container():
        username = st.text_input("Uporabniško ime ali email")
        password = st.text_input("Geslo", type="password")

    if st.button("Prijava"):
        login_user(username, password, cookie_controller)
