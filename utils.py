import streamlit as st
import requests
import pandas as pd

ODK_URL = st.secrets["ODK_URL"]
USERNAME = st.secrets["USERNAME"]
PASSWORD = st.secrets["PASSWORD"]
PROJECT_ID = st.secrets["PROJECT_ID"]

@st.cache_data(ttl=300)
def load_data(form_id):
    url = f"{ODK_URL}/v1/projects/{PROJECT_ID}/forms/{form_id}/submissions.csv"
    
    response = requests.get(url, auth=(USERNAME, PASSWORD))

    if response.status_code != 200:
        st.error(f"Error: {response.status_code}")
        return pd.DataFrame()

    import io

    if response.status_code != 200:
        return pd.DataFrame()

    df = pd.read_csv(io.StringIO(response.text))

    return df
def load_repeat_data(form_id, entity_url):
    url = (
        f"{ODK_URL}/v1/projects/{PROJECT_ID}"
        f"/forms/{form_id}.svc/{entity_url}"
    )
    response = requests.get(
        url,
        auth=(USERNAME, PASSWORD)
    )
    if response.status_code != 200:
        st.error(f"{entity_url}: {response.status_code}")
        return pd.DataFrame()
    data = response.json()
    if "value" not in data:
        return pd.DataFrame()
    return pd.json_normalize(data["value"])
