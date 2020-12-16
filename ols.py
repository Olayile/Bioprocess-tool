
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st


#create dataset
df = pd.DataFrame({'rating': [90, 85, 82, 88, 94, 90, 76, 75, 87, 86],
                   'points': [25, 20, 14, 16, 27, 20, 12, 15, 14, 19]})
def get_residuals(dat, axis):
    model = ols('X ~ Y', data=dat).fit()
    stud_res = model.outlier_test()
    x= dat[axis]
    y= stud_res['student_resid']
    plt.scatter(x, y)
    plt.axhline(y=0, color='black', linestyle='--')
    plt.xlabel('Points')
    plt.ylabel('Studentized Residuals')
    
    fig_1 = px.scatter(x=x, y=y)
    fig_1.update_layout( autosize=False,
                  width=800, height=800,
                  margin=dict(l=40, r=40, b=40, t=40), shapes=[dict(type= 'line',yref= 'y', y0= 0, y1= 0, xref= 'paper', x0= 0, x1= 14)])
                  
    return st.plotly_chart(fig_1)



