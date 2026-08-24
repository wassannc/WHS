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

        # -----------------------------------------
        # GET INDIVIDUAL REPAIR TYPES
        # -----------------------------------------

        repair_types = []

        for value in village_df["checkdam_repairs"].dropna():

            value = str(value).strip()

            if value:
                parts = value.split()

                for repair in parts:
                    if repair not in repair_types:
                        repair_types.append(repair)

        # -----------------------------------------
        # GUIDE WALL REPAIR
        # -----------------------------------------

        if "Guide_wall_repair" in repair_types:

            st.subheader("🔧 Guidewall Repair")

            # Load Guidewall repeat table
            gwr_df = load_repeat_data(
                "2.Rejuvenation_works",
                "Submissions.gwr.gwr_"
            )

            if gwr_df.empty:
                st.info("No Guidewall repair records found.")
            else:

                # Link repeat records to main submissions
                gwr_df = gwr_df.merge(
                    main_df[
                        [
                            "KEY",
                            "basic_details_repairs-village",
                            "basic_details_repairs-gp",
                            "basic_details_repairs-block"
                        ]
                    ],
                    left_on="__Submissions-id",
                    right_on="KEY",
                    how="left"
                )

                # Filter to selected village
                gwr_village_df = gwr_df[
                    gwr_df["basic_details_repairs-village"]
                    .astype(str)
                    .str.strip()
                    == selected_village
                ].copy()

                if gwr_village_df.empty:
                    st.info(
                        f"No Guidewall repair data found for {selected_village}."
                    )
                else:

                    # Select required columns
                    gwr_village_df = gwr_village_df[
                        [
                            "basic_details_repairs-block",
                            "basic_details_repairs-gp",
                            "basic_details_repairs-village",
                            "avg_length_gwr",
                            "avg_breadth_gwr",
                            "avg_height_gwr",
                            "volume_guidewall_tobe_break",
                            "volume_guidewall_tobe_constrn"
                        ]
                    ]

                    # Rename columns
                    gwr_village_df = gwr_village_df.rename(
                        columns={
                            "basic_details_repairs-block": "Block",
                            "basic_details_repairs-gp": "GP",
                            "basic_details_repairs-village": "Village",
                            "avg_length_gwr": "Avg Length-mtrs",
                            "avg_breadth_gwr": "Avg Breadth-mtrs",
                            "avg_height_gwr": "Avg Height-mtrs",
                            "volume_guidewall_tobe_break":
                                "Volume guidewall to be break-cubmtrs",
                            "volume_guidewall_tobe_constrn":
                                "Volume guidewall to be constructed-cubmtrs"
                        }
                     )

                    st.dataframe(
                        gwr_village_df,
                        use_container_width=True
                    )
                # -----------------------------------------
                # NEW CANAL GUIDEWALL
                # -----------------------------------------

                if "New_canal_guidewall" in repair_types:
                
                    st.subheader("🏗️ New Canal Guidewall")
                
                    # Load repeat table
                    ncg_df = load_repeat_data(
                        "2.Rejuvenation_works",
                        "Submissions.ncg.ncg_"
                    )
                
                    if ncg_df.empty:
                        st.info("No New Canal Guidewall records found.")
                
                    else:
                
                        # Link repeat records to main submissions
                        ncg_df = ncg_df.merge(
                            main_df[
                                [
                                    "KEY",
                                    "basic_details_repairs-village",
                                    "basic_details_repairs-gp",
                                    "basic_details_repairs-block"
                                ]
                            ],
                            left_on="__Submissions-id",
                            right_on="KEY",
                            how="left"
                        )
                
                        # Filter selected village
                        ncg_village_df = ncg_df[
                            ncg_df["basic_details_repairs-village"]
                            .astype(str)
                            .str.strip()
                            == selected_village
                        ].copy()
                
                        if ncg_village_df.empty:
                
                            st.info(
                                f"No New Canal Guidewall data found for {selected_village}."
                            )
                
                        else:
                
                            # Select required columns
                            ncg_village_df = ncg_village_df[
                                [
                                    "basic_details_repairs-block",
                                    "basic_details_repairs-gp",
                                    "basic_details_repairs-village",
                                    "guidewalls_side",
                                    "guidewalls_nos_ncg",
                                    "length_ncg",
                                    "basement_soilwork_osncg",
                                    "volume_cc148_basement_concrete_osncg",
                                    "volume_cc136_to_make_canal_guidewalls_osncg"
                                ]
                            ]
                
                            # Rename columns
                            ncg_village_df = ncg_village_df.rename(
                                columns={
                                    "basic_details_repairs-block": "Block",
                                    "basic_details_repairs-gp": "GP",
                                    "basic_details_repairs-village": "Village",
                                    "guidewalls_side": "Side",
                                    "guidewalls_nos_ncg": "No.",
                                    "length_ncg": "Length-mtrs",
                                    "basement_soilwork_osncg": "Basement soil work",
                                    "volume_cc148_basement_concrete_osncg":
                                        "Basement concrete volume-cubmtrs",
                                    "volume_cc136_to_make_canal_guidewalls_osncg":
                                        "Canal guidewall volume-cubmtrs"
                                }
                            )
                
                            st.dataframe(
                                ncg_village_df,
                                use_container_width=True
                            )
                # -----------------------------------------
                # CANAL GUIDEWALL HEIGHT INCREASE
                # -----------------------------------------
                
                if "Canal_guidewall_height_increase" in repair_types:
                
                    st.subheader("📏 Canal Guidewall Height Increase")
                
                    # Load repeat table
                    cghi_df = load_repeat_data(
                        "2.Rejuvenation_works",
                        "Submissions.Canal_guidewall_height_increase.Canal_guidewall_height_increase_"
                    )
                
                    if cghi_df.empty:
                        st.info("No Canal Guidewall Height Increase records found.")
                
                    else:
                
                        # Link repeat records to main submissions
                        cghi_df = cghi_df.merge(
                            main_df[
                                [
                                    "KEY",
                                    "basic_details_repairs-village",
                                    "basic_details_repairs-gp",
                                    "basic_details_repairs-block"
                                ]
                            ],
                            left_on="__Submissions-id",
                            right_on="KEY",
                            how="left"
                        )
                
                        # Filter selected village
                        cghi_village_df = cghi_df[
                            cghi_df["basic_details_repairs-village"]
                            .astype(str)
                            .str.strip()
                            == selected_village
                        ].copy()
                
                        if cghi_village_df.empty:
                
                            st.info(
                                f"No Canal Guidewall Height Increase data found for {selected_village}."
                            )
                
                        else:
                
                            # Select required columns
                            cghi_village_df = cghi_village_df[
                                [
                                    "basic_details_repairs-block",
                                    "basic_details_repairs-gp",
                                    "basic_details_repairs-village",
                                    "canal_guidewall_height_increase_side",
                                    "guidewalls_nos_canal_guidewall_height_increase",
                                    "length_canal_guidewall_height_increase",
                                    "width_canal_guidewall_height_increase",
                                    "height_canal_guidewall_height_increase",
                                    "workdetails_canal_guidewall_height_increase"
                                ]
                            ]
                
                            # Rename columns
                            cghi_village_df = cghi_village_df.rename(
                                columns={
                                    "basic_details_repairs-block": "Block",
                                    "basic_details_repairs-gp": "GP",
                                    "basic_details_repairs-village": "Village",
                                    "canal_guidewall_height_increase_side": "Side",
                                    "guidewalls_nos_canal_guidewall_height_increase": "No.",
                                    "length_canal_guidewall_height_increase": "Length-mtrs",
                                    "width_canal_guidewall_height_increase": "Width-mtrs",
                                    "height_canal_guidewall_height_increase": "Height-mtrs",
                                    "workdetails_canal_guidewall_height_increase": "Work details"
                                }
                            )
                
                            st.dataframe(
                                cghi_village_df,
                                use_container_width=True
                            )
                # -----------------------------------------
                # WEARING COAT
                # -----------------------------------------
                
                if "Wearing_coat" in repair_types:
                
                    st.subheader("🛣️ Wearing Coat")
                
                    wc_df = load_repeat_data(
                        "2.Rejuvenation_works",
                        "Submissions.wc.wc_"
                    )
                
                    if wc_df.empty:
                        st.info("No Wearing Coat records found.")
                
                    else:
                
                        # Link repeat records to main submissions
                        wc_df = wc_df.merge(
                            main_df[
                                [
                                    "KEY",
                                    "basic_details_repairs-village",
                                    "basic_details_repairs-gp",
                                    "basic_details_repairs-block"
                                ]
                            ],
                            left_on="__Submissions-id",
                            right_on="KEY",
                            how="left"
                        )
                
                        # Filter selected village
                        wc_village_df = wc_df[
                            wc_df["basic_details_repairs-village"]
                            .astype(str)
                            .str.strip()
                            == selected_village
                        ].copy()
                
                        if wc_village_df.empty:
                
                            st.info(
                                f"No Wearing Coat data found for {selected_village}."
                            )
                
                        else:
                
                            # Select required columns
                            wc_village_df = wc_village_df[
                                [
                                    "basic_details_repairs-block",
                                    "basic_details_repairs-gp",
                                    "basic_details_repairs-village",
                                    "avg_length_wc_leak1",
                                    "avg_breadth_wc_leak1",
                                    "avg_depth_wc_leak1",
                                    "volume_leak1_wc"
                                ]
                            ]
                
                            # Rename columns
                            wc_village_df = wc_village_df.rename(
                                columns={
                                    "basic_details_repairs-block": "Block",
                                    "basic_details_repairs-gp": "GP",
                                    "basic_details_repairs-village": "Village",
                                    "avg_length_wc_leak1": "Avg Length-mtrs",
                                    "avg_breadth_wc_leak1": "Avg Breadth-mtrs",
                                    "avg_depth_wc_leak1": "Avg Depth-mtrs",
                                    "volume_leak1_wc": "Total Volume-cubmtrs"
                                }
                            )
                
                            st.dataframe(
                                wc_village_df,
                                use_container_width=True
                            )    
                # -----------------------------------------
                # GUIDEWALL BEDJOINT LEAKAGE
                # -----------------------------------------
                
                if "guidewall_and_bed_joint_leakage" in repair_types:
                
                    st.subheader("🧱 Guidewall Bedjoint Leakage")
                
                    gbjl_df = load_repeat_data(
                        "2.Rejuvenation_works",
                        "Submissions.gwbjl.gwbjl_"
                    )
                
                    if gbjl_df.empty:
                        st.info("No Guidewall Bedjoint Leakage records found.")
                
                    else:
                
                        # Link repeat records to main submissions
                        gbjl_df = gbjl_df.merge(
                            main_df[
                                [
                                    "KEY",
                                    "basic_details_repairs-village",
                                    "basic_details_repairs-gp",
                                    "basic_details_repairs-block"
                                ]
                            ],
                            left_on="__Submissions-id",
                            right_on="KEY",
                            how="left"
                        )
                
                        # Filter selected village
                        gbjl_village_df = gbjl_df[
                            gbjl_df["basic_details_repairs-village"]
                            .astype(str)
                            .str.strip()
                            == selected_village
                        ].copy()
                
                        if gbjl_village_df.empty:
                
                            st.info(
                                f"No Guidewall Bedjoint Leakage data found for {selected_village}."
                            )
                
                        else:
                
                            gbjl_village_df = gbjl_village_df[
                                [
                                    "basic_details_repairs-block",
                                    "basic_details_repairs-gp",
                                    "basic_details_repairs-village",
                                    "leakage_canal_length_gwbjl_leak1",
                                    "leakage_canal_breadth_gwbjl_leak1",
                                    "leakage_canal_height_gwbjl_leak1",
                                    "volume_cc_gwbjl_leak1",
                                    "total_volume_gwbjl"
                                ]
                            ]
                
                            gbjl_village_df = gbjl_village_df.rename(
                                columns={
                                    "basic_details_repairs-block": "Block",
                                    "basic_details_repairs-gp": "GP",
                                    "basic_details_repairs-village": "Village",
                                    "leakage_canal_length_gwbjl_leak1":
                                        "Length-mtrs",
                                    "leakage_canal_breadth_gwbjl_leak1":
                                        "Breadth-mtrs",
                                    "leakage_canal_height_gwbjl_leak1":
                                        "Height-mtrs",
                                    "volume_cc_gwbjl_leak1":
                                        "Volume-cubmtrs",
                                    "total_volume_gwbjl":
                                        "Total Volume-cubmtrs"
                                }
                            )
                
                            st.dataframe(
                                gbjl_village_df,
                                use_container_width=True
                            ) 
                # -----------------------------------------
                # LEAKAGE THROUGH CANAL BED
                # -----------------------------------------
                
                if "leakage_through_canal_bed" in repair_types:
                
                    st.subheader("💧 Leakage Through Canal Bed")
                
                    lcb_df = load_repeat_data(
                        "2.Rejuvenation_works",
                        "Submissions.stop_leak_bodywall_repeat.stop_leak_bodywall_repeat_"
                    )
                
                    if lcb_df.empty:
                
                        st.info("No Leakage Through Canal Bed records found.")
                
                    else:
                
                        # Link repeat records to main submissions
                        lcb_df = lcb_df.merge(
                            main_df[
                                [
                                    "KEY",
                                    "basic_details_repairs-village",
                                    "basic_details_repairs-gp",
                                    "basic_details_repairs-block"
                                ]
                            ],
                            left_on="__Submissions-id",
                            right_on="KEY",
                            how="left"
                        )
                
                        # Filter selected village
                        lcb_village_df = lcb_df[
                            lcb_df["basic_details_repairs-village"]
                            .astype(str)
                            .str.strip()
                            == selected_village
                        ].copy()
                
                        if lcb_village_df.empty:
                
                            st.info(
                                f"No Leakage Through Canal Bed data found for {selected_village}."
                            )
                
                        else:
                
                            lcb_village_df = lcb_village_df[
                                [
                                    "basic_details_repairs-block",
                                    "basic_details_repairs-gp",
                                    "basic_details_repairs-village",
                                    "avg_length_la_leak1_sl",
                                    "avg_breadth_la_leak1_sl",
                                    "avg_height_sl_la_leak1",
                                    "cc124_volume_la_sl_leak1"
                                ]
                            ]
                
                            lcb_village_df = lcb_village_df.rename(
                                columns={
                                    "basic_details_repairs-block": "Block",
                                    "basic_details_repairs-gp": "GP",
                                    "basic_details_repairs-village": "Village",
                                    "avg_length_la_leak1_sl": "Avg Length-mtrs",
                                    "avg_breadth_la_leak1_sl": "Avg Breadth-mtrs",
                                    "avg_height_sl_la_leak1": "Avg Height-mtrs",
                                    "cc124_volume_la_sl_leak1":
                                        "Volume-cubmtrs"
                                }
                            )
                
                            st.dataframe(
                                lcb_village_df,
                                use_container_width=True
                            )    
                # -----------------------------------------
                # LEAKAGES ARREST
                # -----------------------------------------
                
                if "Leackages_arrest" in repair_types:
                
                    st.subheader("🚧 Leakages Arrest")
                
                    la_df = load_repeat_data(
                        "2.Rejuvenation_works",
                        "Submissions.stop_leak_bodywall_repeat.stop_leak_bodywall_repeat_"
                    )
                
                    if la_df.empty:
                
                        st.info("No Leakages Arrest records found.")
                
                    else:
                
                        # Link repeat records to main submissions
                        la_df = la_df.merge(
                            main_df[
                                [
                                    "KEY",
                                    "basic_details_repairs-village",
                                    "basic_details_repairs-gp",
                                    "basic_details_repairs-block"
                                ]
                            ],
                            left_on="__Submissions-id",
                            right_on="KEY",
                            how="left"
                        )
                
                        # Filter selected village
                        la_village_df = la_df[
                            la_df["basic_details_repairs-village"]
                            .astype(str)
                            .str.strip()
                            == selected_village
                        ].copy()
                
                        if la_village_df.empty:
                
                            st.info(
                                f"No Leakages Arrest data found for {selected_village}."
                            )
                
                        else:
                
                            la_village_df = la_village_df[
                                [
                                    "basic_details_repairs-block",
                                    "basic_details_repairs-gp",
                                    "basic_details_repairs-village",
                                    "avg_length_la_leak1_sl",
                                    "avg_breadth_la_leak1_sl",
                                    "avg_height_sl_la_leak1",
                                    "cc124_volume_la_sl_leak1"
                                ]
                            ]
                
                            la_village_df = la_village_df.rename(
                                columns={
                                    "basic_details_repairs-block": "Block",
                                    "basic_details_repairs-gp": "GP",
                                    "basic_details_repairs-village": "Village",
                                    "avg_length_la_leak1_sl": "Avg Length-mtrs",
                                    "avg_breadth_la_leak1_sl": "Avg Breadth-mtrs",
                                    "avg_height_sl_la_leak1": "Avg Height-mtrs",
                                    "cc124_volume_la_sl_leak1":
                                        "Volume-cubmtrs"
                                }
                            )
                
                            st.dataframe(
                                la_village_df,
                                use_container_width=True
                            )
                # -----------------------------------------
                # SCOURVENT OPENING
                # -----------------------------------------
                
                if "Scourvent_opening" in repair_types:
                
                    st.subheader("🔘 Scourvent Opening")
                
                    so_df = load_repeat_data(
                        "2.Rejuvenation_works",
                        "Submissions.so"
                    )
                
                    if so_df.empty:
                
                        st.info("No Scourvent Opening records found.")
                
                    else:
                
                        # Link repeat records to main submissions
                        so_df = so_df.merge(
                            main_df[
                                [
                                    "KEY",
                                    "basic_details_repairs-village",
                                    "basic_details_repairs-gp",
                                    "basic_details_repairs-block"
                                ]
                            ],
                            left_on="__Submissions-id",
                            right_on="KEY",
                            how="left"
                        )
                
                        # Filter selected village
                        so_village_df = so_df[
                            so_df["basic_details_repairs-village"]
                            .astype(str)
                            .str.strip()
                            == selected_village
                        ].copy()
                
                        if so_village_df.empty:
                
                            st.info(
                                f"No Scourvent Opening data found for {selected_village}."
                            )
                
                        else:
                
                            # Select required columns
                            so_village_df = so_village_df[
                                [
                                    "basic_details_repairs-block",
                                    "basic_details_repairs-gp",
                                    "basic_details_repairs-village",
                                    "avg_length_so",
                                    "avg_breadth_so",
                                    "avg_height_so",
                                    "volume_so"
                                ]
                            ]
                
                            # Rename columns
                            so_village_df = so_village_df.rename(
                                columns={
                                    "basic_details_repairs-block": "Block",
                                    "basic_details_repairs-gp": "GP",
                                    "basic_details_repairs-village": "Village",
                                    "avg_length_so": "Avg Length-mtrs",
                                    "avg_breadth_so": "Avg Breadth-mtrs",
                                    "avg_height_so": "Avg Height-mtrs",
                                    "volume_so": "Volume-cubmtrs"
                                }
                            )
                
                            st.dataframe(
                                so_village_df,
                                use_container_width=True
                            )
                # -----------------------------------------
                # WATER SUPPLY CONTROL
                # -----------------------------------------
                
                if "Water_supply_control" in repair_types:
                
                    st.subheader("🚰 Water Supply Control")
                
                    wsc_df = load_repeat_data(
                        "2.Rejuvenation_works",
                        "Submissions.wsc.wsc_"
                    )
                
                    if wsc_df.empty:
                
                        st.info("No Water Supply Control records found.")
                
                    else:
                
                        # Link repeat records to main submission
                        wsc_df = wsc_df.merge(
                            main_df[
                                [
                                    "KEY",
                                    "basic_details_repairs-village",
                                    "basic_details_repairs-gp",
                                    "basic_details_repairs-block"
                                ]
                            ],
                            left_on="__Submissions-id",
                            right_on="KEY",
                            how="left"
                        )
                
                        # Filter selected village
                        wsc_village_df = wsc_df[
                            wsc_df["basic_details_repairs-village"]
                            .astype(str)
                            .str.strip()
                            == selected_village
                        ].copy()
                
                        if wsc_village_df.empty:
                
                            st.info(
                                f"No Water Supply Control data found for {selected_village}."
                            )
                
                        else:
                
                            # Select only useful engineering fields
                            wsc_village_df = wsc_village_df[
                                [
                                    "basic_details_repairs-block",
                                    "basic_details_repairs-gp",
                                    "basic_details_repairs-village",
                                    "vent1_wsc",
                                    "hole_size_diameter_vent1",
                                    "valve_size_vent1"
                                ]
                            ]
                
                            # Rename columns
                            wsc_village_df = wsc_village_df.rename(
                                columns={
                                    "basic_details_repairs-block": "Block",
                                    "basic_details_repairs-gp": "GP",
                                    "basic_details_repairs-village": "Village",
                                    "vent1_wsc": "Vent",
                                    "hole_size_diameter_vent1": "Hole size-dia",
                                    "valve_size_vent1": "Valve size"
                                }
                            )
                
                            st.dataframe(
                                wsc_village_df,
                                use_container_width=True
                            )
                # -----------------------------------------
                # DAM MEASUREMENT - MAIN TABLE
                # -----------------------------------------
                
                if "Dam_measurement" in repair_types:
                
                    st.subheader("📏 Dam Measurement")
                
                    # =========================================
                    # 1. CHECKDAM MEASUREMENTS
                    # =========================================
                
                    st.markdown("### 📐 Checkdam Measurements")
                
                    checkdam_cols = [
                        "Dam_measurements-Checkdam_lenght",
                        "Dam_measurements-Checkdam_top_width",
                        "Dam_measurements-Checkdam_height",
                        "Dam_measurements-Steps_available",
                        "Dam_measurements-Steps_need",
                        "Dam_measurements-Steps_required",
                        "Dam_measurements-steps_volume"
                    ]
                
                    checkdam_cols = [
                        col for col in checkdam_cols
                        if col in village_df.columns
                    ]
                
                    if checkdam_cols:
                
                        checkdam_df = village_df[checkdam_cols].copy()
                
                        checkdam_df = checkdam_df.rename(
                            columns={
                                "Dam_measurements-Checkdam_lenght":
                                    "Checkdam Length-m",
                                "Dam_measurements-Checkdam_top_width":
                                    "Checkdam Top Width-m",
                                "Dam_measurements-Checkdam_height":
                                    "Checkdam Height-m",
                                "Dam_measurements-Steps_available":
                                    "Steps Available",
                                "Dam_measurements-Steps_need":
                                    "Steps Need",
                                "Dam_measurements-Steps_required":
                                    "Steps Required",
                                "Dam_measurements-steps_volume":
                                    "Steps Volume-cum"
                            }
                        )
                
                        st.dataframe(
                            checkdam_df,
                            use_container_width=True,
                            hide_index=True
                        )
                
                    # =========================================
                    # 2. GUIDE WALLS
                    # =========================================
                
                    st.markdown("### 🧱 Guidewalls")
                
                    guidewall_rows = []
                
                    for step in [1, 2, 3]:
                
                        nos_col = f"Dam_measurements-guidewall_step{step}_nos"
                        length_col = f"Dam_measurements-guidewall_step{step}_length"
                        width_col = f"Dam_measurements-guidewall_step{step}_width"
                        height_col = f"Dam_measurements-guidewall_step{step}_height"
                        volume_col = f"Dam_measurements-guidewall_step{step}_volume"
                
                        if any(
                            col in village_df.columns
                            for col in [
                                nos_col,
                                length_col,
                                width_col,
                                height_col,
                                volume_col
                            ]
                        ):
                
                            guidewall_rows.append({
                                "Step": f"Step {step}",
                                "No.": village_df[nos_col].iloc[0]
                                    if nos_col in village_df.columns else "",
                                "Length-m": village_df[length_col].iloc[0]
                                    if length_col in village_df.columns else "",
                                "Width-m": village_df[width_col].iloc[0]
                                    if width_col in village_df.columns else "",
                                "Height-m": village_df[height_col].iloc[0]
                                    if height_col in village_df.columns else "",
                                "Volume-cum": village_df[volume_col].iloc[0]
                                    if volume_col in village_df.columns else ""
                            })
                
                    if guidewall_rows:
                
                        guidewall_df = pd.DataFrame(guidewall_rows)
                
                        st.dataframe(
                            guidewall_df,
                            use_container_width=True,
                            hide_index=True
                        )
                
                    # =========================================
                    # 3. ABUTMENTS
                    # =========================================
                
                    st.markdown("### 🏗️ Abutments")
                
                    abutment_rows = []
                
                    if any(
                        col in village_df.columns
                        for col in [
                            "Dam_guidewall-abutments_condition",
                            "Dam_guidewall-abutment_right",
                            "Dam_guidewall-soilwork_abutment_right",
                            "Dam_guidewall-cc148_abutment_right"
                        ]
                    ):
                
                        abutment_rows.append({
                            "Side": "Right",
                            "Condition":
                                village_df[
                                    "Dam_guidewall-abutments_condition"
                                ].iloc[0]
                                if "Dam_guidewall-abutments_condition"
                                in village_df.columns else "",
                
                            "Abutment":
                                village_df[
                                    "Dam_guidewall-abutment_right"
                                ].iloc[0]
                                if "Dam_guidewall-abutment_right"
                                in village_df.columns else "",
                
                            "Soil Work":
                                village_df[
                                    "Dam_guidewall-soilwork_abutment_right"
                                ].iloc[0]
                                if "Dam_guidewall-soilwork_abutment_right"
                                in village_df.columns else "",
                
                            "CC 1:4:8":
                                village_df[
                                    "Dam_guidewall-cc148_abutment_right"
                                ].iloc[0]
                                if "Dam_guidewall-cc148_abutment_right"
                                in village_df.columns else ""
                        })
                
                    if any(
                        col in village_df.columns
                        for col in [
                            "Dam_guidewall-abutments_condition",
                            "Dam_guidewall-abutment_left",
                            "Dam_guidewall-soilwork_abutment_left",
                            "Dam_guidewall-cc148_abutment_left"
                        ]
                    ):
                
                        abutment_rows.append({
                            "Side": "Left",
                            "Condition":
                                village_df[
                                    "Dam_guidewall-abutments_condition"
                                ].iloc[0]
                                if "Dam_guidewall-abutments_condition"
                                in village_df.columns else "",
                
                            "Abutment":
                                village_df[
                                    "Dam_guidewall-abutment_left"
                                ].iloc[0]
                                if "Dam_guidewall-abutment_left"
                                in village_df.columns else "",
                
                            "Soil Work":
                                village_df[
                                    "Dam_guidewall-soilwork_abutment_left"
                                ].iloc[0]
                                if "Dam_guidewall-soilwork_abutment_left"
                                in village_df.columns else "",
                
                            "CC 1:4:8":
                                village_df[
                                    "Dam_guidewall-cc148_abutment_left"
                                ].iloc[0]
                                if "Dam_guidewall-cc148_abutment_left"
                                in village_df.columns else ""
                        })
                
                    if abutment_rows:
                
                        abutment_df = pd.DataFrame(abutment_rows)
                
                        st.dataframe(
                            abutment_df,
                            use_container_width=True,
                            hide_index=True
                        )
                
                    # =========================================
                    # 4. APRON
                    # =========================================
                
                    st.markdown("### 🔨 Apron")
                
                    apron_cols = [
                        "Dam_guidewall-apron_condition",
                        "Dam_guidewall-len_apron1",
                        "Dam_guidewall-len_apron2",
                        "Dam_guidewall-volume_apron1",
                        "Dam_guidewall-volume_apron2"
                    ]
                
                    apron_cols = [
                        col for col in apron_cols
                        if col in village_df.columns
                    ]
                
                    if apron_cols:
                
                        apron_df = village_df[apron_cols].copy()
                
                        apron_df = apron_df.rename(
                            columns={
                                "Dam_guidewall-apron_condition":
                                    "Condition",
                                "Dam_guidewall-len_apron1":
                                    "Apron Length 1-m",
                                "Dam_guidewall-len_apron2":
                                    "Apron Length 2-m",
                                "Dam_guidewall-volume_apron1":
                                    "Apron Volume 1-cum",
                                "Dam_guidewall-volume_apron2":
                                    "Apron Volume 2-cum"
                            }
                        )
                
                        st.dataframe(
                            apron_df,
                            use_container_width=True,
                            hide_index=True
                        )
                    # =========================================
                    # 5. Other Earthwork at Dam
                    # =========================================
                
                    st.markdown("### 🔨 Other Earthwork at Dam")
                
                    ew_cols = [
                        "earthwork_dam-water_passing_below_aprons_bw",
                        "earthwork_dam-us_cutoff_len",
                        "earthwork_dam-earthwork_us",
                        "earthwork_dam-ds_cutoff_len",
                        "earthwork_dam-earthwork_ds",
                        "earthwork_dam-earthwork_bw"
                    ]
                
                    ew_cols = [
                        col for col in ew_cols
                        if col in village_df.columns
                    ]
                
                    if ew_cols:
                
                        ew_df = village_df[ew_cols].copy()
                
                        ew_df = ew_df.rename(
                            columns={
                                "earthwork_dam-water_passing_below_aprons_bw":
                                    "Water passing below aprons?",
                                "earthwork_dam-us_cutoff_len":
                                    "Upstream cutoff length-m",
                                "earthwork_dam-earthwork_us":
                                    "Upstream earthwork-cum",
                                "earthwork_dam-ds_cutoff_len":
                                    "Downstream cutoff length-m",
                                "earthwork_dam-earthwork_ds":
                                    "Downstream earthwork-cum",
                                "earthwork_dam-earthwork_bw":
                                    "Earthwork at bottom width"
                            }
                        )
                
                        st.dataframe(
                            ew_df,
                            use_container_width=True,
                            hide_index=True
                        )
                # -----------------------------------------
                # Scourvent Open - MAIN TABLE
                # -----------------------------------------
                
                if "Scourvent_opening" in repair_types:
                
                    st.subheader("⛰️ Scourvent Open")
                
                    so_cols = [
                        "so-lower_breadth_so",
                        "so-upper_breadth_so",
                        "so-avg_breadth_so",
                        "so-lower_length_so",
                        "so-upper_length_so",
                        "so-avg_length_so",
                        "so-avg_height_so",
                        "so-volume_so",
                        "so-gps_so-Latitude",
                        "so-gps_so-Longitude",
                        "so-image_so"   
                    ]
                
                    # Keep only columns available in the main table
                    available_so_cols = [
                        col for col in so_cols
                        if col in village_df.columns
                    ]
                
                    if available_so_cols:
                
                        so_df = village_df[
                            available_so_cols
                        ].copy()
                
                        so_df = so_df.rename(
                            columns={
                                "so-lower_breadth_so":
                                    "Lower Breadth-m",
                                "so-upper_breadth_so":
                                    "Upper Breadth-m",
                                "so-avg_breadth_so":
                                    "Average Breadth-m",
                
                                "so-lower_length_so":
                                    "Lower Length-m",
                                "so-upper_length_so":
                                    "Upper Length-m",
                                "so-avg_length_so":
                                    "Average Length-m",
                
                                "so-avg_height_so":
                                    "Average Height-m",
                
                                "so-volume_so":
                                    "Volume-cum",
                                
                                "so-gps_so-Latitude":
                                    "GPS Latitude",
                                "so-gps_so-Longitude":
                                    "GPS Longitude",
                                "so-image_so":
                                    "Photo"
                            }
                        )
                
                        st.dataframe(
                            so_df,
                            use_container_width=True,
                            hide_index=True
                        )
                
                    else:
                
                        st.info(
                            "No Scourvent Open data found for this village."
                        )
                # -----------------------------------------
                # TALUS REPACKING - MAIN TABLE
                # -----------------------------------------
                
                if "Talus_repacking" in repair_types:
                
                    st.subheader("⛰️ Talus Repacking")
                
                    # =========================================
                    # 1. EXISTING TALUS
                    # =========================================
                
                    st.markdown("### Existing Talus")
                
                    talus_cols = [
                        "tr-avg_breadth_tr",
                        "tr-avg_length_tr",
                        "tr-avg_depth_tr",
                        "tr-gps_tr-Latitude",
                        "tr-gps_tr-Longitude",
                        "tr-image_tr",
                        "tr-volume_tr"
                    ]
                
                    available_talus_cols = [
                        col for col in talus_cols
                        if col in village_df.columns
                    ]
                
                    if available_talus_cols:
                
                        talus_df = village_df[
                            available_talus_cols
                        ].copy()
                
                        talus_df = talus_df.rename(columns={
                            "tr-avg_breadth_tr": "Avg Breadth-m",
                            "tr-avg_length_tr": "Avg Length-m",
                            "tr-avg_depth_tr": "Avg Depth-m",
                            "tr-gps_tr-Latitude": "GPS Latitude",
                            "tr-gps_tr-Longitude": "GPS Longitude",
                            "tr-image_tr": "Photo",
                            "tr-volume_tr": "Volume-cum"
                        })
                
                        st.dataframe(
                            talus_df,
                            use_container_width=True,
                            hide_index=True
                        )
                
                    # =========================================
                    
                    # 2. TALUS TO REPACK
                    # =========================================
                
                    st.markdown("### Talus to Repack")
                
                    repack_cols = [
                        "tr-to_repack_tp",
                        "tr-avg_breadth_tp",
                        "tr-avg_length_tp",
                        "tr-avg_height_tp",
                        "tr-gps_tp-Latitude",
                        "tr-gps_tp-Longitude",
                        "tr-image_tp",
                        "tr-volume_tp"
                    ]
                
                    available_repack_cols = [
                        col for col in repack_cols
                        if col in village_df.columns
                    ]
                
                    if available_repack_cols:
                
                        repack_df = village_df[
                            available_repack_cols
                        ].copy()
                
                        repack_df = repack_df.rename(columns={
                            "tr-to_repack_tp": "To Repack",
                            "tr-avg_breadth_tp": "Avg Breadth-m",
                            "tr-avg_length_tp": "Avg Length-m",
                            "tr-avg_height_tp": "Avg Height-m",
                            "tr-gps_tp-Latitude": "GPS Latitude",
                            "tr-gps_tp-Longitude": "GPS Longitude",
                            "tr-image_tp": "Photo",
                            "tr-volume_tp": "Volume-cum"
                        })
                
                        st.dataframe(
                            repack_df,
                            use_container_width=True,
                            hide_index=True
                        )
                # -----------------------------------------
                # CANAL EXCESS WATER DRAWING - MAIN TABLE
                # -----------------------------------------
                
                if "canal_excess_water_drawing" in repair_types:
                
                    st.subheader("💧 Canal Excess Water Drawing")
                
                    # =========================================
                    # 1. BASEMENT SOIL WORK
                    # =========================================
                
                    st.markdown("### Basement Soil Work")
                
                    soil_cols = [
                        "cewd-chainage_soil_work_for_basement_from",
                        "cewd-chainage_soil_work_for_basement_to",
                        "cewd-basement_length_soil_work",
                        "cewd-basement_breadth_soil_work",
                        "cewd-basement_depth_soil_work",
                        "cewd-total_soilwork_basement_cum"
                    ]
                
                    available_soil_cols = [
                        col for col in soil_cols
                        if col in village_df.columns
                    ]
                
                    if available_soil_cols:
                
                        soil_df = village_df[available_soil_cols].copy()
                
                        soil_df = soil_df.rename(columns={
                            "cewd-chainage_soil_work_for_basement_from":
                                "Chainage From",
                            "cewd-chainage_soil_work_for_basement_to":
                                "Chainage To",
                            "cewd-basement_length_soil_work":
                                "Length-m",
                            "cewd-basement_breadth_soil_work":
                                "Breadth-m",
                            "cewd-basement_depth_soil_work":
                                "Depth-m",
                            "cewd-total_soilwork_basement_cum":
                                "Total Soil Work-cum"
                        })
                
                        st.dataframe(
                            soil_df,
                            use_container_width=True,
                            hide_index=True
                        )
                
                    # =========================================
                    # 2. BASEMENT CONCRETE WORK
                    # =========================================
                
                    st.markdown("### Basement Concrete Work")
                
                    concrete_cols = [
                        "cewd-cc_concrete_work_basement",
                        "cewd-basement_length_concrete_work",
                        "cewd-basement_breadth_concrete_work",
                        "cewd-basement_depth_concrete_work",
                        "cewd-total_concrete_work_basement"
                    ]
                
                    available_concrete_cols = [
                        col for col in concrete_cols
                        if col in village_df.columns
                    ]
                
                    if available_concrete_cols:
                
                        concrete_df = village_df[
                            available_concrete_cols
                        ].copy()
                
                        concrete_df = concrete_df.rename(columns={
                            "cewd-cc_concrete_work_basement":
                                "Concrete Work",
                            "cewd-basement_length_concrete_work":
                                "Length-m",
                            "cewd-basement_breadth_concrete_work":
                                "Breadth-m",
                            "cewd-basement_depth_concrete_work":
                                "Depth-m",
                            "cewd-total_concrete_work_basement":
                                "Total Concrete Work-cum"
                        })
                
                        st.dataframe(
                            concrete_df,
                            use_container_width=True,
                            hide_index=True
                        )
                
                    # =========================================
                    # 3. WALL TO BE CONSTRUCTED
                    # =========================================
                
                    st.markdown("### Wall to be Constructed")
                
                    wall_cols = [
                        "cewd-length_wall_tobe_constrn",
                        "cewd-breadth_wall_tobe_constrn",
                        "cewd-height_wall_tobe_constrn",
                        "cewd-volume_walls_cum"
                    ]
                
                    available_wall_cols = [
                        col for col in wall_cols
                        if col in village_df.columns
                    ]
                
                    if available_wall_cols:
                
                        wall_df = village_df[
                            available_wall_cols
                        ].copy()
                
                        wall_df = wall_df.rename(columns={
                            "cewd-length_wall_tobe_constrn":
                                "Length-m",
                            "cewd-breadth_wall_tobe_constrn":
                                "Breadth-m",
                            "cewd-height_wall_tobe_constrn":
                                "Height-m",
                            "cewd-volume_walls_cum":
                                "Volume-cum"
                        })
                
                        st.dataframe(
                            wall_df,
                            use_container_width=True,
                            hide_index=True
                        )
                
                    # =========================================
                    # 4. LOCATION & PHOTO
                    # =========================================
                
                    location_cols = [
                        "cewd-gps_cewd-Latitude",
                        "cewd-gps_cewd-Longitude",
                        "cewd-image_cewd"
                    ]
                
                    available_location_cols = [
                        col for col in location_cols
                        if col in village_df.columns
                    ]
                
                    if available_location_cols:
                
                        st.markdown("### 📍 Location / Photo")
                
                        location_df = village_df[
                            available_location_cols
                        ].copy()
                
                        location_df = location_df.rename(columns={
                            "cewd-gps_cewd-Latitude":
                                "GPS Latitude",
                            "cewd-gps_cewd-Longitude":
                                "GPS Longitude",
                            "cewd-image_cewd":
                                "Photo"
                        })
                
                        st.dataframe(
                            location_df,
                            use_container_width=True,
                            hide_index=True
                        )
                # -----------------------------------------
                # CANAL BED AND GUIDEWALLS - MAIN TABLE
                # -----------------------------------------
                
                if "Canal_bed_and_guide_walls" in repair_types:
                
                    st.subheader("🧱 Canal Bed and Guidewalls")
                
                    # =========================================
                    # 1. CANAL BED / REPLACEMENT
                    # =========================================
                
                    st.markdown("### Canal Bed / Replacement")
                
                    bed_cols = [
                        "cbagw-chainage_cbagw_from",
                        "cbagw-chainage_cbagw_to",
                        "cbagw-length_canalbed_guidewall_tobe_replaced",
                        "cbagw-canal_breadth_cbagw",
                        "cbagw-basement_depth_cbagw",
                        "cbagw-cc_1_4_8_thickness_cbagw"
                    ]
                
                    available_bed_cols = [
                        col for col in bed_cols
                        if col in village_df.columns
                    ]
                
                    if available_bed_cols:
                
                        bed_df = village_df[available_bed_cols].copy()
                
                        bed_df = bed_df.rename(columns={
                            "cbagw-chainage_cbagw_from":
                                "Chainage From",
                            "cbagw-chainage_cbagw_to":
                                "Chainage To",
                            "cbagw-length_canalbed_guidewall_tobe_replaced":
                                "Length to be Replaced-m",
                            "cbagw-canal_breadth_cbagw":
                                "Canal Breadth-m",
                            "cbagw-basement_depth_cbagw":
                                "Basement Depth-m",
                            "cbagw-cc_1_4_8_thickness_cbagw":
                                "CC 1:4:8 Thickness-m"
                        })
                
                        st.dataframe(
                            bed_df,
                            use_container_width=True,
                            hide_index=True
                        )
                
                    # =========================================
                    # 2. GUIDEWALLS
                    # =========================================
                
                    st.markdown("### Guidewalls")
                
                    guidewall_cols = [
                        "cbagw-guidewalls_nos_cbagw",
                        "cbagw-guidewall_breadth_cbagw",
                        "cbagw-guidewall_height_cbagw"
                    ]
                
                    available_guidewall_cols = [
                        col for col in guidewall_cols
                        if col in village_df.columns
                    ]
                
                    if available_guidewall_cols:
                
                        guidewall_df = village_df[
                            available_guidewall_cols
                        ].copy()
                
                        guidewall_df = guidewall_df.rename(columns={
                            "cbagw-guidewalls_nos_cbagw":
                                "Guidewalls Nos.",
                            "cbagw-guidewall_breadth_cbagw":
                                "Guidewall Breadth-m",
                            "cbagw-guidewall_height_cbagw":
                                "Guidewall Height-m"
                        })
                
                        st.dataframe(
                            guidewall_df,
                            use_container_width=True,
                            hide_index=True
                        )
                
                    # =========================================
                    # 3. CONCRETE / REMOVAL
                    # =========================================
                
                    st.markdown("### Concrete / Removal")
                
                    concrete_cols = [
                        "cbagw-toremove_old_guidewall_cc136_cbagw",
                        "cbagw-toremove_oldbedconcrete_cc148_cbagw",
                        "cbagw-volume_concrete_cc148",
                        "cbagw-volume_concrete_cc136"
                    ]
                
                    available_concrete_cols = [
                        col for col in concrete_cols
                        if col in village_df.columns
                    ]
                
                    if available_concrete_cols:
                
                        concrete_df = village_df[
                            available_concrete_cols
                        ].copy()
                
                        concrete_df = concrete_df.rename(columns={
                            "cbagw-toremove_old_guidewall_cc136_cbagw":
                                "Old Guidewall CC 1:3:6 to Remove",
                            "cbagw-toremove_oldbedconcrete_cc148_cbagw":
                                "Old Bed Concrete CC 1:4:8 to Remove",
                            "cbagw-volume_concrete_cc148":
                                "Concrete Volume CC 1:4:8-cum",
                            "cbagw-volume_concrete_cc136":
                                "Concrete Volume CC 1:3:6-cum"
                        })
                
                        st.dataframe(
                            concrete_df,
                            use_container_width=True,
                            hide_index=True
                        )
                
                    # =========================================
                    # 4. LOCATION / PHOTO
                    # =========================================
                
                    location_cols = [
                        "cbagw-gps_cbagw-Latitude",
                        "cbagw-gps_cbagw-Longitude",
                        "cbagw-image_cbagw"
                    ]
                
                    available_location_cols = [
                        col for col in location_cols
                        if col in village_df.columns
                    ]
                
                    if available_location_cols:
                
                        st.markdown("### 📍 Location / Photo")
                
                        location_df = village_df[
                            available_location_cols
                        ].copy()
                
                        location_df = location_df.rename(columns={
                            "cbagw-gps_cbagw-Latitude":
                                "GPS Latitude",
                            "cbagw-gps_cbagw-Longitude":
                                "GPS Longitude",
                            "cbagw-image_cbagw":
                                "Photo"
                        })
                
                        st.dataframe(
                            location_df,
                            use_container_width=True,
                            hide_index=True
                        )
                # -----------------------------------------
                # CANAL EXCAVATION - MAIN TABLE
                # -----------------------------------------
                
                if "Canal_excuvation" in repair_types:
                
                    st.subheader("🚜 Canal Excavation")
                
                    # =========================================
                    # 1. CANAL EXCAVATION MEASUREMENTS
                    # =========================================
                
                    st.markdown("### Canal Excavation Measurements")
                
                    excavation_cols = [
                        "ce-chainage_ce_from",
                        "ce-chainage_ce_to",
                        "ce-canal_length_ce",
                        "ce-canal_bed_breadth_ce",
                        "ce-canaldepth_ce",
                        "ce-soil_work_to_dig_canal"
                    ]
                
                    available_excavation_cols = [
                        col for col in excavation_cols
                        if col in village_df.columns
                    ]
                
                    if available_excavation_cols:
                
                        excavation_df = village_df[
                            available_excavation_cols
                        ].copy()
                
                        excavation_df = excavation_df.rename(columns={
                            "ce-chainage_ce_from":
                                "Chainage From",
                            "ce-chainage_ce_to":
                                "Chainage To",
                            "ce-canal_length_ce":
                                "Canal Length-m",
                            "ce-canal_bed_breadth_ce":
                                "Canal Bed Breadth-m",
                            "ce-canaldepth_ce":
                                "Canal Depth-m",
                            "ce-soil_work_to_dig_canal":
                                "Soil Work to Dig Canal"
                        })
                
                        st.dataframe(
                            excavation_df,
                            use_container_width=True,
                            hide_index=True
                        )
                
                    # =========================================
                    # 2. LOCATION / PHOTO
                    # =========================================
                
                    location_cols = [
                        "ce-gps_ce-Latitude",
                        "ce-gps_ce-Longitude",
                        "ce-image_ce"
                    ]
                
                    available_location_cols = [
                        col for col in location_cols
                        if col in village_df.columns
                    ]
                
                    if available_location_cols:
                
                        st.markdown("### 📍 Location / Photo")
                
                        location_df = village_df[
                            available_location_cols
                        ].copy()
                
                        location_df = location_df.rename(columns={
                            "ce-gps_ce-Latitude":
                                "GPS Latitude",
                            "ce-gps_ce-Longitude":
                                "GPS Longitude",
                            "ce-image_ce":
                                "Photo"
                        })
                
                        st.dataframe(
                            location_df,
                            use_container_width=True,
                            hide_index=True
                        )
                # -----------------------------------------
                # DESILTATION AT THE DAM - MAIN TABLE
                # -----------------------------------------
                
                if "Desiltation_at_the_dam" in repair_types:
                
                    st.subheader("🪨 Desiltation at the Dam")
                
                    # =========================================
                    # 1. DESILTATION MEASUREMENTS
                    # =========================================
                
                    st.markdown("### Desiltation Measurements")
                
                    desilt_cols = [
                        "datd-length_datd",
                        "datd-breadth_datd",
                        "datd-depth_datd",
                        "datd-volume_soil_datd"
                    ]
                
                    available_desilt_cols = [
                        col for col in desilt_cols
                        if col in village_df.columns
                    ]
                
                    if available_desilt_cols:
                
                        desilt_df = village_df[
                            available_desilt_cols
                        ].copy()
                
                        desilt_df = desilt_df.rename(columns={
                            "datd-length_datd":
                                "Length-m",
                            "datd-breadth_datd":
                                "Breadth-m",
                            "datd-depth_datd":
                                "Depth-m",
                            "datd-volume_soil_datd":
                                "Soil Volume-cum"
                        })
                
                        st.dataframe(
                            desilt_df,
                            use_container_width=True,
                            hide_index=True
                        )
                
                    # =========================================
                    # 2. LOCATION / PHOTO
                    # =========================================
                
                    location_cols = [
                        "datd-gps_ce-Latitude",
                        "datd-gps_ce-Longitude",
                        "datd-gps_ce-Altitude",
                        "datd-gps_ce-Accuracy",
                        "datd-image_ce"
                    ]
                
                    available_location_cols = [
                        col for col in location_cols
                        if col in village_df.columns
                    ]
                
                    if available_location_cols:
                
                        st.markdown("### 📍 Location / Photo")
                
                        location_df = village_df[
                            available_location_cols
                        ].copy()
                
                        location_df = location_df.rename(columns={
                            "datd-gps_ce-Latitude":
                                "GPS Latitude",
                            "datd-gps_ce-Longitude":
                                "GPS Longitude",
                            "datd-gps_ce-Altitude":
                                "GPS Altitude",
                            "datd-gps_ce-Accuracy":
                                "GPS Accuracy",
                            "datd-image_ce":
                                "Photo"
                        })
                
                        st.dataframe(
                            location_df,
                            use_container_width=True,
                            hide_index=True
                        )
                # -----------------------------------------
                # CANAL DESILTATION - MAIN TABLE
                # -----------------------------------------
                
                if "Canal_desiltation" in repair_types:
                
                    st.subheader("🪨 Canal Desiltation")
                
                    # =========================================
                    # 1. CANAL DESILTATION MEASUREMENTS
                    # =========================================
                
                    st.markdown("### Canal Desiltation Measurements")
                
                    desilt_cols = [
                        "cd-chainage_cd_from",
                        "cd-chainage_cd_to",
                        "cd-canal_length_cd",
                        "cd-canal_upper_breadth_mathati_cd",
                        "cd-canalbed_breadth_cd",
                        "cd-soil_dunes_height_cd",
                        "cd-volume_soil_tobe_removed_canal_cd"
                    ]
                
                    available_desilt_cols = [
                        col for col in desilt_cols
                        if col in village_df.columns
                    ]
                
                    if available_desilt_cols:
                
                        canal_desilt_df = village_df[
                            available_desilt_cols
                        ].copy()
                
                        canal_desilt_df = canal_desilt_df.rename(columns={
                            "cd-chainage_cd_from":
                                "Chainage From",
                            "cd-chainage_cd_to":
                                "Chainage To",
                            "cd-canal_length_cd":
                                "Canal Length-m",
                            "cd-canal_upper_breadth_mathati_cd":
                                "Canal Upper Breadth-m",
                            "cd-canalbed_breadth_cd":
                                "Canal Bed Breadth-m",
                            "cd-soil_dunes_height_cd":
                                "Soil Dunes Height-m",
                            "cd-volume_soil_tobe_removed_canal_cd":
                                "Soil Volume to Remove-cum"
                        })
                
                        st.dataframe(
                            canal_desilt_df,
                            use_container_width=True,
                            hide_index=True
                        )
                
                    # =========================================
                    # 2. LOCATION / PHOTO
                    # =========================================
                
                    location_cols = [
                        "cd-gps_ce-Latitude",
                        "cd-gps_ce-Longitude",
                        "cd-image_ce"
                    ]
                
                    available_location_cols = [
                        col for col in location_cols
                        if col in village_df.columns
                    ]
                
                    if available_location_cols:
                
                        st.markdown("### 📍 Location / Photo")
                
                        location_df = village_df[
                            available_location_cols
                        ].copy()
                
                        location_df = location_df.rename(columns={
                            "cd-gps_ce-Latitude":
                                "GPS Latitude",
                            "cd-gps_ce-Longitude":
                                "GPS Longitude",
                            "cd-image_ce":
                                "Photo"
                        })
                
                        st.dataframe(
                            location_df,
                            use_container_width=True,
                            hide_index=True
                        )
    
        
    elif page != "2.Rejuvenation_works":
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
