import pandas as pd
import os
from pkg_resources import resource_filename

def lending_club(file_name = 'sample_credit_data.pkl'):
    """Sample test loan default data from Lending Club https://www.lendingclub.com/. Only a sample of all loans and available features is provided

    Metadata:
        id                         object - Loan ID
        loan_issue_date    datetime64[ns] - Date when loan was issued. All dates are set to fist day of the month
        default                     int64 - Flag if the loan went to default or not. 
                                            Default is defined as one of statuses: 'Late (31-120 days)', 'Late (16-30 days)', 'Default'
        loan_amnt                 float64 - Amount requested
        funded_amnt               float64 - Amount granted
        term                        int64 - Term of the loan in months
        int_rate                  float64 - Annual interest rate
        annual_inc                float64 - Annual income of the client
        fico_range_low            float64 - Fico rate range low
        fico_range_high           float64 - Fico rate range high
        long_emp                    int64 - Indicator if client is employed for longer than 5 years
        credit_grade_A              uint8 - Indicator if clients credit grade is A
        credit_grade_B              uint8 - Indicator if clients credit grade is B
        credit_grade_C              uint8 - Indicator if clients credit grade is C
        credit_grade_D              uint8 - Indicator if clients credit grade is D
        credit_grade_E              uint8 - Indicator if clients credit grade is E
        credit_grade_F              uint8 - Indicator if clients credit grade is F
        credit_grade_G              uint8 - Indicator if clients credit grade is G

    Args:
        file_name (str) : name of the file which will be loaded from the data folder

    Returns:
        credit_df (pandas.DataFrame): DataFrame with loan defaults data from lending club

    """

    filepath = resource_filename("pyrisk", os.path.join('datasets/data',file_name))

    credit_df = pd.read_pickle(filepath)

    return credit_df
