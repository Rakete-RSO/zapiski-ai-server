# app.py
import streamlit as st
from help_pages.login import login_page
from help_pages.registration import register_page
from help_pages.home import home_page
from help_pages.upload import upload_notes_page


# Function to switch pages
def navigate_to(page_name):
    st.session_state["current_page"] = page_name

def main():
    # Initialize session state for login and navigation
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    print("Reruning")

    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Domov"  # Default page
        print(st.session_state["current_page"])

    print(st.session_state["current_page"])
    # Sidebar navigation menu
    menu = ["Domov", "Prijava", "Registracija"]

    # Select the menu item
    selected_menu = st.sidebar.selectbox(
        "Meni:", menu, index=menu.index(st.session_state["current_page"])
    )

    if selected_menu != st.session_state["current_page"]:
        st.session_state["current_page"] = selected_menu


    # Render the selected page
    if st.session_state["current_page"] == "Domov":
        home_page(navigate_to)
    elif st.session_state["current_page"] == "Prijava":
        if st.session_state['logged_in']:
            st.warning("Že ste prijavljeni.")
            home_page(navigate_to)
        else:
            login_page(navigate_to)
    elif st.session_state["current_page"] == "Registracija":
        if st.session_state['logged_in']:
            st.warning("Ste že prijavljeni.")
            home_page(navigate_to)
        else:
            register_page(navigate_to)
    elif st.session_state["current_page"] == "Odjava":
        st.session_state['logged_in'] = False
        st.session_state['access_token'] = None
        st.success("Uspešno odjavljeni.")
        navigate_to("Domov")
        home_page(navigate_to)
    elif st.session_state["current_page"] == "Nalaganje zapiskov":
        if st.session_state['logged_in']:
            upload_notes_page(navigate_to)
        else:
            st.warning("Prosimo, prijavite se za dostop do te strani.")
            login_page(navigate_to)


if __name__ == "__main__":
    main()