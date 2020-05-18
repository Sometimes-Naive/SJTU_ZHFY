from .models import *
import os, sys


CURRENT_YEAR = 2020

# *********************************************FILE SETTINGS*******************************************************************
BASE_DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

DATA_PATH = os.path.join(BASE_DATA_PATH, 'run')
PREPROCESS_DATA_PATH = os.path.join(BASE_DATA_PATH, 'preprocess')

FILENAME_LIST = [
    'quantity_features.json',
    'party_features.json',
    'topic_features.json'
]
# ****************************************************************************************************************

#//////////////////////////////////////////////CIVIL CASE\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

CIVIL_TOPIC_DICT = {
    'divorce_dispute': 0,
}
CIVIL_TOPIC_DIRNAME = list(CIVIL_TOPIC_DICT.keys())
CIVIL_MODEL_LIST = [
    DivorceDisputeCaseDoc,
]

CIVIL_DATABASE_LIST = [
    'TOPIC_data',
]

# ****************************************************************************************************************
PLAINTIFF_ALIAS_LIST = [
    '原告',
    '申请人',
    '上诉人'
]


DEFENDANT_ALIAS_LIST = [
    '被告',
    '被申请人',
    '被上诉人',
    '被申诉人'
]

# ****************************************************************************************************************

#//////////////////////////////////////////////CRIMINAL CASE\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
CRIMINAL_TOPIC_DICT = {
    'dangerous_driving': 0,
}
CRIMINAL_TOPIC_DIRNAME = list(CRIMINAL_TOPIC_DICT.keys())
CRIMINAL_MODEL_LIST = [
    CriminalCaseDoc,
]

CRIMINAL_DATABASE_LIST = [
    'court',
]

CRIMINAL_CASE_CAUSE_LIST = [
    '危险驾驶罪'
]

# ****************************************************************************************************************

ACCUSED_ALIAS_LIST = [
    '被告人',
    '罪犯',
    '被告'
]