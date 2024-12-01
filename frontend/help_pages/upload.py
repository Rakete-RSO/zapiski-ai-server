# upload.py
import streamlit as st
import requests

API_URL = "http://tvoj-api-url"  # Zamenjaj s pravim URL-jem

def upload_notes_page():
    st.title("Naloži zapiske")

    uploaded_file = st.file_uploader("Izberi sliko zapiskov", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        if st.button("Naloži"):
            files = {"file": uploaded_file.getvalue()}
            headers = {
                "Authorization": f"Bearer {st.session_state['access_token']}"
            }
            response = requests.post(f"{API_URL}/upload", files=files, headers=headers)

            if response.status_code == 200:
                st.success("Zapiski uspešno naloženi!")
            else:
                st.error("Napaka pri nalaganju zapiskov.")