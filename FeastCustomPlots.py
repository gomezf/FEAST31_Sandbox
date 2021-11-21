# Custom plotting functions for FEAST
# Plots results as time series with uncertainty
#
# FGomez
#

import numpy as np
import matplotlib.pyplot as plt
import copy
import feast

def TimeSeriesUncertainty(ResultsDirectory):
    ra = feast.ResultsProcessing.results_analysis_functions.results_analysis
    npv, em_timeseries, programs = ra(ResultsDirectory, gas_price=0, discount_rate=0)

    #calculating average and std per program
    avg_emissions=np.zeros((em_timeseries.shape[0],em_timeseries.shape[1]))
    std_emissions = copy.deepcopy(avg_emissions)

    for progs in range(0, len(programs)):
        avg_emissions[progs] = np.mean(em_timeseries[progs],axis=1)
        std_emissions[progs] = np.std(em_timeseries[progs],axis=1)

    avgn_emissions = copy.deepcopy(avg_emissions)
    stdn_emissions = copy.deepcopy(avg_emissions)
    for progs in range(0, len(programs)):
        avgn_emissions[progs] = np.divide(avg_emissions[progs],avg_emissions[2,0])
        stdn_emissions[progs] = np.divide(std_emissions[progs],avg_emissions[2,0])

    import seaborn as sns
    fig, ax = plt.subplots()
    #clrs = sns.color_palette("husl", 5)
    epochs = list(range(0,len(avg_emissions[0])))
    with sns.axes_style("darkgrid"):
        for avg,std,progs in zip(avgn_emissions,stdn_emissions,programs):
            ax.plot(epochs,avg,label=progs)
            ax.fill_between(epochs,avg-std, avg+std,alpha=0.3)
        ax.legend()
        ax.grid()

    fig, ax = plt.subplots()
    epochs = list(range(0,len(avg_emissions[0])))
    with sns.axes_style("darkgrid"):
        for avg,std,progs in zip(avg_emissions,std_emissions,programs):
            ax.plot(epochs,avg,label=progs)
            ax.fill_between(epochs,avg-std, avg+std,alpha=0.3)
        ax.legend()
        ax.grid()