import streamlit as st
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
# remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

# icon("search")
# selected = st.number_input("", "Search...")
# button_clicked = st.button("OK")



#sidebar

st.sidebar.selectbox('Biological Kinetics', ['Monod', 'Substrate Inhibition', 'Product Inhibition'])


initial_conditions=st.sidebar.number_input('Initial Substrate')
units_substrate = st.sidebar.selectbox('Units',['mg/L', 'g/L', 'mg/m3','g/m3'])
# remember to change unit during analysis

initial_conditions_Product =st.sidebar.number_input('Initial Product')
units_product = st.sidebar.selectbox('Units',['mg/L', 'g/L', 'mg/m3','g/m3'], key=1)


bioreactor=st.sidebar.selectbox('Bioreactor setup', ['Batch', 'Continous'])
#If the batch operation is chosen, the physical parameters such as flow rate, volume,dilution rate, retention time are hidden and cannot be edited by the user
if bioreactor == 'Batch':
    st.image('Images/batch.png')
else:
    st.image('Images/continuous.png')

col1,col2,col3 = st.beta_columns(3)
col1.selectbox('Reactant', ['Glucose', 'Xylose', 'Fructose', 'Other'])

col2.image('Images/reaction.png', width= 200)


col3.selectbox('Product', ['Organic Acids', 'Ethanol', 'Hydrogen', 'Other'])
    

if st.button('Click here to enter your data'):

    with st.beta_expander('Operation parameters'):
        col1, col2, col3 = st.beta_columns(3)
        col1.markdown('')
        col1.markdown("<div> <span class='highlight blue'>Simulation Time <span class='bold'></div>", unsafe_allow_html=True)
        col2.number_input('')
        col3.selectbox('',['hours', 'minutes'])

    #operating conditions
        col1_1, col2_1, col3_1 = st.beta_columns(3)
        col1_1.markdown('')
        col1_1.markdown("<div> <span class='highlight blue'>Steptime, deltaT <span class='bold'></div>", unsafe_allow_html=True)
        col2_1.number_input('', key=1)
        col3_1.selectbox('',['hours', 'minutes'], key=1)
    
    #Initial concentration
    with st.beta_expander('Initial concentrations'):
        col1_2, col2_2, col3_2 = st.beta_columns(3)
        col1_2.markdown('')
        col1_2.markdown("<div> <span class='highlight blue'>Biomass concentration<span class='bold'></div>", unsafe_allow_html=True)
        col2_2.number_input('', key=2)
        col3_2.selectbox('',['mg/L', 'g/L', 'mg/m3','g/m3'])

        ## substrate concenration

        col1_3, col2_3, col3_3 = st.beta_columns(3)
        col1_3.markdown('')
        col1_3.markdown("<div> <span class='highlight blue'>Substrate concentration<span class='bold'></div>", unsafe_allow_html=True)
        col2_3.number_input('', key=3)
        col3_3.selectbox('',['mg/L', 'g/L', 'mg/m3','g/m3'], key=1)

        ## Product concentration
        col1_4, col2_4, col3_4 = st.beta_columns(3)
        col1_4.markdown('')
        col1_4.markdown("<div> <span class='highlight blue'>Product concentration<span class='bold'></div>", unsafe_allow_html=True)
        col2_4.number_input('', key=4)
        col3_4.selectbox('',['mg/L', 'g/L', 'mg/m3','g/m3'], key=2)

    with st.beta_expander('Substrate Parameters'):
        col1_6, col2_6, col3_6 = st.beta_columns(3)
        col1_6.markdown('')
        col1_6.markdown("<div> <span class='highlight blue'>'Biomass Yield (Yx/s)<span class='bold'></div>", unsafe_allow_html=True)
        col2_6.number_input('', key=5)
        col3_6.selectbox('',['mg X/ mg S'])
            

        col1_7, col2_7, col3_7, col4_7 = st.beta_columns(4)
        col1_7.markdown('')
        col1_7.markdown("<div> <span class='highlight blue'>Max growth rate, umax<span class='bold'></div>", unsafe_allow_html=True)
        col2_7.number_input('', key=6)
        col3_7.selectbox('',['L/hour'])
        col4_7.markdown('')
        col4_7.markdown('')
        col4_7.checkbox('umax temperature correlation')

        col1_8, col2_8, col3_8, col4_8 = st.beta_columns(4)
        col1_8.markdown('')
        col1_8.markdown("<div> <span class='highlight blue'>'Decay constant, b'<span class='bold'></div>", unsafe_allow_html=True)
        col2_8.number_input('', key=7)
        col3_8.selectbox('',['L/hour'] , key=1)
        col4_8.markdown('')
        col4_8.markdown('')
        col4_8.checkbox('b temperature correlation')
        
    with st.beta_expander('Product Parameters'):
        col1_9, col2_9, = st.beta_columns(2)
        

    

    

    

    
    

    

    
    

    

  
#write(sympy_expr)
