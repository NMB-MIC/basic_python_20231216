import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm



def process_capability(data):
    """calculate process capability 
    then return fig and some param """

    # Set specification limits
    target = 5
    LSL = 3
    USL = 7

    # Calculate Cp
    cp = (USL-LSL)/(6*np.std(data))

    # Calculate Cpk
    cpk = min((USL-data.mean())/(3*data.std()), (data.mean()-LSL)/(3*data.std()))

    # Calculate z-value
    z = min((USL-data.mean())/(data.std()), (data.mean()-LSL)/(data.std()))

    # Get data summary statistics
    num_samples = len(data)
    sample_mean = data.mean()
    sample_std = data.std()
    sample_max = data.max()
    sample_min = data.min()
    sample_median = np.median(data)

    # Get percentage of data points outside of specification limits
    pct_below_LSL = len(data[data < LSL])/len(data)*100
    pct_above_USL = len(data[data > USL])/len(data)*100

    if cp < 1.33:
        cp_result = 'NG'
        cp_color = 'red'
    else:
        cp_result = 'OK'
        cp_color = 'green'

    if cpk < 1.33:
        cpk_result = 'NG'
        cpk_color = 'red'
    else:
        cpk_result = 'OK'
        cpk_color = 'green'


    if cpk_result == 'NG' or cp_result == 'NG':
        total_result = 'NG'
        total_result_color = 'red'
    else:
        total_result = 'OK'
        total_result_color = 'green'

    # Generate probability density function 
    x = np.linspace(min(data), max(data), 1000)
    y = norm.pdf(x, loc=5, scale=1)  
    
    # Plot histogram for data along with probability density functions and specification limits
    fig = plt.figure(figsize=(15,10))
    plt.hist(data, color="lightgrey", edgecolor="black", density=True)
    sns.kdeplot(data, color="blue", label="Density ST")
    plt.plot(x, y, linestyle="--", color="black", label="Theorethical Density ST")
    plt.axvline(LSL, linestyle="--", color="red", label="LSL")
    plt.axvline(USL, linestyle="--", color="orange", label="USL")
    plt.axvline(target, linestyle="--", color="green", label="Target")
    plt.title('Process Capability Analysis')
    plt.xlabel("Measure")
    plt.ylabel("")
    plt.yticks([])
  
    #plt.axis([min(x)-1, max(x)+1,0, max(y)+0.1]) #min max axis and min max y axis
    plt.legend(loc='upper left')
    plt.text(max(x), max(y), f'RESULT: {total_result}',color=total_result_color, fontsize=20,weight="heavy")
    plt.text(max(x), max(y)-0.02, f'cp: {round(cpk,2)}',color=cpk_color, fontsize=18)
    plt.text(max(x), max(y)-0.04, f'cpk: {round(cpk,2)}',color=cpk_color, fontsize=18)
    #plt.savefig("export/process_capability.png")
    #plt.show()
    return fig