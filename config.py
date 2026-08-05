FORMS = {
    "A. Preliminary_assessment": {
        "form_id": "Preliminary_assessment",
        "columns": ["geo-district","geo-block","geo-gp","geo-village","geo-village_gps","pa-work","pa-water_storage_months","pa-gps","pa-total_hhs","pa-pvtg_hhs","pa-irrigated_hhs","pa-irrigated_acres","pa-pipeline_suitable","pa-checkdam","pa-applied_for_grant","pa-applied_in","pa-working_ngo","pa-ngo","pa-grazing","pa-contribution","pa-irrigated_ext_rabi","pa-need_to_work","pa-village_person_name","pa-village_person_phone","pa-survey_by"],
        "column_labels": {"geo-district": "District","geo-block": "Block","geo-gp": "GP","geo-village": "village","geo-village_gps": "Village GPS","pa-work": "Type of work","pa-water_storage_months": "No.of months water will store","pa-gps": "Structure GPS","pa-total_hhs": "Total HHs","pa-pvtg_hhs": "PVTG HHs","pa-irrigated_hhs": "HHs undedr irrigation","pa-irrigated_acres": "Present irrigated area","pa-pipeline_suitable": "Suitable for pipeline","pa-checkdam": "Checkdam available","pa-applied_for_grant": "Applied for grant","pa-applied_in": "Applied in","pa-working_ngo": "Working NGO","pa-ngo": "NGO name","pa-grazing": "Grazing type","pa-contribution": Community ready contribution","pa-irrigated_ext_rabi": "Irrigated extent in Rabi","pa-need_to_work": "Need to work","pa-village_person_name": "Name of the Village cont person","pa-village_person_phone": "Phone no","pa-survey_by": "Survey by"},
        "landscape_col": "geo-village"
    },
    "1. Basic Information": {
        "form_id": "Basic_info",
        "columns": ["geo-district","geo-block","geo-gp","geo-village","Households-community","Households-total_hhs","whs-hhs_covered","Households-population","enumerator-Jalamithra"],
        "column_labels": {"geo-district": "District","geo-block": "Block","geo-gp": "GP","geo-village": "Village","Households-community": "Community","Households-total_hhs": "Total HHs","whs-hhs_covered": "Househods covered","Households-population": "Population","enumerator-Jalamithra": "Jalamithra"},
        "landscape_col": "geo-village"
    },
    "1.1 Water Discharge": {
        "form_id": "1.1 Discarge",
        "columns": ["basic_info-Date","basic_info-block","basic_info-gp","basic_info-village","basic_info-name_water_source","discharge-Discarge","enumerator-Jalamithra"],
        "column_labels": {"basic_info-Date": "Date","basic_info-block": "Block","basic_info-gp": "GP","basic_info-village": "Village","basic_info-name_water_source": "Water source name","discharge-Discarge": "Discharge-Litrs/sec","enumerator-Jalamithra": "Jalamithra"},
        "landscape_col": "basic_info-village"
    },
    "2- Rejuvenation Works-Repairs": {
        "form_id": "2-Rejuvenation_works",
        "columns": ["SubmissionDate","basic_details_repairs-block","basic_details_repairs-gp","basic_details_repairs-village","checkdam_repairs"],
        "column_labels": {"SubmissionDate": "Date","basic_details_repairs-block": "Block","basic_details_repairs-gp": "GP","basic_details_repairs-village": "Village","checkdam_repairs": "Repairs in this structure"},
        "landscape_col": "basic_details_repairs-village"
    },
    "3-New Irrigation Sources": {
        "form_id": "3.New Irrigation Sources",
        "columns": ["new_irri_structr-block","new_irri_structr-gp","new_irri_structr-village","new_irri_structr-villages_under_proposed_system","new_irri_structr-Source_name","new_irri_structr-source_elevation","new_irri_structr-Ayacut_elevation","new_irri_structr-in_hieght","new_irri_structr-distance_proposed_site_to_ayacut_mtrs","new_irri_structr_-families_covered_under_irrigation","new_irri_structr_-total_land_village_acrs","new_irri_structr_-proposed_ayacut_acrs","enumerator-Jalamithra"],
        "column_labels": {"new_irri_structr-block": "Block","new_irri_structr-gp": "GP","new_irri_structr-village": "Village","new_irri_structr-villages_under_proposed_system": "No of villages covered","new_irri_structr-Source_name": "Water source","new_irri_structr-source_elevation": "Elevation of source","new_irri_structr-Ayacut_elevation": "elevation of ayacut","new_irri_structr-in_hieght": "Which is in height","new_irri_structr-distance_proposed_site_to_ayacut_mtrs": "Distance- site to ayacut/meters","new_irri_structr_-families_covered_under_irrigation": "Families covered","new_irri_structr_-total_land_village_acrs": "Total village land-acres","new_irri_structr_-proposed_ayacut_acrs": "Proposed ayacut-acres","enumerator-Jalamithra": "Jalamithra"},
        "landscape_col": "new_irri_structr-village"
    },
    "6. Lead_statement": {
        "form_id": "6. Lead_statement",
        "columns": ["lead_statement-block","lead_statement-gp","lead_statement-village","sand-plainroad_kms_from_Kothavala","sand-ghatroad_kms_from_Kothavalas","metal-plainroad_kms_mamidipalli_metal","metal-ghatroad_kms_mamidipalli_metal","ud-chc_equipmnt_hired_farmer","ud-chc_equipmnt_total_hours_used","stone-place_stone","enumerator-Jalamithra"],
        "column_labels": {"lead_statement-block": "Block","lead_statement-gp": "GP","lead_statement-village": "Village","sand-plainroad_kms_from_Kothavala": "Distance from Kothavalasa for sand-km's","sand-ghatroad_kms_from_Kothavalas": "ghat KMs from Kothavalasa","metal-plainroad_kms_mamidipalli_metal": "Distance from Mamidipalli-metals","metal-ghatroad_kms_mamidipalli_metal": "Ghat Kms from Mamidipalli","stone-place_stone": "Place for stone","enumerator-Jalamithra": "Jalamithra"},
        "landscape_col": "lead_statement-village"
    }
}
