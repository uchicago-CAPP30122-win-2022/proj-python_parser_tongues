from distutils.command.clean import clean
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
import numpy as np
import pandas as pd
import sqlite3 as sql 
import statsmodels.api as sm


'''
Stefan Manuel

'''

def regress(regression_cols, dependent_col, filename="data/data.csv"):
    ''''
    Assuming control and regressor filesets are both organized buy county fips code, performs a join on them 
    '''
    
    all_data = pd.read_csv(filename)    

    
    cleaned_data = all_data.dropna()
    enc = OneHotEncoder()
    svi_dummies = pd.get_dummies(cleaned_data['SVI'])
    # cleaned_data = cleaned_data.transform(np.log )
    cleaned_data = pd.concat([cleaned_data, svi_dummies], axis=1)
    model = LinearRegression(fit_intercept = False).fit(cleaned_data[regression_cols], cleaned_data[dependent_col])
    # model = sm.WLS(cleaned_data[dependent_col], cleaned_data[regression_cols], weights=cleaned_data['Population']).fit()
    # model = sm.GLS(cleaned_data[dependent_col], cleaned_data[regression_cols]).fit()
    rv = model.coef_
    rv = pd.DataFrame(data = rv, columns = regression_cols)
    # print(model.summary())

    return rv

regression_cols = [ 'Was Winner Democrat?', 'UNEMP', 'INCOME', 'Population', "Metro Status", 'Population 65 Plus', 'A', 'B', 'C', 'D' ]
dependent_col = ['Complete 18 Plus Percent']
data = "data/data.csv"
print(regress(regression_cols, dependent_col, data))



