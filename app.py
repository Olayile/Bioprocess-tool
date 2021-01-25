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
from calculations import yieldx, productivity
import pandas as pd





st.set_page_config(layout="wide")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)

local_css("style.css")



class  Biomass:
    pass
    
p = Biomass()



#sidebar
def main():

   
    st.sidebar.image('Images/Green Connection Icon Internet Logo (1).png', use_column_width= True)

    if st.sidebar.selectbox('Choose Your Project', ['Open Single Limiting Nutrient Project', 'Open Multiple Limiting Nutrients Project', 'Open Inhibition Model Project'] ):
        bioreactor=st.sidebar.selectbox('Bioreactor setup', ['Batch', 'Continous'])
        kinetics_chosen=st.sidebar.selectbox('Biological Kinetics', ['Monod', 'Substrate Inhibition', 'Product Inhibition'])

    st.image('Images/Untitled design.png', use_column_width= True)
    


    
    #If the batch operation is chosen, the physical parameters such as flow rate, volume,dilution rate, retention time are hidden and cannot be edited by the user
    if bioreactor == 'Batch':
        st.image('Images/batch.png')
    else:
        st.image('Images/continuous.png')

    col1,col2,col3 = st.beta_columns(3)
    col1.selectbox('Reactant', ['Glucose', 'Xylose', 'Fructose', 'Other'])

    col2.image('Images/reaction.png', width= 200)


    col3.selectbox('Product', ['Organic Acids', 'Ethanol', 'Hydrogen', 'Other'])

    st.header("Calculations")

    

    csv=st.file_uploader('Add your csv file', type=["csv"])

    if csv is not None:
        st.write(type(csv))
        df= pd.read_csv(csv)
        st.dataframe(df)

                                                                     

        st.subheader("Yield")

        product_column= st.text_input('Add the column name for the product yield you would like')
        substrate_column= st.text_input('Add the column name for the substrate column you would like')
        st.write(yieldx(df, product_column, substrate_column))


        st.subheader("Productivity")

        product_column_1 = st.text_input('Add the column name for the product yield you would like', key=1)
        time_column = st.text_input('Add the column name for the time column you would like to use')
        st.write(productivity(df, product_column_1, time_column))

        cell_column = st.text_input('Please add the cell growth column', key=1)


        col_sub, col_prod, col_cell = st.beta_columns(3)


        
        fig_substrate = px.scatter(x=df[time_column], y=df[substrate_column],  labels={'x':'t [h]', 'y':'Cs (g/L)'} )
        fig_product = px.scatter(x=df[time_column], y=df[product_column_1], labels={'x':'t [h]', 'y':'Cp (g/L)'})
        fig_cell = px.scatter(x=df[time_column], y=df[cell_column], labels={'x':'t [h]', 'y':'Cx (g/L)'} )
        


        col_sub.plotly_chart(fig_substrate)
        col_prod.plotly_chart(fig_product)
        col_cell.plotly_chart(fig_cell)



        
        
    session_state = SessionState.get(name="", button_sent=False)
    button_sent = st.button('Click here to enter your data')

    if button_sent:
        session_state.button_sent = True

    if session_state.button_sent:
    



    #########################
 




    
        time_units = ['hours', 'minutes']
        weight_units= ['mg/L', 'g/L', 'mg/m3','g/m3']
        yield_units = ['mg X/ mg S']
        def col(amount, name, variable_name, units, check_box=None):

            if amount == 3:
                col1, col2, col3 = st.beta_columns(3)
                col1.markdown('')
                col1.markdown("<div> <span class='highlight blue'>{} <span class='bold'></div>" .format(name), unsafe_allow_html=True)
                variable  = col2.number_input('', key= name)
                setattr(p, variable_name, variable)
                col3.selectbox('', units, key= name)
                
            elif amount == 4:
                col1_7, col2_7, col3_7, col4_7 = st.beta_columns(4)
                col1_7.markdown('')
                col1_7.markdown("<div> <span class='highlight blue'>{}x<span class='bold'></div>".format(name), unsafe_allow_html=True)
                variable =col2_7.number_input('', key=name)
                setattr(p, variable_name, variable)
                col3_7.selectbox('',units, key=name)
                col4_7.markdown('')
                col4_7.markdown('')
                col4_7.checkbox(check_box)


        
            

        with st.beta_expander('Operation parameters'):
            col(3, 'Simulation Time', 'time', time_units)
        

        #operating conditions
            col(3, 'Steptime, deltaT', 'delta_t', time_units)
      
        #Initial concentration
        with st.beta_expander('Initial concentrations'):
            col(3, 'Biomass concentration', 'biomass_concentration', weight_units)
           

            ## substrate concenration

            col(3, 'Substrate concentration', 'substrate_concentration', weight_units)


            ## Product concentration

            col(3, 'Product concentration', 'product_concentration', weight_units)

        with st.beta_expander('Substrate Parameters'):
            col(3, 'Biomass Yield (Yx/s)', 'biomass_yield', yield_units )

            col(4, 'Max growth rate, umax', 'mumax', ['1/hour'], 'umax temperature correlation')
                

            col(4, 'Decay constant, b', 'decay_constant', ['1/hour'], 'b temperature correlation')


            col(3, 'Half saturation concentration, Ks', 'Ks', ['mg/L'] )


            col(3, 'Substrate maintenance coefficient, mS', 'mS',['1/hours']  )
        

        #Product Parameters
        with st.beta_expander('Product Parameters'):
            col1_11, col2_11, col3_11= st.beta_columns(3)
            col1_11.markdown('')
            col1_11.markdown("<div> <span class='highlight blue'> Product Type <span class='bold'></div>", unsafe_allow_html=True)
            col2_11.radio('',['Growth Associated', 'Non-growth Associated', 'Mixed'])
            kpg=col3_11.number_input('Kpg', key=3)
            kpng=col3_11.number_input('Kpng', key=3)

    #Product yield
            col(3, 'Product Yield, Ypl/s', 'product_yield', ['mg P /mg S'] )
            
    # Product maintenance
            col(3, 'Product maintenance coefficient, mP', 'product_maintenance', ['1/hours'])


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

    ##############################################################################################
    
    



    

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

