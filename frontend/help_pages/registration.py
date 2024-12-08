# register.py
import time

import streamlit as st
import requests
import bcrypt
from config import API_URL  # Import API_URL from config.py



def validate_password(password: str) -> bool:
    """
    Validate the password against your backend's criteria:
    - At least 8 characters long
    - Includes uppercase, lowercase, a number, and a special character
    """
    if len(password) < 8:
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for char in password):
        return False
    return True

def register_user(username: str, email: str, password: str, navigate_to):
    """
    Handle the registration process by sending a POST request to the auth server.
    """

    # Create the request payload
    data = {
        "username": username,
        "email": email,
        "password": password,
    }

    try:
        # Send the POST request to the authentication server
        print("sending POST request")
        response = requests.post(f"{API_URL}/register", json=data)
        print("POST response")

        # Handle the response
        if response.status_code in [200, 201]:
            st.success("Uspešno registrirani! Sedaj se lahko prijavite.")
            time.sleep(1)
            navigate_to("Prijava")
        else:
            error_detail = response.json().get("detail", "Neznana napaka")
            st.error(f"Napaka pri registraciji: {error_detail}")
    except requests.exceptions.RequestException as e:
        st.error(f"Napaka pri povezovanju s strežnikom: {str(e)}")


def register_page(navigate_to):
    st.title("Registracija")
    with st.container(border=True):
        username = st.text_input("Uporabniško ime")
        email = st.text_input("Email")
        password = st.text_input("Geslo", type="password")
        confirm_password = st.text_input("Potrdi geslo", type="password")

    if st.button("Registracija"):
        print("whatever")
        if username == "" or email == "" or password == "" or confirm_password == "":
            st.warning("Prosimo, izpolnite vsa polja.")
        elif password != confirm_password:
            st.warning("Gesli se ne ujemata.")
        elif not validate_password(password):
            st.warning(
                "Geslo mora biti dolgo najmanj 8 znakov ter vsebovati veliko začetnico, malo začetnico, številko in poseben znak."
            )
        else:
            register_user(username, email, password, navigate_to)