import app_2
import help_1
import about
import streamlit as st

from multiapp import MultiApp
app = MultiApp()
st.sidebar.image('Images/1748083.png', width= 100)
app.add_app("Bioferm Application", app_2.app)
app.add_app("help", help_1.app)
app.add_app("About", about.app)
app.run()