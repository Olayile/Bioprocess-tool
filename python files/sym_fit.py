from symfit import Parameter, variables, Fit, ODEModel, Eq, Ge, D
import numpy as np
from symfit.core.minimizers import DifferentialEvolution


def modeling(pdata, xdata, sdata, tdata):
    X, S, P, t = variables('X, S, P, t')
    k = Parameter('k', 0.1)   
    umax = Parameter('umax',min=0.06, max= 0.25) 
    Ki = Parameter('Ki',min= 10, max= 80)  
    Ks = Parameter('Ks',min=0.5, max= 8)  
    Kip = Parameter('Kip',min= 10, max= 17) 
    mx = Parameter('mx', min= 0.001, max = 0.1)
    alpha = Parameter('alpha',min= 0.1, max= 2.4)
    beta = Parameter('beta',min=0.001, max= 1.2)
    X0= 0.01
    S0 = 50
    P0 = 0.01

    model_dict = {
        D(X, t): umax*S/(Ks+S) * X,
        D(S, t): -umax*S/(Ks+S) * X,
        D(P, t): umax*S/(Ks+S)}



    ode_model_monod = ODEModel(model_dict, initial={t: 0.0, X: X0, S: S0, P: P0})

    fit = Fit(ode_model_monod, t=tdata, X=xdata, S=sdata, P= pdata)
    fit_result = fit.execute()
    return ode_model_monod, fit_result