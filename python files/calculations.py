import numpy as np

def productivity(df, product_column, time_column):
    final_time=df[time_column].max()
    final_amount=df[df[time_column]== final_time][product_column].to_numpy()[0]
    productivity = final_amount/final_time

    return productivity

def yieldx(df, product_column, substrate_column):
    final_substrate=df[substrate_column].max()
    initial_substrate= df[substrate_column].min()
    final_amount=df[df[substrate_column]== final_substrate][product_column].to_numpy()[0]
    yieldx = final_amount/(final_substrate-initial_substrate)

    return yieldx

