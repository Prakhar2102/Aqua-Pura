import numpy as np
import pandas as pd 
import pickle
loaded_model=pickle.load(open('watermodel.sav','rb'))
data=pd.read_csv("wp.csv")
water_mean_data=pd.pivot_table(data,index=['Potability'],aggfunc='mean')
import streamlit as st

def meand(x):
    y=water_mean_data.loc[x]
    return y

def prediction(input_data):

    # input_data to numpy array : 
    input_data_as_numpy_array = np.asarray(input_data)

    # reshape the array 
    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

    # Prediction : 
    prediction = loaded_model.predict(input_data_reshaped)
    print(prediction)
    if prediction == 0:
        return ("Water Not Fit for Drinking.")
    elif prediction == 1:
        return ("Healthy Water Fit for Drinking.")


def main():   
    st.title('Aqua Pura Model')
    st.markdown(""" 
    **Aqua Pura** is a model which can predict if you can consume a water sample or not,  i.e., water is Potable or Not.
    **Potable water**, also known as drinking water, is obtained from surface and underground sources and has to be treated to fulfil drinking water requirements.
    """)
    activities=["Water Potability Prediciton","Minimum Requriments"]
    option=st.sidebar.selectbox("Select Your Option",activities)
    st.subheader(option)
    
    diagnosis = ''
    if option=="Water Potability Prediciton":
        st.subheader('Enter the following data : -')
        col1, col2 ,col3 = st.columns(3)
        with col1:
            ph = float(st.number_input("ph"))
            Hardness = float(st.number_input("Hardness (In ppm) : "))
            Solids= float(st.number_input("Solids (In mg/L) : "))
        with col2:
            Chloramines =float(st.number_input("Chloramines (In ppm) : "))
            Sulfate =float(st.number_input("Sulfate (In mg/L) : "))
            Conductivity =float(st.number_input("Conductivity (In $\mu$s/cm) : "))
            
        with col3:
            Organic_carbon =float(st.number_input("Organic_carbon (In mg/L C) : "))
            Trihalomethanes =float(st.number_input(" Trihalomethanes (In $\mu$g/L) : "))
            Turbidity =float(st.number_input("Turbidity (In NTU) : "))
        if st.button('Test for Potability'):
            diagnosis = prediction([ph,Hardness,Solids,Chloramines,Sulfate,Conductivity,Organic_carbon,Trihalomethanes,Turbidity])
            st.success(diagnosis)
            st.text("This data is 71% Accurate.")
    elif option=="Minimum Requriments":
        st.markdown(""" ##### The minimum requirement of ph, Hardness, Solids, Chloramines, Sulfate, Conductivity, Organic_carbon, Trihalomethanes, Turbidity for Potable water is :""")
        st.text(meand(1))
        
if __name__ == '__main__':
    main()
