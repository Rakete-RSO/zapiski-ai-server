# app.py
import time

import requests
import streamlit as st
from config import AUTH_BASE_URL

from help_pages.home import home_page
from help_pages.login import login_page
from help_pages.registration import register_page
from help_pages.upload import upload_notes_page
from streamlit_cookies_controller import CookieController


# Function to switch pages
def navigate_to(page_name):
    st.session_state["current_page"] = page_name

def logout_user():
    """Resets the session state to log out the user."""
    st.session_state["logged_in"] = False
    st.session_state["access_token"] = None
    st.session_state["messages"] = []
    st.session_state["chat_id"] = None
    st.success("Uspešno odjavljeni.")
    navigate_to("Nalaganje zapiskov")
    st.rerun()

def check_access_token(access_token):
    try:
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(f"{AUTH_BASE_URL}/verify-token", headers=headers)

        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        return False

def main():
    # Initialize session state for login and navigation
    controller = CookieController()
    access_token = controller.get('access_token')
    st.session_state["access_token"] = access_token
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = check_access_token(access_token)

    # This part seems unnecessary but it isn't
    if access_token:
        st.session_state["logged_in"] = check_access_token(access_token)

    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Nalaganje zapiskov"  # Default page

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Sidebar navigation menu
    menu = [
        # "Domov",  EDIT (tjaz): za enkrat sem disablal route domov, ter vse preusmerim na Nalaganje zapiskov
        "Prijava",
        "Registracija",
        "Nalaganje zapiskov",
    ]

    if (st.session_state["logged_in"]):
        menu = [
            # "Domov",  EDIT (tjaz): za enkrat sem disablal route domov, ter vse preusmerim na Nalaganje zapiskov
            "Prijava",
            "Registracija",
            "Nalaganje zapiskov",
            "Odjava"
        ]

    # Select the menu item
    selected_menu = st.sidebar.selectbox(
        "Meni:", menu, index=menu.index(st.session_state["current_page"])
    )

    if selected_menu != st.session_state["current_page"]:
        st.session_state["current_page"] = selected_menu

    # Render the selected page
    elif st.session_state["current_page"] == "Prijava":
        if st.session_state["logged_in"]:
            # st.warning("Ste že prijavljeni.")
            upload_notes_page()
        else:
            login_page(controller)
    elif st.session_state["current_page"] == "Registracija":
        if st.session_state["logged_in"]:
            # st.warning("Ste že prijavljeni.")
            upload_notes_page()
        else:
            register_page(navigate_to)
    elif st.session_state["current_page"] == "Odjava":
        logout_user()
    elif st.session_state["current_page"] == "Nalaganje zapiskov":
        if st.session_state["logged_in"]:
            upload_notes_page()
        else:
            st.warning("Prosimo, prijavite se za dostop do te strani.")
            login_page(controller)


if __name__ == "__main__":
    main()
