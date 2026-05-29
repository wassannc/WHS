import streamlit as st
import pandas as pd

from config import FORMS
from utils import load_odk_data

st.set_page_config(page_title="Project Dashboard", layout="wide")

# ---------------- SIDEBAR ----------------

st.sidebar.title("Menu")

menu_items = ["Submission Matrix"] + list(FORMS.keys())

page = st.sidebar.radio("Go to", menu_items)

# ---------------- SUBMISSION MATRIX ----------------

if page == "Submission Matrix":

    st.title("📊 Submission Matrix")

    all_data = []

    for form_name, config in FORMS.items():

        df = load_odk_data(config["form_id"])
        st.write(form_name)
        st.write(df["Enumerator_name"].head(20))
        
        if df.empty:
            continue

        # Enumerator column
        submit_col = "Enumerator_name"

        if submit_col not in df.columns:
            continue

        # Remove empty values
        df = df[df[submit_col].notna()]

        # Count submissions
        temp = (
            df.groupby(submit_col)
            .size()
            .reset_index(name="Count")
        )

        # Add form name
        temp["Form"] = form_name

        # Rename columns
        temp.columns = ["Person", "Count", "Form"]

        # Append
        all_data.append(temp)

    # FINAL OUTPUT
    if len(all_data) > 0:

        final_df = pd.concat(all_data)

        matrix = final_df.pivot_table(
            index="Person",
            columns="Form",
            values="Count",
            fill_value=0
        )

        st.dataframe(matrix, use_container_width=True)

    else:
        st.warning("No data found")

# ---------------- FORM REPORTS ----------------

elif page in FORMS:

    st.title(f"📥 {page} Report")

    config = FORMS[page]

    df = load_odk_data(config["form_id"])

    if df.empty:
        st.warning("No data found")

    else:

        # Select required columns
        columns = config.get("columns", [])

        available_cols = [
            col for col in columns if col in df.columns
        ]

        df_filtered = df[available_cols]

        st.dataframe(
            df_filtered,
            use_container_width=True
        )

        # Download button
        st.download_button(
            label="⬇ Download CSV",
            data=df_filtered.to_csv(index=False),
            file_name=f"{page}_report.csv",
            mime="text/csv"
        )
