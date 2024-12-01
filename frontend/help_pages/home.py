# home.py
import streamlit as st

def home_page():
    st.title("Dobrodošli na platformi za zapiske")

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        with st.container(border=True):
            st.write("Za uporabo naše platforme se prosimo prijavite.")

            # Obrazec za prijavo na začetni strani
            username = st.text_input("Uporabniško ime ali email")
            password = st.text_input("Geslo", type="password")
            if st.button("Prijava"):
                if username == "" or password == "":
                    st.warning("Prosimo, izpolnite vsa polja.")
                else:
                    # Pokličemo funkcijo za prijavo
                    from login import login_user
                    success = login_user(username, password)
                    if success:
                        st.success("Uspešno prijavljeni!")
                        st.experimental_rerun()
                    else:
                        st.error("Neuspešna prijava. Preverite svoje podatke.")

            st.write("Če še niste registrirani, se lahko registrirate tukaj:")
            if st.button("Registracija"):
                from registration import register_page
                register_page()
    else:
        st.write("Tukaj lahko nalagate slike svojih zapiskov in jih pretvorite v bolje berljivo obliko.")
        st.write("Uporabite meni na levi za navigacijo po aplikaciji.")