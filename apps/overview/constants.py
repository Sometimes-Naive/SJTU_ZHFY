import os


PROVINCE_ACTIVATED = '重庆'

DATA_PATH = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'data/'

PREPROCESS_DATA_PATH = DATA_PATH + 'preprocess/'



CIVIL_CASE_FILENAME = 'civil_case'
CRIMINAL_CASE_FILENAME = 'criminal_case'
ADMINISTRATIVE_CASE_FILENAME = 'adminstrative_case'
OVERALL_STATISTICS_FILENAME = 'overall_statistics'
CASE_CAUSE_FILENAME_SUFFIX = '_cause'
JSON_TYPE_SUFFIX = '.json'
FILENAME_LIST = [
    CIVIL_CASE_FILENAME, 
    CRIMINAL_CASE_FILENAME, 
    ADMINISTRATIVE_CASE_FILENAME,
    OVERALL_STATISTICS_FILENAME
]



CATEGORIES = {'civil': 0, 'criminal':1, 'administrative':2, 'overall':3}
CASE_NAMES = ['民事案件', '刑事案件', '行政案件']
CASE_CAUSE_NAMES = ['民事案由', '刑事案由', '行政案由']