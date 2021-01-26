


def dx_dt(mu, Cx, kd):
    ''''''
    rx= mu*Cx 
    rd= kd*Cx

    return rx- rd

def ds_dt(mu, Cx, Yxp, Yps, rms):
    ''''''
    rs= mu*Cx/Yxp + mu*Cx/Yps + rms

    return -(rs)

def dp_dt(alpha, mu, Cx, beta, kdp, Cp):
    '''Batch configuration for product formation.add
    alpha= a growth associated parameter
    beta= a non-growth associated parameter
    mu = cell growth rate variable
    Cx= cell concentration
    kdp= 
    Cp= concentration of product '''

    rp = (alpha*mu*Cx) + (beta*Cx)
    rdp = kdp * Cp
    return rp - rdp


    model_dict = {
        dx_dt(mu, Cx, kd): mu*Cx - kd*Cx,
        ds_dt(mu, Cx, Yxp, Yps, rms): -(mu*Cx/Yxp + mu*Cx/Yps + rms),
        dp_dt(alpha, mu, Cx, beta, kdp, Cp): (alpha*mu*Cx) + (beta*Cx) - (kdp * Cp),
    }

    mu, Cx, Yxp, Yps, rms, Cp  = variables('mu, Cx, Yxp, Yps, rms, Cp')
    kd = Parameter('kd', 0.1)
    alpha = Parameter('alpha', 0.1)
    beta = Parameter('beta', 0.1)
    kdp = Parameter('kdp, 0.1')


