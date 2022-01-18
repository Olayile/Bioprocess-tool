import substrate_models
import lmfit
from scipy.integrate import odeint



class Bacteria:
    '''Class for ODE modelling and parameter optimization'''
    def __init__(self, X=None, S= None , P= None, t=None, cell_growth_type = None):
      self.X = X
      self.S = S
      self.P = P
      self.t = t

      if cell_growth_type == 'monod':

    def mu_monod(Cs, umax, Ks):
        return (umax*Cs)/(Cs+Ks)
         
    def add_params(umax_value= None, umax_min, umax_max, Ks, ):
        #how can i do this better?
        self.params = lmfit.Parameters()
        self.params.add('umax', value=umax_value, min=umax_min, max=umax_max)
        self.params.add('Ks')
        self.params.add('Yxp')
        self.params.add('Ysp')
        self.params.add('beta')
 

    def d_celldt(self, x,  t, *args):
        umax, Ks, Yxp, Ysp, beta = args
        self.X, self.S, self.P = x 

        m= mu_monod(self.S, umax, Ks)
        dXdt = m*self.X
        dSdt = - m*self.X/Yxp
        dPdt = - m*self.X/Ysp+ beta
        return dXdt, dSdt, dPdt



    def d_solve(self):
        umax = self.params['umax'].value
        Ks = self.params['Ks'].value
        Yxp = self.params['Yxp'].value  
        Ysp = self.params['Ysp'].value 
        beta = self.params['beta'].value

        sol = odeint(dxdt, self.x0, self.t, args=(umax, Ks, Yxp, Ysp, beta))

        return sol

    self.X0 = 0.1
    self.S0 = 0.1
    self.P0 = 0.1
    self.x0 = X0, S0, P0

    def residual():
        data=[self.X, self.S, self.P]
        model = d_solve()
        resid = data - model


    


    
        









    

    


    

