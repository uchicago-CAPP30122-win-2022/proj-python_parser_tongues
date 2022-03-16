from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import statsmodels.api as sm


'''

'''

regression_cols = [ 'DEM_WON', 'UNEMP', 'INCOME', 'POP', "IS_METRO", 'POP_65UP', 'A', 'B', 'C', 'D' ]
dependent_col = ['COUN_VAX_RATE']

def regress(regression_cols, dependent_col, filename="data/data.csv"):
    ''''
    Assuming control and regressor filesets are both organized buy county fips code, performs a join on them 

    '''
    
    all_data = pd.read_csv(filename)    

    svi_dummies = pd.get_dummies(all_data['SVI'])
    all_data = pd.concat([all_data, svi_dummies], axis=1)

    cleaned_data = all_data.dropna()
    #model = LinearRegression(fit_intercept = False).fit(cleaned_data[regression_cols], cleaned_data[dependent_col])
    model1 = sm.WLS(cleaned_data[dependent_col], cleaned_data[regression_cols], weights=cleaned_data['POP']).fit()
    #model1 = sm.GLS(cleaned_data[dependent_col], cleaned_data[regression_cols]).fit()
    #rv = pd.DataFrame(data = rv, columns = regression_cols)
    fitted_vals = pd.DataFrame(data = model1.predict(all_data[regression_cols]), columns = ["Predicted Vaccine Completeness"])
    all_data = pd.concat([all_data, fitted_vals], axis=1)
    all_data.to_csv('data_predicted.csv')
    return model1.summary(), model1.params, model1.predict(all_data[regression_cols])


regression_cols = [ 'DEM_WON', 'UNEMP', 'INCOME', 'POP', "IS_METRO", 'POP_65UP', 'A', 'B', 'C', 'D' ]
dependent_col = ['COUN_VAX_RATE']
data = "data/data.csv"
regress(regression_cols, dependent_col, data)
print(regress(regression_cols, dependent_col, data)[0])



