from lmfit import minimize, Parameters, Parameter, report_fit
from scipy.integrate import odeint



def monod(S, umax, Ks):
    '''No inhibition'''
    mu=(umax*S)/(S+Ks)
    return mu


def competitive(S, umax, Ks, Ki):
    '''competitive inhibition growth rate'''
    mu= umax*S/(Ks*(1+(S/Ki))+S)
    return mu

def non_competitive(S, umax, Ks, Ki):
    mu= (umax*S/S+Ks)*(Ki/S+Ki)
    return mu

def andrews(S, umax, Ks, Ki):
    mu = umax*S/(Ks+S+(S**2/Ki))
    return mu

def edwards(S, umax, Ks, Ki, K):
    mu= umax*S/(Ks+S+(s**2/Ki)*(1+(S/K)))
    return mu


def mod_steeles():
    pass


# ODE models

def dx_dt(mu, X, t):
    '''X= bacterial growth
       mu= growth rate'''
    return mu*X


# ode model solutions

def g(mu, X, t):
    x=odeint(dx_dt, X, t)
    return x

def residual(mu, X, t, data):
    model = g(mu, X, t)
    return (model - data).ravel()


# set parameters including bounds
params = Parameters()
params.add('Ks', value=1.0, min=0, max=100)
params.add('Ki', value= 1.0, min=0, max=10)
params.add('umax', value= 1.0, min=0, max=10)

# fit model and find predicted values
result = minimize(residual, params, args=(t, data), method='leastsq')
final = data + result.residual.reshape(data.shape)