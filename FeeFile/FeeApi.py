import pandas as pd
import requests as rq
import numpy as np



class FeeApi:
    BASE_URL = "https://qa-zahara-api.zinnia.io/v1/policies"

    def get_excel_data(self, ex_path, sheet, contract, txn_number):
        df = pd.read_excel(ex_path, engine="openpyxl", sheet_name=sheet)
        filtered_row = df[(df["FEE_CONT"] == contract) & (df["FEE_TXN"] == int(txn_number))]
        filtered_row = filtered_row.replace(np.nan, '')
        excel_list = filtered_row.values[0].tolist()
        return excel_list

    def validate_data(self, path, sheet_name, contract, txn_number, plan_code):

        excel_row = self.get_excel_data(path, sheet_name, contract, txn_number)
        api_data = self.get_api(contract , plan_code , txn_number)

        assert excel_row[0] == api_data[0],  f"Contract missmatch. Api Value: {api_data[0]},  Excel value: {excel_row[0]}"
        assert excel_row[1] == api_data[1],  f"TXN_Number missmatch. Api Value: {api_data[1]},  Excel value: {excel_row[1]}"
        assert excel_row[2] == api_data[2],  f"Source missmatch. Api Value: {api_data[2]},  Excel value: {excel_row[2]}"
        assert excel_row[3] == api_data[3],  f"Desc missmatch. Api Value: {api_data[3]},  Excel value: {excel_row[3]}"
        assert excel_row[4] == api_data[4],  f"Amount missmatch. Api Value: {api_data[4]},  Excel value: {excel_row[4]}"
        assert excel_row[5] == api_data[5],  f"Status missmatch. Api Value: {api_data[5]},  Excel value: {excel_row[5]}"

        print("All data matched:  Test passed")

    def get_api(self, contract , plan_code , transID ):
        api_data = []
        response = rq.get(f"{self.BASE_URL}/{plan_code}/{contract}/transactions")
        data = response.json()
        for i in range (len(data["data"])):

            if data["data"][i]["transactionId"] == transID:
                api_data.append(data["data"][i]["policyNumber"])
                api_data.append(int(data["data"][i]["transactionId"]))
                api_data.append("ZINNIA")
                desc = "" if data["data"][i]["charges"] == None else data["data"][i]["charges"][0]
                api_data.append(desc)
                amt = "" if data["data"][i]["charges"] == None else data["data"][i]["charges"][1]
                api_data.append(amt)
                api_data.append(data["data"][i]["status"])

        return api_data




