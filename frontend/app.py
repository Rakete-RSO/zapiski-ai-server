# app.py
import streamlit as st
from help_pages.login import login_page
from help_pages.registration import register_page
from help_pages.home import home_page
from help_pages.upload import upload_notes_page

def main():
    st.set_page_config(page_title="Aplikacija za zapiske")

    # Uporabimo session_state za shranjevanje stanja prijave
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    # Navigacija
    if st.session_state['logged_in']:
        menu = ["Domov", "Nalaganje zapiskov", "Odjava"]
    else:
        menu = ["Domov", "Prijava", "Registracija"]

    choice = st.sidebar.selectbox("Meni", menu)

    if choice == "Domov":
        home_page()
    elif choice == "Prijava":
        if st.session_state['logged_in']:
            st.warning("Že ste prijavljeni.")
        else:
            login_page()
    elif choice == "Registracija":
        if st.session_state['logged_in']:
            st.warning("Ste že prijavljeni.")
        else:
            register_page()
    elif choice == "Odjava":
        st.session_state['logged_in'] = False
        st.session_state['access_token'] = None
        st.success("Uspešno odjavljeni.")
        st.experimental_rerun()
    elif choice == "Nalaganje zapiskov":
        if st.session_state['logged_in']:
            upload_notes_page()
        else:
            st.warning("Prosimo, prijavite se za dostop do te strani.")
            login_page()

if __name__ == '__main__':
    main()