import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

def train(data):
    try:
        df = pd.DataFrame(data=data)
        xTrain, xTest, yTrain, yTest = train_test_split(df[[  "rpiId" , "date" ,"hour", "minute" ]], df["temp"], test_size = 0.3) 
        model = LinearRegression(n_jobs=4);
        model.fit(xTrain, yTrain,);
        pickle.dump(model, open('ubu-temp.model', 'wb'))
        return True
    except:
        return False

def pred(data):
    loaded_model = pickle.load(open('ubu-temp.model', 'rb'))
    return round(loaded_model.predict([data])[0],2)