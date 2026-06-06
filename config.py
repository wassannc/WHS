FORMS = {
    "1. Basic Information": {
        "form_id": "Basic_info",
        "columns": ["geo-district","geo-block","geo-gp","geo-village","Households-community","Households-total_hhs","Households-population","enumerator-Jalamithra"],
        "column_labels": ["geo-district": "District","geo-block": "Block","geo-gp": "GP","geo-village": "Village","Households-community": "Community","Households-total_hhs": "Total HHs","Households-population": "Population","enumerator-Jalamithra": "Jalamithra"]
        "landscape_col": "geo-village"
    },
    "1.1 Water Discharge": {
        "form_id": "1.1 Discarge",
        "columns": ["basic_info-Date","basic_info-block","basic_info-gp","basic_info-village","basic_info-name_water_source","discharge-Discarge","enumerator-Jalamithra"],
        "landscape_col": "basic_info-village"
    },
    "2- Rejuvenation Works-Repairs": {
        "form_id": "2-Rejuvenation_works",
        "columns": ["SubmissionDate","table_list_pd-landscape","table_list_pd-brc_unit","table_list_pd-product_name","table_list_pd-brc_sale_date","table_list_pd-dj_sale_farmer","table_list_pd-gender","table_list_pd-sale_village","table_list_sd-sale_qty","table_list_sd-total_income","table_list_cd-crops","table_list_cd-crop_ext"],
        "landscape_col": "basic_details_repairs-village"
    },
    "3-New Irrigation Sources": {
        "form_id": "3.New Irrigation Sources",
        "columns": ["new_irri_structr-block","new_irri_structr-gp","new_irri_structr-village","new_irri_structr-villages_under_proposed_system","new_irri_structr-Source_name","new_irri_structr-source_elevation","new_irri_structr-Ayacut_elevation","new_irri_structr-in_hieght","new_irri_structr-distance_proposed_site_to_ayacut_mtrs","new_irri_structr_-families_covered_under_irrigation","new_irri_structr_-total_land_village_acrs","new_irri_structr_-proposed_ayacut_acrs","enumerator-Jalamithra"],
        "landscape_col": "new_irri_structr-village"
    },
    "4-New Farmpond": {
        "form_id": "4-New Farmpond",
        "columns": ["CB_info-landscape","CB_info-gp","CB_info-village","CB_info-Trainining_type","CB_info-Event_name","CB_info-Event_mode","Cb_info1-from_date","Cb_info1-days","Cb_info1-male","Cb_info1-female","Cb_info1-total_members","Cb_info1-Event_place"],
        "landscape_col": "CB_info-landscape"
    },
    "5-Trench Works": {
        "form_id": "5-SCT",
        "columns": ["SubmissionDate","basic_info-landscape","basic_info-gp","basic_info-village","basic_info-orchard_type","basic_info-farmer_add","type"],
        "landscape_col": "basic_info-landscape"
    },
    "6. Lead_statement": {
        "form_id": "6. Lead_statement",
        "columns": ["lead_statement-block","lead_statement-gp","lead_statement-village","sand-plainroad_kms_from_Kothavala","sand-ghatroad_kms_from_Kothavalas","metal-plainroad_kms_mamidipalli_metal","metal-ghatroad_kms_mamidipalli_metal","ud-chc_equipmnt_hired_farmer","ud-chc_equipmnt_total_hours_used","stone-place_stone","enumerator-Jalamithra"],
        "landscape_col": "lead_statement-village"
    }
}
