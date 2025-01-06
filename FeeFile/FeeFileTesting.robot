*** Settings ***
Library    FeeApi.py



*** Variables ***

${path}=   C:/Users/SING31/Documents/All Jira/RAHR-8605/Wellabe..DWarehouse.Fees.20241220.20241220.xlsx
${sheetName}=  fee
${contract}=  ANN1000863
${txnNumber}=  8
${planCode}=  WBFDAV03


*** Test Cases ***
Fee File Row validation:
      Validate Data    ${path}    ${sheetName}    ${contract}    ${txnNumber}    ${planCode}
