import streamlit as st
import pandas as pd
from config import FORMS
from utils import load_data, load_repeat_data
import folium
from streamlit_folium import st_folium
import json
st.set_page_config(page_title="Project Dashboard", layout="wide")

# ---------------- SIDEBAR ----------------
main_menu = st.sidebar.radio(
    "Menu",
    ["📊 Reports", "🗺️ Maps"]
)

if main_menu == "🗺️ Maps":
    page = st.sidebar.radio(
        "Select Map",
        ["AHT Map"]
    )

elif main_menu == "📊 Reports":
    page = st.sidebar.radio(
        "Select Report",
        ["Form Submissions"] + list(FORMS.keys())
    )
# ---------------- Form Submissions ----------------

if page == "Form Submissions":

    st.title("📊 Form Submissions")

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
        
elif page == "AHT Map":

    st.title("🗺️ AHT Village Map")

    m = folium.Map(
        location=[18.3, 82.8],   # temporary center
        zoom_start=11,
        tiles=None
    )
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Satellite",
        overlay=False,
        control=True
    ).add_to(m)

    with open("Villages.geojson", "r", encoding="utf-8") as f:
        villages = json.load(f)

    folium.GeoJson(
        villages,
        name="Villages"
    ).add_to(m)

    st_folium(
        m,
        width=1200,
        height=700
    )
# ---------------- FORM REPORTS ----------------

elif page in FORMS:

    st.title(f"📥 {page}")

    config = FORMS[page]
    if page == "2.Rejuvenation_works":

        # -----------------------------------------
        # LOAD MAIN REJUVENATION DATA
        # -----------------------------------------

        main_df = load_data("2.Rejuvenation_works")

        if main_df.empty:
            st.warning("No rejuvenation data found")
            st.stop()

        # -----------------------------------------
        # VILLAGE FILTER
        # -----------------------------------------

        villages = (
            main_df["basic_details_repairs-village"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

        villages = sorted(villages)

        selected_village = st.selectbox(
            "Select Village",
            villages
        )

        # -----------------------------------------
        # FILTER MAIN TABLE BY VILLAGE
        # -----------------------------------------

        village_df = main_df[
            main_df["basic_details_repairs-village"]
            .astype(str)
            .str.strip()
            == selected_village
        ].copy()

        st.write("Selected Village:", selected_village)

        # -----------------------------------------
        # BASIC VILLAGE INFORMATION
        # -----------------------------------------

        if not village_df.empty:

            st.write(
                f"**Block:** {village_df['basic_details_repairs-block'].iloc[0]}   "
                f"**GP:** {village_df['basic_details_repairs-gp'].iloc[0]}"
            )

        # -----------------------------------------
        # REPAIR TYPES PRESENT IN THIS VILLAGE
        # -----------------------------------------

        repair_types = (
            village_df["checkdam_repairs"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

        st.write("Repair types found:", repair_types)
        
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
