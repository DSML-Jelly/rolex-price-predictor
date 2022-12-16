import pandas as pd
import pickle

# create a dataframe with one row for predictions
# initialize as one row with all 0s
# iterate through form data and add 1 to keys in data dictionary
def transformData(data):
    df = pd.read_csv('./data/rowPrediction.csv')

    print(df.loc[0, 'ConditionAAA'])

    for key, val in data.items():

        if val == 'noDiamond':
            continue
        else:
            df.loc[0, val] = 1
    # print(df.loc[0, :])

    return makePrediction(df)

def makePrediction(row):
    # load in the model and make a prediction on the row
    model = pickle.load(open('./model/lgbmmodel.pkl', 'rb'))
    
    # print("PREDICTING!!")
    # check which columns in the rowPrediction are not in 
    # for col in row.columns:
    #     if col not in model.feature_name_:
    #         print("NOT IN: ", col)
    prediction = model.predict(row)

    # prediction is stored in the first element of a list
    return round(prediction[0], 2)

# determine the top 5 features
# def featImportance(row, importances):
#     pass

if __name__ == '__main__':
    transformData([])
