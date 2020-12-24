import streamlit as st
import SessionState
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import plotly.express as px
import pandas as pd
import ols
import base64
import substrate_models as sm






st.set_page_config(layout="wide")
# st.markdown("""
# <style>
# body {
#     color: #fff;
#     background-color: #111;
# }
# </style>
#     """, unsafe_allow_html=True)

# functions
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)

local_css("style.css")







#sidebar
def main():

   

    if st.sidebar.selectbox('Choose Your Project', ['Open Single Limiting Nutrient Project', 'Open Multiple Limiting Nutrients Project', 'Open Inhibition Model Project'] ):
        bioreactor=st.sidebar.selectbox('Bioreactor setup', ['Batch', 'Continous'])
        kinetics_chosen=st.sidebar.selectbox('Biological Kinetics', ['Monod', 'Substrate Inhibition', 'Product Inhibition'])


   


    
    #If the batch operation is chosen, the physical parameters such as flow rate, volume,dilution rate, retention time are hidden and cannot be edited by the user
    if bioreactor == 'Batch':
        st.image('Images/batch.png')
    else:
        st.image('Images/continuous.png')

    col1,col2,col3 = st.beta_columns(3)
    col1.selectbox('Reactant', ['Glucose', 'Xylose', 'Fructose', 'Other'])

    col2.image('Images/reaction.png', width= 200)


    col3.selectbox('Product', ['Organic Acids', 'Ethanol', 'Hydrogen', 'Other'])
        
    session_state = SessionState.get(name="", button_sent=False)
    button_sent = st.button('Click here to enter your data')

    if button_sent:
        session_state.button_sent = True

    if session_state.button_sent:
    

        with st.beta_expander('Operation parameters'):
            col1, col2, col3 = st.beta_columns(3)
            col1.markdown('')
            col1.markdown("<div> <span class='highlight blue'>Simulation Time <span class='bold'></div>", unsafe_allow_html=True)
            time = col2.number_input('')
            col3.selectbox('',['hours', 'minutes'])
            

        #operating conditions
            col1_1, col2_1, col3_1 = st.beta_columns(3)
            col1_1.markdown('')
            col1_1.markdown("<div> <span class='highlight blue'>Steptime, deltaT <span class='bold'></div>", unsafe_allow_html=True)
            delta_t = col2_1.number_input('', key=1)
            col3_1.selectbox('',['hours', 'minutes'], key=1)
        
        #Initial concentration
        with st.beta_expander('Initial concentrations'):
            col1_2, col2_2, col3_2 = st.beta_columns(3)
            col1_2.markdown('')
            col1_2.markdown("<div> <span class='highlight blue'>Biomass concentration<span class='bold'></div>", unsafe_allow_html=True)
            biomass_concentration= col2_2.number_input('', key=2)
            col3_2.selectbox('',['mg/L', 'g/L', 'mg/m3','g/m3'])

            ## substrate concenration

            col1_3, col2_3, col3_3 = st.beta_columns(3)
            col1_3.markdown('')
            col1_3.markdown("<div> <span class='highlight blue'>Substrate concentration<span class='bold'></div>", unsafe_allow_html=True)
            substate_concentration= col2_3.number_input('', key=3)
            col3_3.selectbox('',['mg/L', 'g/L', 'mg/m3','g/m3'], key=1)

            ## Product concentration
            col1_4, col2_4, col3_4 = st.beta_columns(3)
            col1_4.markdown('')
            col1_4.markdown("<div> <span class='highlight blue'>Product concentration<span class='bold'></div>", unsafe_allow_html=True)
            product_concentration=col2_4.number_input('', key=4)
            col3_4.selectbox('',['mg/L', 'g/L', 'mg/m3','g/m3'], key=2)

        with st.beta_expander('Substrate Parameters'):
            col1_6, col2_6, col3_6 = st.beta_columns(3)
            col1_6.markdown('')
            biomass_yield= col1_6.markdown("<div> <span class='highlight blue'>'Biomass Yield (Yx/s)<span class='bold'></div>", unsafe_allow_html=True)
            col2_6.number_input('', key=5)
            col3_6.selectbox('',['mg X/ mg S'])
                

            col1_7, col2_7, col3_7, col4_7 = st.beta_columns(4)
            col1_7.markdown('')
            col1_7.markdown("<div> <span class='highlight blue'>Max growth rate, umax<span class='bold'></div>", unsafe_allow_html=True)
            mumax=col2_7.number_input('', key=6)
            col3_7.selectbox('',['L/hour'])
            col4_7.markdown('')
            col4_7.markdown('')
            col4_7.checkbox('umax temperature correlation')

            col1_8, col2_8, col3_8, col4_8 = st.beta_columns(4)
            col1_8.markdown('')
            col1_8.markdown("<div> <span class='highlight blue'>'Decay constant, b'<span class='bold'></div>", unsafe_allow_html=True)
            decay_constant=col2_8.number_input('', key=7)
            col3_8.selectbox('',['1/hour'] , key=1)
            col4_8.markdown('')
            col4_8.markdown('')
            col4_8.checkbox('b temperature correlation')

            col1_9, col2_9, col3_9= st.beta_columns(3)
            col1_9.markdown('')
            col1_9.markdown("<div> <span class='highlight blue'> Half saturation concentration, Ks <span class='bold'></div>", unsafe_allow_html=True)
            Ks=col2_9.number_input('', key=8)
            col3_9.selectbox('',['mg/L'] , key=1)
        
            col1_10, col2_10, col3_10= st.beta_columns(3)
            col1_10.markdown('')
            col1_10.markdown("<div> <span class='highlight blue'> Substrate maintenance coefficient, mS <span class='bold'></div>", unsafe_allow_html=True)
            mS=col2_10.number_input('', key=9)
            col3_10.selectbox('',['1/hours'] , key=3)

        #Product Parameters
        with st.beta_expander('Product Parameters'):
            col1_11, col2_11, col3_11= st.beta_columns(3)
            col1_11.markdown('')
            col1_11.markdown("<div> <span class='highlight blue'> Product Type <span class='bold'></div>", unsafe_allow_html=True)
            col2_11.radio('',['Growth Associated', 'Non-growth Associated', 'Mixed'])
            kpg=col3_11.number_input('Kpg', key=3)
            kpng=col3_11.number_input('Kpng', key=3)

    #Product yied
            col1_12, col2_12, col3_12= st.beta_columns(3)
            col1_12.markdown('')
            col1_12.markdown("<div> <span class='highlight blue'> Product Yield, Ypl/s <span class='bold'></div>", unsafe_allow_html=True)
            product_yield=col2_12.number_input('', key=10)
            col3_12.selectbox('',['mg P /mg S'], key=3)

    # Product maintenance
            col1_12, col2_12, col3_12= st.beta_columns(3)
            col1_12.markdown('')
            col1_12.markdown("<div> <span class='highlight blue'> Product maintenance coefficient, mP <span class='bold'></div>", unsafe_allow_html=True)
            product_maintenance=col2_12.number_input('', key=11)
            col3_12.selectbox('', ['1/hours'], key=4)


    if st.button("Simulate"):
        def dx_dt(x, t, mu, xmax):
            '''Logistic equation (Chandrashekar et al 1999)'''
            return mu* x* (1- x/xmax)

    # mu = 1. 
    # xmax = 30.
    # x0 = 10.
        t = np.linspace(0., int(time),  int(delta_t))
        N = odeint(dx_dt, biomass_concentration, t, args=(mumax, (biomass_concentration+10
    )))
        fig = px.line(x=t, y=N, labels=dict(x= 'Time', y='Biomass concentration'))
        fig.update_layout( title= {'text':f"{kinetics_chosen}", 'xanchor': 'center', 'yanchor': 'top'}, autosize=False,
                  width=800, height=800,
                  margin=dict(l=40, r=40, b=40, t=40), 
                  font= dict(size= 15)
                  
)
        st.plotly_chart(fig)

    dataset = pd.DataFrame({'X': t, 'Y': N.ravel()}, columns=['X', 'Y'])


    st.markdown('# Studentized Residuals')

    st.write(ols.get_residuals(dataset, 'Y'))

    



    

    selected_equations = st.multiselect("Select One or more inhibition models", ["Monod (No inhibition)", "Competive inhibiton", "Non-competitive inhibition", "Edward's Model", "Andrew's Model", "Modified Steele's Model"])

    # if selected_equations == "Monod (No inhibition)":
    st.write(sm.monod(1,1,1))




        # if selected_equations == "Monod (No inhibition)":
        #     st.latex('$\mu=\frac{\hat{\mu} S_{S}}{S_{S}+K_{S}}$')

    def download_link(object_to_download, download_filename, download_link_text):
        """
        Generates a link to download the given object_to_download.

        object_to_download (str, pd.DataFrame):  The object to be downloaded.
        download_filename (str): filename and extension of file. e.g. myata.csv, some_txt_output.txt
        download_link_text (str): Text to display for download link.

        Examples:
        download_link(YOUR_DF, 'YOUR_DF.csv', 'Click here to download data!')
        download_link(YOUR_STRING, 'YOUR_STRING.txt', 'Click here to download your text!')

        """
        if isinstance(object_to_download,pd.DataFrame):
            object_to_download = object_to_download.to_csv(index=False)

        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()

        return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'


# Examples
    
    button_download = st.button('Download Dataframe as CSV')
    if button_download:
  
        tmp_download_link = download_link(dataset, 'YOUR_DF.csv', 'Click here to download your data!')
        st.markdown(tmp_download_link, unsafe_allow_html=True)

    # Non-inhibiting and biomass inhibition models

    

    # s = st.text_input('Enter text here')
    # st.write(s)

# if st.button('Download input as a text file'):
#     tmp_download_link = download_link(s, 'YOUR_INPUT.txt', 'Click here to download your text!')
#     st.markdown(tmp_download_link, unsafe_allow_html=True)
    
    # Simulations

    # ########Functions###############################

    # Define a function which calculates the derivative
    
   

if __name__ == "__main__":
    main()



            
        
    #####Caalls######################
    # 

   

    

    
    

    

    
    

    

  
#write(sympy_expr)
