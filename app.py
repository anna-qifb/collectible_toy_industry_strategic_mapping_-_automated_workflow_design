import streamlit as st
import requests
import json
import os

# Load mock data (fallback or for local testing/demo)
MOCK_FILE = "JSON full 14032026.json"

@st.cache_data
def load_mock_data():
    if os.path.exists(MOCK_FILE):
        with open(MOCK_FILE, 'r') as f:
            return json.load(f)
    return {"message": "No mock data found"}

# Your n8n production webhook URL (keep secret!)
# N8N_WEBHOOK_URL = st.secrets.get("N8N_WEBHOOK_URL", "https://your-n8n-instance.com/webhook/bf525c9a-4d06-4c6b-bdcf-c4c8bf3c3044")
N8N_WEBHOOK_URL = st.secrets.get("N8N_WEBHOOK_URL", "http://localhost:5678/webhook/bf525c9a-4d06-4c6b-bdcf-c4c8bf3c3044")

st.title("My App with n8n Backend + Mock Data")

# Example: user input form
user_input = st.text_input("Enter something to process:")

if st.button("Process via n8n"):
    if user_input:
        payload = {"Input your company name: ": user_input}

        try:
            # Try real n8n webhook
            response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=15)
            response.raise_for_status()
            result = response.json()
            st.success("n8n processed it!")
            st.json(result)
        except Exception as e:
            st.warning(f"n8n error: {e} → falling back to mock data")
            mock = load_mock_data()
            st.json(mock)
    else:
        st.info("Enter something first!")

# Optional: show raw mock data for demo
if st.checkbox("Show mock JSON data"):
    st.json(load_mock_data())
