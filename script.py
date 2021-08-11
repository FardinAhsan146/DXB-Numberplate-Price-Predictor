from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBRegressor
import pandas as pd
import numpy as np
import re

def predict_price(number):
    
    d = {'Number': [number],
        'Code_encoded': [0]}
    val_X = pd.DataFrame(data = d)
    
    xgb_model = XGBRegressor()
    xgb_model.fit(train_X, train_y)
    return f'Predicted price for number {number} is {xgb_model.predict(val_X)[0]:.2f} AED'        

if __name__ == '__main__':

    plates = pd.read_csv('num_plates.csv')
    plates = plates[['Number', 'Code', 'Price']]

    plates['Price'] = plates['Price'].\
    apply(lambda x: re.sub(r"[a-zA-Z,]",'',x)).astype(int)
    plates['Full_plate'] = plates['Code'] + '-' +  plates['Number'].astype(str)

    #Encode categorical values, turns letters into numbers
    label_encoder = LabelEncoder()
    plates['Code_encoded'] = label_encoder.fit_transform(plates['Code'])

    # Create X and Y
    y = plates['Price']
    features = ['Number','Code_encoded']
    X = plates[features]

    # Create the test train split
    train_X, val_X, train_y, val_y = train_test_split(X, y,random_state = 0)