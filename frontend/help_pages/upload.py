import requests
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from config import CHAT_BASE_URL, DOCUMENT_BASE_URL, OPENAI_BASE_URL

def fetch_chatgpt_version(headers):
    """
    Fetch the version of ChatGPT being used via the GraphQL API.
    """
    query = """
    query {
      getChatgptVersion
    }
    """
    response = requests.post(
        f"{OPENAI_BASE_URL}/graphql",
        json={"query": query},
        headers=headers,
    )
    if response.status_code == 200:
        data = response.json()
        return data.get("data", {}).get("getChatgptVersion", "Unknown")
    else:
        return "Napaka pri pridobivanju verzije"


def upload_notes_page():
    st.title("Naloži zapiske")

    uploaded_file = st.file_uploader(
        "Izberi sliko zapiskov", type=["jpg", "png", "jpeg"]
    )
    headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
    chat_id = st.session_state.get("chat_id")

    chatgpt_version = fetch_chatgpt_version(headers)
    st.sidebar.markdown(f"### ChatGPT Verzija: {chatgpt_version}")

    display_initial_uploaded_file = True
    if chat_id:
        # Display previous messages
        if "messages" not in st.session_state:
            st.session_state["messages"] = []

        for msg in st.session_state["messages"]:
            if msg["role"] == "assistant":
                st.markdown(f"**Asistent:**\n {msg['content']}")
            else:
                st.markdown(f"**Vi:**\n {msg['content']}")
                if "uploaded_file" in msg and msg["uploaded_file"]:
                    display_initial_uploaded_file = False
                    display_file(msg["uploaded_file"])
    else:
        response = requests.post(f"{CHAT_BASE_URL}/chat", headers=headers)
        if response.status_code == 200:
            chat_id = response.json().get("chat_id")
            if chat_id:
                st.session_state["chat_id"] = chat_id
                st.session_state["messages"] = []
            else:
                st.error(
                    "Napaka pri nalaganju zapiskov. Neuspešno pridobivanje chat_id."
                )
        else:
            st.error("Napaka pri nalaganju zapiskov.")

    if uploaded_file and display_initial_uploaded_file:
        display_file(uploaded_file)

    user_input = st.text_input("Vaše sporočilo:", value="")

    # if uploaded_file is not None:
    if st.button("Pošlji"):
        if not uploaded_file and not user_input.strip():
            st.error("Naložite sliko ali pošljite sporočilo")
        else:
            files = {}
            if uploaded_file:
                files["file"] = (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type,
                )
            response = requests.post(
                f"{OPENAI_BASE_URL}/chat/messages",
                headers=headers,
                files=files,
                data={
                    "message": user_input,
                    "chat_id": chat_id,
                },
            )
            if response.status_code == 200:
                resp_data = response.json()
                user_msg = {
                    "role": "user",
                    "content": user_input.strip(),
                    "uploaded_file": uploaded_file,
                }
                assistant_msg = {
                    "role": "assistant",
                    "content": resp_data.get("content", ""),
                }
                st.session_state["messages"].append(user_msg)
                st.session_state["messages"].append(assistant_msg)
                st.rerun()  # refresh the page to show the new messages
            else:
                st.error("Napaka pri pošiljanju sporočila.")

            uploaded_file = None

    if chat_id:
        export_url = f"{DOCUMENT_BASE_URL}/export-document/{chat_id}"
        response = requests.get(export_url, headers=headers)
        if response.status_code == 200:
            st.download_button(
                label="Prenesi klepet kot dokument",
                data=response.content,
                file_name=f"{st.session_state['chat_id']}_chat_export.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        else:
            st.error("Napaka pri prenosu dokumenta.")


def display_file(file: UploadedFile):
    if file.type in ["image/jpeg", "image/png"]:
        st.image(
            file,
            caption="Naložena slika",
            use_container_width=True,
        )
    elif file.type == "application/pdf":
        st.write("Prikazovanje PDF datotek ni neposredno podprto.")
        st.download_button(
            label="Prenesite naloženi PDF",
            data=file.read(),
            file_name=file.name,
            mime="application/pdf",
        )
