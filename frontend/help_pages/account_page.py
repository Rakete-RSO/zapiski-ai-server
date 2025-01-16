import streamlit as st
import requests
from config import AUTH_BASE_URL


def account_page():
    """
    Display account details for the logged-in user.
    """
    st.title("Moj Račun")

    # Prepare the GraphQL query
    query = """
    query getUser($access_token: String!) {
      getUser(accessToken: $access_token) {
        id
        username
        email
        subscriptionTier
        subscribedDate
      }
    }
    """
    variables = {"access_token": st.session_state["access_token"]}  # Replace with logged-in user's email

    # Send the request
    headers = {"Authorization": f"Bearer {st.session_state['access_token']}", "Content-Type": "application/json"}
    try:
        response = requests.post(
            f"{AUTH_BASE_URL}/graphql",  # GraphQL endpoint
            json={"query": query, "variables": variables},
            headers=headers,
        )

        if response.status_code == 200:
            data = response.json()
            user_data = data.get("data", {}).get("getUser", None)
            if user_data:
                st.subheader("Vaši podatki:")
                st.write(f"Uporabniško ime: {user_data['username']}")
                st.write(f"E-pošta: {user_data['email']}")
                st.write(f"Naročniški paket: {user_data['subscriptionTier']}")
                st.write(f"Datum prijave: {user_data['subscribedDate']}")

                st.subheader("Spremenite naročniški paket:")
                current_tier = user_data["subscriptionTier"]
                tiers = ["Basic", "Pro", "Premium"]
                selected_tier = st.selectbox(
                    "Izberite novi paket:",
                    options=tiers,
                    index=tiers.index(current_tier) if current_tier in tiers else 0,
                )

                # Update button
                if st.button("Posodobite paket"):
                    update_subscription(selected_tier)
            else:
                st.error("Uporabnik ni bil najden.")
        else:
            st.error(f"Napaka pri pridobivanju podatkov: {response.status_code}")
    except Exception as e:
        st.error(f"Napaka: {e}")


def update_subscription(selected_tier):
    """
    Sends a request to update the user's subscription tier using the REST API.
    """
    url = f"{AUTH_BASE_URL}/update-subscription"
    payload = {"subscription_tier": selected_tier}
    headers = {
        "Authorization": f"Bearer {st.session_state['access_token']}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            st.success(f"Uspešno posodobljeno: {data['subscription_tier']}")
        else:
            st.error(f"Napaka pri posodabljanju paketa: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Napaka: {e}")
