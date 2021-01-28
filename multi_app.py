import app_2
import help_1
import about


from multiapp import MultiApp
app = MultiApp()
app.add_app("Bioferm Application", app_2.app)
app.add_app("help", help_1.app)
app.add_app("About", about.app)
app.run()