import numpy as np
import pandas as pd 
import pickle
loaded_model=pickle.load(open('watermodel.sav','rb'))
data=pd.read_csv("wp.csv")
water_mean_data=pd.pivot_table(data,index=['Potability'],aggfunc='mean')
import streamlit as st
## footer
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb


def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))

def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)

def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 50px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="black",
        text_align="center",
        height="1",
        opacity=0.85
    )

    style_hr = styles(
        display="inline",
        margin=px(4, 4, 7, 0),
        #border_style="inset",
        #border_width=px(0.001)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


def footer():
    myargs = [
        "©️ PrakharJaiswal ", "                       ",
        link("https://www.linkedin.com/in", image('https://icons.getbootstrap.com/assets/icons/linkedin.svg')),
        "     ",  
        link("https://www.instagram.com/prakhar2111",image('https://icons.getbootstrap.com/assets/icons/instagram.svg')),
    ]
    layout(*myargs)
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
        return ("Water Not Fit for Drinking and the data is 70% accurate")
    elif prediction == 1:
        return ("Healthy Water Fit for Drinking and the data is 70% accurate")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# css_example = '''                                                                                                                                               
# <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    
#                                                                                                                                                                <h1><i class="fa-solid fa-droplet">Aqua Pura Model</i></h1>                                                                                                                                                          
# '''

# st.write(css_example, unsafe_allow_html=True)

def main():
    
    
    st.title('Aqua Pura Model')
    st.markdown(""" 
    **Aqua Pura** is a model which can predict if you can consume a water sample or not,  i.e., water is Potable or Not.
    
    **Potable water**, also known as drinking water, is obtained from surface and underground sources and has to be treated to fulfil drinking water requirements.
    """)
    activities=["Water Potability Prediciton","Minimum Requriment"]
    option=st.sidebar.selectbox("Select Your Option",activities)
    st.subheader(option)
    
    diagnosis = ''
    if option=="Water Potability Prediciton":
        st.subheader('Enter the following data : -')
        col1, col2 ,col3 = st.columns(3)
        with col1:
            ph = st.text_input(" ph : ")
            Hardness = st.text_input("Hardness : ")
            Solids= st.text_input("Solids : ")
        with col2:
            Chloramines = st.text_input("Chloramines : ")
            Sulfate = st.text_input("Sulfate : ")
            Conductivity = st.text_input("Conductivity : ")
            
        with col3:
            Organic_carbon = st.text_input("Organic_carbon : ")
            Trihalomethanes = st.text_input(" Trihalomethanes: ")
            Turbidity = st.text_input("Turbidity : ")
        if st.button('Test'):
            diagnosis = prediction([ph,Hardness,Solids,Chloramines,Sulfate,Conductivity,Organic_carbon,Trihalomethanes,Turbidity])
            st.success(diagnosis)
    elif option=="Minimum Requriment":
        st.subheader("The Minimum Requirement for Potable water is :")
        st.text(meand(1))
    footer()
        
if __name__ == '__main__':
    main()