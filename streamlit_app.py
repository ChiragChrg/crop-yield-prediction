import pickle
import streamlit as st
import pandas as pd
import numpy as np

# Loading the Saved Model
# model_data = pickle.load(open('RandomForestModel.pickle', 'rb'))
model_data = pickle.load(open('DecisionTreeModel.pickle', 'rb'))
loaded_model = model_data['model']
encoders = model_data['encoders']

# function to handle unseen labels
def transform_column(column, value, encoder):
    if value in encoder.classes_:
        return encoder.transform([value])[0]
    else:
        return encoder.transform([encoder.classes_[0]])[0]

# creating a function for Prediction
def yield_prediction(input_data):
    # Convert input_data into a DataFrame
    columns_List=['Area', 'Item', 'Year', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp']
    input_df = pd.DataFrame([input_data], columns=columns_List)

    # Standardize data
    # for column in columns_List:
    #     encoder = label_encoders[column]
    #     input_df[column] = encoder.transform(input_df[column])
    
    for column in ['Area', 'Item']:
        input_df[column] = input_df[column].apply(lambda x: transform_column(column, x, encoders[column]))

    prediction = loaded_model.predict(input_df)
    print(prediction)
    return prediction


Area_List = ['Albania', 'Algeria', 'Angola', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Belarus', 'Belgium', 'Botswana', 'Brazil', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cameroon', 'Canada', 'Central African Republic', 'Chile', 'Colombia', 'Croatia', 'Denmark', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Eritrea', 'Estonia', 'Finland', 'France', 'Germany', 'Ghana', 'Greece', 'Guatemala', 'Guinea', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'India', 'Indonesia', 'Iraq', 'Ireland', 'Italy', 'Jamaica', 'Japan', 'Kazakhstan', 'Kenya', 'Latvia', 'Lebanon', 'Lesotho', 'Libya', 'Lithuania', 'Madagascar', 'Malawi', 'Malaysia', 'Mali', 'Mauritania', 'Mauritius', 'Mexico', 'Montenegro', 'Morocco', 'Mozambique', 'Namibia', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Norway', 'Pakistan', 'Papua New Guinea', 'Peru', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Rwanda', 'Saudi Arabia', 'Senegal', 'Slovenia', 'South Africa', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Tajikistan', 'Thailand', 'Tunisia', 'Turkey', 'Uganda', 'Ukraine', 'United Kingdom', 'Uruguay', 'Zambia', 'Zimbabwe']

Crops_List = ['Maize', 'Potatoes', 'Rice, paddy', 'Sorghum', 'Soybeans', 'Wheat', 'Cassava', 'Sweet potatoes', 'Plantains and others', 'Yams']

# Year_List = [1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013]
Year_List = list(range(1900, 2101))

# Rainfall_Rate_List = [51, 56, 59, 74, 83, 89, 92, 151, 207, 216, 241, 250, 282, 285, 346, 383, 416, 447, 494, 495, 534, 536, 537, 562, 565, 589, 591, 593, 600, 608, 618, 624, 626, 630, 636, 637, 641, 652, 656, 657, 661, 686, 691, 700, 703, 748, 758, 778, 788, 832, 847, 854, 867, 1010, 1020, 1032, 1083, 1110, 1113, 1118, 1162, 1180, 1181, 1187, 1212, 1220, 1274, 1292, 1300, 1342, 1410, 1414, 1440, 1485, 1500, 1513, 1522, 1537, 1604, 1622, 1651, 1668, 1712, 1732, 1738, 1761, 1784, 1976, 1996, 2041, 2051, 2274, 2280, 2331, 2387, 2666, 2702, 2875, 3142, 3240]
Rainfall_Rate_List = list(range(0, 12000))

Temp_List = list(range(0, 61))

def format_rainfall(value):
    return f"{value} mm"

def format_temp(value):
    return f"{value} ℃"

def main():   
    st.title('Crop Yield Prediction')
    
    Area = st.selectbox('Select an Area', Area_List)
    Crop = st.selectbox('Select a Crop', Crops_List)
    # Year = st.select_slider('Select the Year', Year_List)
    # Year = st.text_input('Enter the Year')
    Year = st.selectbox("Select a year:", Year_List, index=Year_List.index(2024))
    Rainfall = st.select_slider('Select the Rainfall/year in mm', Rainfall_Rate_List, value=990, format_func=format_rainfall)
    Pesticide = st.number_input('Enter the amount of Pesticides in Tonnes',step=1)
    # Temperature = st.number_input('Enter the Average Temperature in Celsius',step=1)
    Temperature = st.select_slider("Select an Average Temperature", Temp_List, value=25, format_func=format_temp)

    diagnosis = ''
    
    if st.button('Yield Test Result'):
        result = yield_prediction([Area, Crop, Year, Rainfall, Pesticide, Temperature])[0]
        diagnosis = f"Yield: {result:.2f} hg/ha"
        
    st.success(diagnosis)


if __name__ == '__main__':
    main()