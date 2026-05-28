import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
import pandas as pd
from datetime import date
from config import FORMS
from utils import load_odk_data
def push_to_google_sheet(df):

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=scope
    )

    client = gspread.authorize(creds)

    sheet = client.open("Reminder_SABAL").worksheet("Data")

    # 🔥 SAFE CONVERSION
    df = df.fillna("").astype(str)

    # Prepare data
    data = [df.columns.values.tolist()] + df.values.tolist()

    # Clear sheet
    sheet.clear()

    # Upload in chunks (prevents error)
    chunk_size = 5000

    for i in range(0, len(data), chunk_size):
        sheet.update(
            f"A{i+1}",
            data[i:i+chunk_size]
        )
    
st.set_page_config(page_title="MIS Tracking-SABAL", layout="wide")
st.title("📊 MIS Tracking - SABAL")

st.sidebar.title("Menu")

main_section = st.sidebar.radio(
    "Select Section",
    ["MIS-Status", "MIS-Reports"]
)

if main_section == "MIS-Reports":
    page = st.sidebar.radio(
        "Select Form",
        list(FORMS.keys())
    )
else:
    page = "MIS-Status"

if page == "MIS-Status":
    import pandas as pd
    import calendar

    st.title(" MIS Status")
    today = str(date.today())

    # Check last sync date
    if "last_sync" not in st.session_state:
        st.session_state["last_sync"] = ""

    if st.session_state["last_sync"] != today:

        with st.spinner("🔄 Auto syncing data..."):

            all_data = []

            for form_name, config in FORMS.items():
                df = load_odk_data(config["form_id"])

                if df.empty:
                    continue

                landscape_col = config.get("landscape_col")

                if landscape_col in df.columns:
                    landscape = df[landscape_col]
                else:
                    landscape = "Unknown"

                date_series = None
                for col in ["__system.submissionDate", "meta.submissionDate"]:
                    if col in df.columns:
                        date_series = pd.to_datetime(df[col], errors="coerce")
                        break

                if date_series is None:
                    continue

                temp_df = pd.DataFrame({
                    "Landscape": landscape,
                    "Date": date_series,
                    "Form": form_name
                })

                temp_df["Month"] = temp_df["Date"].dt.to_period("M").astype(str)

                temp_df = (
                    temp_df
                    .groupby(["Landscape", "Month", "Form"])
                    .size()
                    .reset_index(name="Count")
                )

                all_data.append(temp_df)

            if all_data:
                final_df = pd.concat(all_data, ignore_index=True)

                current_month = str(pd.Timestamp.now().to_period("M"))
                final_df = final_df[final_df["Month"] == current_month]

                final_df = final_df.sort_values(["Month", "Landscape", "Form"])

                push_to_google_sheet(final_df)

                st.session_state["last_sync"] = today

                st.success("✅ Auto sync completed!")

            else:
                st.warning("No data available to sync")

    # ---------------- FILTERS ----------------
    col1, col2 = st.columns(2)

    with col1:
        all_landscapes = set()

        for form_name, config in FORMS.items():
            df_temp = load_odk_data(config["form_id"])
            col = config.get("landscape_col")

            if col and col in df_temp.columns:
                all_landscapes.update(df_temp[col].dropna().unique())

        all_landscapes = sorted(all_landscapes)

        selected_landscape = st.selectbox(
            "Select Landscape",
            ["All"] + list(all_landscapes)
        )

    with col2:
        months = ["All"] + [calendar.month_name[i] for i in range(1, 13)]
        selected_month = st.selectbox("Select Month", months)

    # ---------------- DATA DISPLAY ----------------
    forms_list = list(FORMS.items())
    cols_per_row = 2

    for i in range(0, len(forms_list), cols_per_row):
        cols = st.columns(cols_per_row)

        for j in range(cols_per_row):
            if i + j >= len(forms_list):
                break

            form_name, config = forms_list[i + j]
            df = load_odk_data(config["form_id"])
            landscape_col = config.get("landscape_col")

            # -------- APPLY FILTERS --------

            # Landscape filter
            if selected_landscape != "All" and landscape_col in df.columns:
                df = df[df[landscape_col] == selected_landscape]

            # Month filter
            date_cols = ["__system.submissionDate", "meta.submissionDate"]
            date_col = None

            for col in date_cols:
                if col in df.columns:
                    date_col = col
                    break

            if selected_month != "All" and date_col:
                df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
                month_num = list(calendar.month_name).index(selected_month)
                df = df[df[date_col].dt.month == month_num]

            # -------- UI --------
            with cols[j]:
                st.markdown(f"#### 📦 {form_name}")

                if df.empty:
                    st.write("No data")
                    continue

                st.caption(f"Total: {len(df)}")

                if landscape_col and landscape_col in df.columns:
                    grouped = (
                        df.groupby(landscape_col)
                        .size()
                        .reset_index(name="Count")
                        .sort_values("Count", ascending=False)
                    )

                    grouped.columns = ["Landscape", "Count"]

                    st.dataframe(grouped, use_container_width=True, height=200)

                else:
                    st.warning(f"{landscape_col} not found")

elif page in FORMS:
    st.title(f"📥 {page} Report")

    config = FORMS[page]
    df = load_odk_data(config["form_id"])

    if df.empty:
        st.warning("No data found")

    else:
        # Select only required columns
        columns = config.get("columns", [])
        available_cols = [col for col in columns if col in df.columns]

        df_filtered = df[available_cols]

        st.dataframe(df_filtered, use_container_width=True)

        # Download button
        st.download_button(
            label="⬇ Download CSV",
            data=df_filtered.to_csv(index=False),
            file_name=f"{page}_report.csv",
            mime="text/csv"
        )
