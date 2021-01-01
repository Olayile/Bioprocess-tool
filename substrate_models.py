from lmfit import minimize, Parameters, Parameter, report_fit
from scipy.integrate import odeint


#SUBSTRTE INHIBITION RATE MODELS
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


class Bacteria:
    def __init__(self, s=None, umax=None, ks=None, ki=None, model_type = None ):
        self.s =s
        self.umax=umax
        self.ks= ks
        self.ki= ki
        

        if model_type == 'monod':
            self.user_defined_model= monod(self.s, self.umax, self.ks)

        elif model_type== 'competitive':
            self.user_defined_model = competitive(self.s, self.umax, self.ks, self.ki)


    def dx_dt(self):
        return self.user_defined_model*self.X

    def g(self):

        x= odeint(self.dx_dt, self.X, self.t)
        return x

#do i have to put self here if i am only using it in this function
    def residual(self, X=[1], t=[1]):
        self.X = X
        self.t= t
        self.calc = self.g()
        return (self.calc - self.X).ravel()

    def set_parameters(self):
        # set parameters including bounds
        self.params = Parameters()
        self.params.add('Ks', value=1.0, min=0, max=100)
        self.params.add('Ki', value= 1.0, min=0, max=10)
        self.params.add('umax', value= 1.0, min=0, max=10)

        self.result = minimize(self.residual, self.params, args=(), method='leastsq')
        self.final = self.X + result.self.residual.reshape(self.X.shape)

    def plot(self):
        plt.plot(self.t, self.X, 'o')
        plt.plot(self.t, self.final, '--', linewidth=2, c='blue');
        self.report=report_fit(self.result)



# display fitted statistics
    





# PRODUCT RATE MODELS

def gp(Kpg, mu, mp):
    ''' Growth associated products'''
    rp= kpg*mu+mp
    return rp

def non_gp(kpng, mp):
    ''' non-growth associated products'''
    rp = kpng + mp
    return rp

def mixed_gp(kpg, kpng, mu, mp):
    '''Mixed growth products'''
    rp= kpg*mu + kpng + mp
    
# ODE models

# def dx_dt(mu, X, t):
#     '''X= bacterial growth
#        mu= growth rate'''
#     return mu*X

def ds_dt(mu, Yps, Yxs, rp, ms, X):
    ''''''

    return -(mu/Yxs+rp/Yps + ms)*X

def dp_dt(rp, X):
    ''''''
    return rp*X
# ode model solutions





#how to optimize parameter

if __name__ == "__main__":
    bacteria = Bacteria(s=5, umax=7, ks=2, ki=3, model_type='monod')
    bacteria.residual()
    bacteria.set_parameters()
    bacteria.plot()


    print(bacteria.final)
    print(bacteria.report)


