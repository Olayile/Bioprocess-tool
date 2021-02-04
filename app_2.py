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
from scipy.optimize import curve_fit
import lmfit
import sys




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


# objective function

def objective(x, a, b, c):
	return a * x + b * x**2 + c


# ODE functions
def ds_dt(Cx, t, mu, test):

    rs= mu*Cx/0.1 + 0.1*Cx/0.1 + 0.1 +test
    return rs

def dx_dt(Cx, t, mu):
    return -0.7*Cx/0.5 + mu*Cx/0.5 + 0.7

def dp_dt(alpha, beta, Cx, Cp):
    return alpha*0.7*Cx + beta*Cx - 0.6 * Cp



#fit function
def fitfunc(t, Cx0, mu):
    'Function that returns Ca computed from an ODE for a k'
    Casol = odeint(ds_dt, Cx0, t, args=(mu,))
    return Casol[:,0]



# Residual function


def residual(params, t, data):
    mu = params['mu'].value
    Cx0 = 0
    model = fitfunc(t, Cx0, mu)
    return model-data

    


#sidebar
def app():


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

    

    # User inputs file/ csv to work on

    csv=st.file_uploader('Add your csv file', type=["csv"])

    if csv is not None:
        st.write(type(csv))
        df= pd.read_csv(csv)
        column_names=df.columns.values.tolist()
        

        st.dataframe(df)


        # Yield calculation, also to be used in ODE calculations    ###########################################                                    

        st.subheader("Yield")

        product_column= st.selectbox('Add the column name for the product yield you would like', column_names)
        substrate_column= st.selectbox('Add the column name for the substrate column you would like', column_names)
        st.write(yieldx(df, product_column, substrate_column))


        # Productivity calculation
        st.subheader("Productivity")

        product_column_1 = st.selectbox('Add the column name for the product yield you would like', column_names, key=1)
        time_column = st.selectbox('Add the column name for the time column you would like to use', column_names)
        st.write(productivity(df, product_column_1, time_column))

        cell_column = st.selectbox('Please add the cell growth column', column_names, key=1)

        ## CURVE FITTING #################################
        st.header('Curve Fitting')
        col_sub, col_prod, col_cell = st.beta_columns(3)


        #  Curve fitting for substrate
        x= df[time_column]
        y= df[substrate_column]
        popt, _ = curve_fit(objective, x, y)
        a, b, c = popt
        y_substrate = objective(x, a, b, c)


        # Plot and line of best fit  for substrate
        fig_substrate = px.scatter(x=x, y=y,  labels={'x':'t [h]', 'y':'Cs (g/L)'} )
        fig_substrate.add_scatter(x=x, y=y_substrate, mode='lines')


        # Curve fitting for product
        x= df[time_column]
        y_product = df[product_column_1]
        popt, _ = curve_fit(objective, x, y_product)
        a_1, b_1, c_1 = popt
        y_products = objective(x, a_1, b_1, c_1)


         # Plot and line of best fit  for product
        fig_product = px.scatter(x=df[time_column], y=df[product_column_1], labels={'x':'t [h]', 'y':'Cp (g/L)'})
        fig_product.add_scatter(x=x, y=y_products, mode='lines')



        # Curve fitting for cell
        x= df[time_column]
        y_cell = df[cell_column]
        popt, _ = curve_fit(objective, x, y_cell)
        a_2, b_2, c_2 = popt
        y_cells = objective(x, a_2, b_2, c_2)

        # Plot and line of best fit  for cell
        fig_cell = px.scatter(x=df[time_column], y=df[cell_column], labels={'x':'t [h]', 'y':'Cx (g/L)'} )
        fig_cell.add_scatter(x=x, y=y_cells, mode='lines')


        col_sub.plotly_chart(fig_substrate)
        col_sub.latex('y = %.5f * x + %.5f * x^2 + %.5f' % (a, b, c))

        col_prod.plotly_chart(fig_product)
        col_prod.latex('y = %.5f * x + %.5f * x^2 + %.5f' % (a_1, b_1, c_1))

        col_cell.plotly_chart(fig_cell)
        col_cell.latex('y = %.5f * x + %.5f * x^2 + %.5f' % (a_2, b_2, c_2))

        ##########################################################################



         # ODE FITTING ###############################################

        st.header('Simulations and  kinetic model')

        

        cell_model=st.selectbox('Pick a cell growth model', ["Monod (No inhibition)", "Competive inhibition", "Non-competitive inhibition", "Edward's Model", "Andrew's Model", "Modified Steele's Model"])

        if cell_model == 'Monod (No inhibition)':

            # what do I add as the substrate, etc in the function
            #Do I need to find optimize the parameters?
            # optimizing cell growth parameters then using it in ODE
            # how to set parameters using classes
            #MAKE A CLASS WHICH OPTIMIZES TO GET MU ASWELL AS OPTIMIZES THE ACTUAL21    

            mu = sm.monod(0, 0, 0)

        elif cell_model == 'Competive inhibition':
            mu = sm.competitive(0, 0, 0 , 0)

        elif cell_model == 'Non-competitive inhibition':
            mu = sm.non_competitive(0,0,0,0)

        elif cell_model == "Edward's Model":
            mu = sm.edwards(0,0,0,0,0)

        elif cell_model == "Andrew's Model":
            mu = sm.andrews(0,0,0,0)

        elif cell_model == "Modified Steele's Model":
            mu = sm.mod_steeles
            


         
            def fitfunc(t, Cx0, mu, test):
                'Function that returns Ca computed from an ODE for a k'
                Casol = odeint(ds_dt, Cx0, t,  args=(mu,test))
                return Casol[:,0]

            def residual(params, mu,  t, data):
                # mu = params['mu'].value
                test = params['test'].value
                Cx0 = 0
                model = fitfunc(t, Cx0, mu, test)
                return model-data

            col1, col2 = st.beta_columns(2)
            fit_types ={'lmfit':col1, 'differential_evolution':col2}
            # Parameter estimation lmfit

            for k, v in fit_types.items():

    

                params = lmfit.Parameters()
                # params.add('mu', value=0.2, min=0, max=10)
                params.add('test', value=0.2, min=0, max=10)
                o1 = lmfit.minimize(residual, params, args=(mu, df[time_column], df[cell_column]), method=k, nan_policy='omit')

            




                v.header(' With {} estimation'.format(k))

                fig_ode_cell = px.scatter(x=df[time_column], y=df[cell_column], labels={'x':'t [h]', 'y':'Cx (g/L)'} )
                fig_ode_cell.add_scatter(x=df[time_column], y=df[cell_column]+o1.residual, mode='lines')

                v.plotly_chart(fig_ode_cell)
                

                fit_report = lmfit.report_fit(o1)

                param_dict =[]
                

                for name, param in o1.params.items():
                    param_dict.append([name, param.value, param.stderr, param.init_value, param.correl, param.expr, param.max, param.min, param.vary])

                data_df = pd.DataFrame(param_dict,columns=['name', 'param.value', 'param.stderr', 'param.init_value', 'param.correl', 'param.expr', 'param.max', 'param.min', 'param.vary'])
                v.dataframe(data_df)
                st.write(mu)

        



        
        
        
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
    

    

