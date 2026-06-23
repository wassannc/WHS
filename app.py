import streamlit as st
import pandas as pd
from config import FORMS
from utils import load_data, load_repeat_data
st.set_page_config(page_title="Project Dashboard", layout="wide")

# ---------------- SIDEBAR ----------------
page = st.sidebar.radio(
    "Select Form",
    [
        "Watershed Map",
        *list(FORMS.keys())
    ]
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

    else:
        
    elif page == "Watershed Map":

        st.title("🗺️ Watershed Map")

        with open("Mandal_Map.html", "r", encoding="utf-8") as f:
            html_data = f.read()

        st.components.v1.html(
            html_data,
            height=700,
            scrolling=True
        )
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
                "LTCB Works",
                "Guidewall repair",
                "Guidewall Bedjoint leakage",
                "New canal guidewall",
                "Scourvent Opening",
                "Leakage arrest",
                "Sluice gate",
                "Canal desiltation",
                "Canal guidewall height increase"
            ]
        )
        st.write("Selected:", report_type)
        
    if page == "2- Rejuvenation Works-Repairs":
        if report_type == "Main Report":
            df = load_data("2.Rejuvenation_works")
            
        elif report_type == "WSC Works":
            df = load_repeat_data(
                "2.Rejuvenation_works",
                "Submissions.wsc.wsc_"
            )
            main_df = load_data("2.Rejuvenation_works")
            df = df.merge(
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
            # SHOW ONLY REQUIRED COLUMNS
            df = df[
                [
                    "basic_details_repairs-block",
                    "basic_details_repairs-gp",
                    "basic_details_repairs-village",
                    "vent1_wsc",
                    "hole_size_diameter_vent1",
                    "valve_size_vent1"
                ]
            ]
            df=df.rename(columns={
                "basic_details_repairs-block": "Block",
                "basic_details_repairs-gp": "GP",
                "basic_details_repairs-village": "Village",
                "vent1_wsc": "Vent1",
                "hole_size_diameter_vent1": "Vent1 hole size-dia",
                "valve_size_vent1": "Vent1 valve size"
            })
            st.dataframe(df)
            st.stop()   

        elif report_type == "Guidewall repair":
            df = load_repeat_data(
                "2.Rejuvenation_works",
                "Submissions.gwr.gwr_"
            )  
            main_df = load_data("2.Rejuvenation_works")
            df = df.merge(
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
            # SHOW ONLY REQUIRED COLUMNS
            df = df[
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
            df=df.rename(columns={
                "basic_details_repairs-block": "Block",
                "basic_details_repairs-gp": "GP",
                "basic_details_repairs-village": "Village",
                "avg_length_gwr": "Avg length-mtrs",
                "avg_breadth_gwr": "Avg breadth-mtrs",
                "avg_height_gwr": "Avg height-mtrs",
                "volume_guidewall_tobe_break": "Volume- guidewall tobe break-cubmtrs",
                "volume_guidewall_tobe_constrn": "Volume guidewall tobe constructed-cubmtrs"
            })
            st.dataframe(df)
            st.stop()

        elif report_type == "Scourvent opening":
            df = load_repeat_data(
                "2.Rejuvenation_works",
                "Submissions.so"
            )  
            main_df = load_data("2.Rejuvenation_works")
            df = df.merge(
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
            # SHOW ONLY REQUIRED COLUMNS
            df = df[
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
            df=df.rename(columns={
                "basic_details_repairs-block": "Block",
                "basic_details_repairs-gp": "GP",
                "basic_details_repairs-village": "Village",
                "avg_length_so": "Avg Length",
                "avg_breadth_so": "Avg Breadth",
                "avg_height_so": "Avg Height",
                "volume_so": "Volume cubmtrs"
            })
            st.dataframe(df)
            st.stop()

        elif report_type == "Guidewall Bedjoint leakage":
            df = load_repeat_data(
                "2.Rejuvenation_works",
                "Submissions.gwbjl.gwbjl_"
            )  
            main_df = load_data("2.Rejuvenation_works")
            df = df.merge(
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
            # SHOW ONLY REQUIRED COLUMNS
            df = df[
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
            st.dataframe(df)
            st.stop()

        elif report_type == "New canal guidewall":
            df = load_repeat_data(
                "2.Rejuvenation_works",
                "Submissions.ncg.ncg_"
            )  
            main_df = load_data("2.Rejuvenation_works")
            df = df.merge(
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
            # SHOW ONLY REQUIRED COLUMNS
            df = df[
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
            st.dataframe(df)
            st.stop()
            
        elif report_type == "WC Works":
            df = load_repeat_data(
                "2.Rejuvenation_works",
                "Submissions.wc.wc_"
            )  
            main_df = load_data("2.Rejuvenation_works")
            df = df.merge(
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
            # SHOW ONLY REQUIRED COLUMNS
            df = df[
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
            df=df.rename(columns={
                "basic_details_repairs-block": "Block",
                "basic_details_repairs-gp": "GP",
                "basic_details_repairs-village": "Village",
                "avg_length_wc_leak1": "Avg Length-mtrs",
                "avg_breadth_wc_leak1": "Avg Breadth-mtrs",
                "avg_depth_wc_leak1": "Avg Depth-mtrs",
                "volume_leak1_wc": "Total volume-cubmtrs"
            })
            st.dataframe(df)
            st.stop()
            
        elif report_type == "Leakage arrest":
            df = load_repeat_data(
                "2.Rejuvenation_works",
                "Submissions.stop_leak_bodywall_repeat.stop_leak_bodywall_repeat_"
            )  
            main_df = load_data("2.Rejuvenation_works")
            df = df.merge(
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
            # SHOW ONLY REQUIRED COLUMNS
            df = df[
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
            st.dataframe(df)
            st.stop()
            
        elif report_type == "LTCB Works":
            df = load_repeat_data(
                "2.Rejuvenation_works",
                "Submissions.ltcb.ltcb_"
            )
            main_df = load_data("2.Rejuvenation_works")
            df = df.merge(
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
            # SHOW ONLY REQUIRED COLUMNS
            df = df[
                [
                    "basic_details_repairs-block",
                    "basic_details_repairs-gp",
                    "basic_details_repairs-village",
                    "canal_damaged_length_leak1",
                    "canal_damaged_breadth_leak1",
                    "cc_volume_ltcb_leak1",
                    "cc_total_volume_ltcb",
                    "area_tobe_clean_chipping_for_concrete"
                ]
            ]
            st.dataframe(df)
            st.stop()


        elif report_type == "Sluice gate":
            df = load_repeat_data(
                "2.Rejuvenation_works",
                "Submissions.slc_gt"
            )  
            main_df = load_data("2.Rejuvenation_works")
            df = df.merge(
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
            # SHOW ONLY REQUIRED COLUMNS
            df = df[
                [
                    "basic_details_repairs-block",
                    "basic_details_repairs-gp",
                    "basic_details_repairs-village",
                    "sluice_gate",
                    "sluice_gate_width",
                    "sluice_gate_height",
                    "sluice_gate_volume"
                ]
            ]
            st.dataframe(df)
            st.stop()

        elif report_type == "Canal excuvation":
            df = load_repeat_data(
                "2.Rejuvenation_works",
                "Submissions.ce"
            )  
            main_df = load_data("2.Rejuvenation_works")
            df = df.merge(
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
            # SHOW ONLY REQUIRED COLUMNS
            df = df[
                [
                    "basic_details_repairs-block",
                    "basic_details_repairs-gp",
                    "basic_details_repairs-village",
                    "soiltype_ce",
                    "canal_length_ce",
                    "soil_work_to_dig_canal"
                ]
            ]
            st.dataframe(df)
            st.stop()
        
        elif report_type == "Canal desiltation":
            df = load_repeat_data(
                "2.Rejuvenation_works",
                "Submissions.Canal_desiltation"
            )  
            main_df = load_data("2.Rejuvenation_works")
            df = df.merge(
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
            # SHOW ONLY REQUIRED COLUMNS
            df = df[
                [
                    "basic_details_repairs-block",
                    "basic_details_repairs-gp",
                    "basic_details_repairs-village",
                    "soiltype_cd",
                    "canal_length_cd",
                    "canal_upper_breadth_mathati_cd",
                    "canalbed_breadth_cd",
                    "soil_dunes_height_cd",
                    "volume_soil_tobe_removed_canal_cd"
                ]
            ]
            st.dataframe(df)
            st.stop()
        
        elif report_type == "Canal guidewall height increase":
            df = load_repeat_data(
                "2.Rejuvenation_works",
                "Submissions.Canal_guidewall_height_increase.Canal_guidewall_height_increase_"
            )  
            main_df = load_data("2.Rejuvenation_works")
            df = df.merge(
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
            # SHOW ONLY REQUIRED COLUMNS
            df = df[
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
            st.dataframe(df)
            st.stop()
        
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
