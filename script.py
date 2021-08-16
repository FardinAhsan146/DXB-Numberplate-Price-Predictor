from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.preprocessing import LabelEncoder
from sklearn import tree
from xgboost import XGBRegressor
from collections import Counter
import pandas as pd
import numpy as np
import re
import math

def predict_price(platenumber):
    
    XGB = 0
    code,number = platenumber.split('-')
    
    if len(number) > 5:
        return 'Invalid number plate'
    
    if len(number) != 5:
        XGB = 1
    
    letter_num = label_map[code]
    
    d = {'number_int':[int(number)],
        'num_digits':[len(number)],
        'Code_encoded': [letter_num],
        'unique_digits':[len(set(number))],
        'shan_entrop':[entropy(number)],
        'max_group':[Counter(number).most_common(1)[0][1]]}
    
    val_X = pd.DataFrame(data = d)
    
    return_value = xgb_model.predict(val_X)[0]\
                    if XGB else tree_model.predict(val_X)[0]

    return f'Predicted price for plate {code}-{number} is {return_value:.2f} AED'   

def entropy(string):
    '''Calculates the Shannon entropy of a string'''
    
    prob = [ float(string.count(c)) / len(string) for c in dict.fromkeys(list(string)) ]
    return - sum(p * math.log(p) / math.log(2.0) for p in prob)    

if __name__ == '__main__':

    plates = pd.read_csv('num_plates.csv')
    plates = plates[['Number', 'Code', 'Price']]

    plates['Price'] = plates['Price'].\
    apply(lambda x: re.sub(r"[a-zA-Z,]",'',x)).astype(int)

    #Encode categorical values, turns letters into numbers
    label_encoder = LabelEncoder()
    plates['Code_encoded'] = label_encoder.fit_transform(plates['Code'])
    label_map = {k:v for k,v in zip(label_encoder.classes_,range(len(label_encoder.classes_)))}
    
    plates['Number'] = plates['Number'].astype(str)
    
    plates['num_digits'] = plates['Number'].apply(lambda x: len(x))
    plates['unique_digits'] = plates['Number'].apply(lambda x: len(set(x)))
    plates['max_group'] = plates['Number'].apply(lambda x: Counter(x).most_common(1)[0][1])
    plates['shan_entrop'] = plates['Number'].apply(entropy)
    plates['number_int'] = plates['Number'].astype(int)


    # Create X and Y
    y = plates['Price']
    features = ['unique_digits', 'shan_entrop','Code_encoded','num_digits','max_group','number_int']
    X = plates[features]
    
    # Create the test train split
    train_X, val_X, train_y, val_y = train_test_split(X, y,random_state = 0)
    
    tree_model = tree.DecisionTreeClassifier()
    tree_model.fit(train_X, train_y)
    
    xgb_model = XGBRegressor()
    xgb_model.fit(train_X, train_y)

    