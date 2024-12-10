import streamlit as st


# NOTE: Trenutno neuporabljen
def home_page(navigate_to):
    st.title("Dobrodošli na platformi za zapiske")

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        with st.container(border=True):
            st.subheader("Za uporabo naše platforme se prosimo prijavite.")
            # Add buttons (center-aligned)
            col1, col2 = st.columns([1, 1], gap="medium")

            with col1:
                if st.button("📜 Registracija", use_container_width=True):
                    navigate_to("Registracija")

            with col2:
                if st.button("🔐 Prijava", use_container_width=True):
                    navigate_to("Prijava")
    else:
        st.write(
            "Tukaj lahko nalagate slike svojih zapiskov in jih pretvorite v bolje berljivo obliko."
        )
        st.write("Uporabite meni na levi za navigacijo po aplikaciji.")

        uploaded_file = st.file_uploader(
            "Naložite svoje slike zapiskov ali dokumente (.pdf, .jpg, .png):",
            type=["pdf", "jpg", "png"],  # Allow only specific file types
        )
        if uploaded_file is not None:
            # Display the uploaded file details
            st.success(f"Uspešno naložen {uploaded_file.name}")

            # Show the image or process the file
            if uploaded_file.type in ["image/jpeg", "image/png"]:
                st.image(
                    uploaded_file, caption="Naložena slika", use_container_width=True
                )
            elif uploaded_file.type == "application/pdf":
                st.write("Prikazovanje PDF datotek ni neposredno podprto.")
                st.download_button(
                    label="Prenesite naloženi PDF",
                    data=uploaded_file.read(),
                    file_name=uploaded_file.name,
                    mime="application/pdf",
                )

