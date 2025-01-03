import pandas as pd
import requests as rq
import numpy as np
from datetime import datetime as dt

class FeatureFile:
    BaseUrl = "https://qa-zahara-api.zinnia.io/v1/policies"

    def validate_data(self, path, sheet_name, contract, feat_type, plan_code):
        excel_row = self.getExcelData(path, sheet_name, contract, feat_type)
        api_data = self.get_api(contract , plan_code , feat_type)

        assert excel_row[0] == api_data[0], "Contract missmatch"
        assert excel_row[1] == api_data[1], "Source missmatch"
        assert excel_row[2] == api_data[2], "feat_type missmatch"
        assert excel_row[3] == api_data[3], "ELEC_DATE missmatch"
        assert excel_row[4] == api_data[4], "START_DATE missmatch"
        assert excel_row[5] == api_data[5], "END_DATE missmatch"
        assert excel_row[3] == api_data[3], "STATUS missmatch"
        assert excel_row[4] == api_data[4], "PERIOD missmatch"


        print("All data matched:  Test passed")

    def getExcelData(self, ex_path, sheet, contract, feat_type ):
        df = pd.read_excel(ex_path, engine="openpyxl", sheet_name= sheet)
        return df[(df["FEA_CONT"] == contract) & (df["FEA_FEAT_TYPE"] == feat_type)].replace(np.nan, '').values[0].tolist()

    def get_api(self, contract, plan_code, feat_type):
        api_data = []
        data = rq.get(f"{self.BaseUrl}/{plan_code}/{contract}").json()
        api_data.append(data["data"]["policyNumber"])
        api_data.append("ZINNIA")

        for i in range(len(data["data"]["policyFeatures"])):
            if data["data"]["policyFeatures"][i]["featureType"] == str(feat_type):
                api_data.append(data["data"]["policyFeatures"][i]["featureType"])
                elect_date = "" if data["data"]["policyFeatures"][i]["effectiveDate"] == None else data["data"]["policyFeatures"][i]["effectiveDate"]
                api_data.append(elect_date)
                start_date = "" if data["data"]["policyFeatures"][i]["startDate"] == None else data["data"]["policyFeatures"][i]["startDate"]
                #dt.strptime(start_date,"%Y-%m-%d").strftime("%Y-%m-%d")
                api_data.append(start_date)
                end_date = "" if data["data"]["policyFeatures"][i]["endDate"] == None else data["data"]["policyFeatures"][i]["endDate"]
                api_data.append(end_date)
                status = "" if data["data"]["policyFeatures"][i]["status"] == None else data["data"]["policyFeatures"][i]["status"]
                api_data.append(status)
                period = "" if data["data"]["policyFeatures"][i]["period"] == None else data["data"]["policyFeatures"][i]["period"]
                api_data.append(str(period))
        return api_data




