import streamlit as st
import pandas as pd
from config import FORMS
from utils import load_data, load_repeat_data
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

        df = load_data(config["form_id"])
        if df.empty:
            continue
        submit_col = "enumerator-Jalamithra"
        if submit_col not in df.columns:
            continue
        df = df[df[submit_col].notna()]
        if df.empty:
            continue

        if df.empty:
            st.write(f"{form_name}: All names are blank")
            continue

        temp = (
            df.groupby(submit_col)
            .size()
            .reset_index(name="Count")
        )

        temp["Form"] = form_name

        temp.columns = ["Person", "Count", "Form"]

        all_data.append(temp)

    # FINAL MATRIX
    if all_data:

        final_df = pd.concat(all_data, ignore_index=True)

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

    st.title(f"📥 {page}")

    config = FORMS[page]
    if page == "2- Rejuvenation Works-Repairs":
        report_type = st.selectbox(
            "Select Rejuvenation Report",
            [
                "Main Report",
                "WSC Works",
                "WC Works",
                "LTCB Works"
            ]
        )
        st.write("Selected:", report_type)
        
    if page == "2- Rejuvenation Works-Repairs":
        if report_type == "Main Report":
            df = load_data("2.Rejuvenation_works")
        elif report_type == "WSC Works":
            df = load_repeat_data(
                "2.Rejuvenation_works",
                "wsc"
            )
        elif report_type == "WC Works":
            df = load_data("2.Rejuvenation_works-wc_")
        elif report_type == "LTCB Works":
            df = load_data("2.Rejuvenation_works-ltcb_")
    else:
        df = load_data(config["form_id"])

    if df.empty:
        st.warning("No data found")

    else:

        # Select required columns
        columns = config.get("columns", [])

        available_cols = [
            col for col in columns if col in df.columns
        ]

        df_filtered = df[available_cols]
        column_labels = config.get("column_labels", {})
        df_filtered = df_filtered.rename(columns=column_labels)

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
