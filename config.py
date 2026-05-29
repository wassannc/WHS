FORMS = {
    "1. Basic Information": {
        "form_id": "Basic_info",
        "columns": ["plot_reg.date","plot_reg.landscape","plot_reg.gp","plot_reg.village","plot_reg.farmer_name","plot_reg.spouse","plot_reg.season","plot_reg.crop_model","plot_reg.main_crop","plot_reg.sowing_date"],
        "landscape_col": "plot_reg.landscape"
    },
    "1.1 Water Discharge": {
        "form_id": "1.1 Discarge",
        "columns": ["Primary_details.date","Primary_details.landscape","Primary_details.gp","Primary_details.village","Primary_details.farmer_name","Primary_details.plot_ext","crop_activity","Nf_activites.nf_inputs","Nf_activites.Other_nf_input","Nf_activites.Qty_other_nfinput"],
        "landscape_col": "Primary_details.landscape"
    },
    "2. Rejuvenation Works-Repairs": {
        "form_id": "2.Rejuvenation_works",
        "columns": ["SubmissionDate","table_list_pd.landscape","table_list_pd.brc_unit","table_list_pd.product_name","table_list_pd.brc_sale_date","table_list_pd.dj_sale_farmer","table_list_pd.gender","table_list_pd.sale_village","table_list_sd.sale_qty","table_list_sd.total_income","table_list_cd.crops","table_list_cd.crop_ext"],
        "landscape_col": "table_list_pd.landscape"
    },
    "3.New Irrigation Sources": {
        "form_id": "3.New Irrigation Sources",
        "columns": ["SubmissionDate","table_list_pd.landscape","table_list_pd.gp","table_list_pd.village","table_list_pd1.farmer_name","table_list_pd1.processing_hub_tool","table_list_pd1.processing_date","table_list_pd1.processed_for","table_list_pd2.processing_farmer_village","table_list_pd2.processing_farmer","table_list_pd2.processing_qty_kgs","table_list_pd2.rent_amount","table_list_pd3.Data_sub_by"],
        "landscape_col": "table_list_pd.landscape"
    },
    "4.New Farmpond": {
        "form_id": "4.New Farmpond",
        "columns": ["CB_info.landscape","CB_info.gp","CB_info.village","CB_info.Trainining_type","CB_info.Event_name","CB_info.Event_mode","Cb_info1.from_date","Cb_info1.days","Cb_info1.male","Cb_info1.female","Cb_info1.total_members","Cb_info1.Event_place"],
        "landscape_col": "CB_info.landscape"
    },
    "5.Trench Works": {
        "form_id": "5.SCT",
        "columns": ["SubmissionDate","basic_info.landscape","basic_info.gp","basic_info.village","basic_info.orchard_type","basic_info.farmer_add","type"],
        "landscape_col": "basic_info.landscape"
    },
    "6. Lead_statement": {
        "form_id": "6. Lead_statement",
        "columns": ["SubmissionDate","pd.landscape","pd.gp","pd.village","farm_equipmnt_hired","ASC_Entp","ud.chc_equipmnt_rented_date","ud.chc_equipmnt_hired_farmer","ud.chc_equipmnt_total_hours_used","ud.total_hired_cost"],
        "landscape_col": "pd.landscape"
    }
}
