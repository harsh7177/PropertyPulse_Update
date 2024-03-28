import pandas as pd
import numpy as np
import streamlit as st
from streamlit import session_state
from sql_details import get_detail_data
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
def impute_bath(df):
    df['bath'] = pd.to_numeric(df['bath'], errors='coerce')
    mean_bathroom= df.groupby('BHK')['bath'].transform('mean').astype(int)
    df['bath'].fillna(mean_bathroom,inplace=True)
    return df


def predict_house_price(df,input_values):
    models = {
        "Random Forest": RandomForestRegressor(),
        "Gradient Boosting": GradientBoostingRegressor()
    }
    f_df=impute_bath(df)
    status_dummi=pd.get_dummies(f_df['Status'])
    f_df=df.drop(['project','Price_Sqft','id','Status','area'],axis=1)
    f_df=pd.concat([f_df,status_dummi],axis=1)
    input_dict = {
        'BHK': input_values[0],
        'Size_Sq_ft': input_values[1],
        'bath': input_values[2],
        'Ready to move': input_values[3],
        'Under Construction': input_values[4]
    }
    X_user = pd.DataFrame([input_dict])
    predictions = {'Random Forest': [], 'Gradient Boosting': []}
    errors = {'Random Forest': [], 'SVM': []}
    for name, model in models.items():
        X = f_df.drop(columns=['Price'])
        y = f_df['Price']
        model.fit(X, y)
        y_pred = model.predict(X_user)
        predictions[name] = y_pred[0]
        y_pred_all = model.predict(X)
        mse = mean_squared_error(y, y_pred_all)
        rmse = np.sqrt(mse)
        r2 = r2_score(y, y_pred_all)
        errors[name] = {'Mean Squared Error': mse, 'Root Mean Squared Error': rmse, 'R-squared': r2}
    average_predictions = np.mean(list(predictions.values()))
    return average_predictions,errors

def predict_page(suburb):
    st.write(suburb)
    table_name = session_state.loc1.lower() + "_" + suburb.replace(' ','_').lower()
    df = get_detail_data(table_name)
    bhk = st.number_input("BHK (Bedrooms, Hall, Kitchen)", min_value=1, step=1)
    size_sq_ft = st.number_input("Size (Sq. ft.)", min_value=1)
    bath = st.number_input("Number of Bathrooms", min_value=1, step=1)
    ready_to_move = st.selectbox("Ready to Move?", ["Yes", "No"])
    under_construction = st.selectbox("Under Construction?", ["Yes", "No"])
    ready_to_move = 1 if ready_to_move == "Yes" else 0
    under_construction = 1 if under_construction == "Yes" else 0
    max_value=df['Price'].max()
    if st.button("Predict"):
        # Perform prediction or any other action here
        st.success("Inputs submitted successfully!")
        prediction, errors = predict_house_price(df, [bhk, size_sq_ft, bath, ready_to_move, under_construction])
        
        # Display predicted value
        st.write(f"Predicted Value: {prediction}")
        scaled_prediction = prediction / max_value  # Scale prediction to range [0.0, 1.0]
        progress_bar = st.progress(scaled_prediction)

   
    
    
    
