# app.py

import requests
import streamlit as st
from streamlit_cookies_controller import CookieController

from config import AUTH_BASE_URL, CHAT_BASE_URL
from help_pages.login import login_page
from help_pages.registration import register_page
from help_pages.upload import upload_notes_page

# Function to switch pages
def navigate_to(page_name):
    st.session_state["current_page"] = page_name

def logout_user(controller):
    """Resets the session state to log out the user."""
    st.session_state["logged_in"] = False
    st.session_state["access_token"] = None

    controller.remove("access_token")

    st.session_state["messages"] = []
    st.session_state["chat_id"] = None
    st.success("Uspešno odjavljeni.")
    navigate_to("Nalaganje zapiskov")
    st.rerun()


def check_access_token(access_token):
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{AUTH_BASE_URL}/verify-token", headers=headers)

        if response.status_code == 200:
            return True
        else:
            return False
    except Exception:
        return False


def fetch_chats(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.get(f"{CHAT_BASE_URL}/chat", headers=headers)
        if response.status_code == 200:
            return response.json()  # Expecting a list of chats
        else:
            st.error(f"Failed to fetch chats: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"An error occurred while fetching chats: {e}")
        return []


def get_chat_messages(access_token, chat_id):
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.get(f"{CHAT_BASE_URL}/chat/{chat_id}", headers=headers)
        if response.status_code == 200:
            return response.json()  # Expecting a list of chats
        else:
            st.error(f"Failed to fetch chats: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"An error occurred while fetching chats: {e}")
        return []


def main():
    # Initialize session state for login and navigation
    controller = CookieController()
    access_token = controller.get("access_token")
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

    if "previous_selected_chat_id" not in st.session_state:
        st.session_state["previous_selected_chat_id"] = ""

    # Sidebar navigation menu
    menu = [
        # "Domov",  EDIT (tjaz): za enkrat sem disablal route domov, ter vse preusmerim na Nalaganje zapiskov
        "Prijava",
        "Registracija",
        "Nalaganje zapiskov",
    ]

    if st.session_state["logged_in"]:
        menu = [
            # "Domov",  EDIT (tjaz): za enkrat sem disablal route domov, ter vse preusmerim na Nalaganje zapiskov
            "Prijava",
            "Registracija",
            "Nalaganje zapiskov",
            "Odjava",
        ]

    # Select the menu item
    selected_menu = st.sidebar.selectbox(
        "Meni:", menu, index=menu.index(st.session_state["current_page"])
    )

    if selected_menu != st.session_state["current_page"]:
        st.session_state["current_page"] = selected_menu

    chat_chooser()

    # Render the selected page
    if st.session_state["current_page"] == "Prijava":
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
        logout_user(controller)
    elif st.session_state["current_page"] == "Nalaganje zapiskov":
        if st.session_state["logged_in"]:
            upload_notes_page()
        else:
            st.warning("Prosimo, prijavite se za dostop do te strani.")
            login_page(controller)


def chat_chooser():
    if st.session_state["logged_in"]:
        st.sidebar.markdown("## Vaši Chat-i")

        # Fetch chats only once and store them in session state
        if "chats" not in st.session_state:
            st.write("Fetching chats...")
            chats = fetch_chats(st.session_state["access_token"])
            st.session_state["chats"] = chats
        else:
            chats = st.session_state["chats"]

        chat_name_to_id_mapping = {
            chat["name"]: chat["id"] for chat in chats if chat["name"]
        }

        if chats:
            # Create a list of chat names
            chat_options = list(chat_name_to_id_mapping.keys())
            # Add an option to create a new chat
            chat_options.append("Ustvari nov Chat")

            # Display the selectbox
            selected_chat = st.sidebar.selectbox("Izberi Chat:", chat_options)

            if selected_chat == "Ustvari nov Chat":
                navigate_to("Nalaganje zapiskov")
                st.session_state["chat_id"] = None
                st.session_state["previous_selected_chat_id"] = ""
                st.session_state["messages"] = []
                # st.rerun()
            else:
                # Find the selected chat's ID
                if selected_chat not in chat_name_to_id_mapping:
                    st.error(f"Chat {selected_chat} ne obstaja. This is very wierd.")
                current_chat_id = chat_name_to_id_mapping[selected_chat]
                if current_chat_id != st.session_state["previous_selected_chat_id"]:
                    st.session_state["chat_id"] = current_chat_id
                    navigate_to("Nalaganje zapiskov")  # Navigate to upload notes page
                    st.session_state["previous_selected_chat_id"] = current_chat_id

                    chat_messages = get_chat_messages(
                        st.session_state["access_token"], current_chat_id
                    )
                    st.session_state["messages"] = chat_messages["messages"]  # type: ignore

                    # st.rerun()
        else:
            st.sidebar.write("Ni najdenih chat-ov.")


if __name__ == "__main__":
    main()
