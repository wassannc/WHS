import streamlit as st
import requests
import pandas as pd

ODK_URL = st.secrets["ODK_URL"]
USERNAME = st.secrets["USERNAME"]
PASSWORD = st.secrets["PASSWORD"]
PROJECT_ID = st.secrets["PROJECT_ID"]

import io

@st.cache_data(ttl=300)
def load_odk_data(form_id):

    url = f"{ODK_URL}/v1/projects/{PROJECT_ID}/forms/{form_id}.csv"

    st.write("FORM ID =", repr(form_id))
    st.write("URL =", url)

    response = requests.get(
        url,
        auth=(USERNAME, PASSWORD)
    )

    st.write("Status:", response.status_code)

    if response.status_code != 200:
        return pd.DataFrame()

    df = pd.read_csv(io.StringIO(response.text))

    st.write("Rows loaded:", len(df))

    return df
