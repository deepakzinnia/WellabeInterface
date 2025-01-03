*** Settings ***
Library    FeatureFile.py

*** Variables ***
${path}=  C:/Users/SING31/Documents/All Jira/Welbi project/Wellabe.DWarehouse.Feat.20241105.20241031.xlsx
${sheetName}=  Data
${contract}=  ADA1000001
${feat_type}=  FREELOOK
${planCode}=  WBFDAV03


*** Test Cases ***
Feature File Row validation:
    Validate Data    ${path}    ${sheetName}    ${contract}    ${feat_type}    ${planCode}
