from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
import numpy as np
import pandas as pd
import sqlite3 as sql 


'''
Stefan Manuel

'''

def regress(regression_cols, dependent_col, filename):
    ''''
    Assuming control and regressor filesets are both organized buy county fips code, performs a join on them 
    '''
    
    all_data = pd.read_csv(filename)    

    
    cleaned_data = all_data.dropna()
    enc = OneHotEncoder()
    # cleaned_data = enc.fit_transform(cleaned_data)
    # cleaned_data.to_csv('temp_data.csv')
    model = LinearRegression().fit(cleaned_data[regression_cols], cleaned_data[dependent_col])
    return model.intercept_, model.coef_

regression_cols = [ 'Was Winner Democrat?', 'UNEMP', 'INCOME', 'UNEMP', 'Population', "Metro Status" ]
dependent_col = ['Completeness Percent']
data = "proj-python_parser_tongues/project/data/data.csv"
print(regress(regression_cols, dependent_col, data))



