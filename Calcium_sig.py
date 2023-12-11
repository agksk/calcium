# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
import numpy as np
import pandas as pd
from scipy.integrate import simps
from numpy import trapz
from numpy import mean
import statistics
from matplotlib import pyplot as plt


# %%
get_ipython().run_line_magic('config', "InlineBackend.print_figure_kwargs =     {'bbox_inches':None}")


# %%
df = pd.read_csv(r'c:\Users\kinga\Desktop\input\1 Nrf-2 WT ACh 50_nM_10_uM.txt', index_col = None, header=0, sep='\\t')
df


# %%
#sorting and background subtraction
def FindSubtrBg(df):
    df = df.sort_values(by=[0], axis=1, ascending=True)
     
    for column in df.iloc[:, 3:-1]:
        df[column] = df[column] - df.iloc[:, 2]
    print(df)   
    return (df) #returning data from function

df=FindSubtrBg(df) #modyfying original dataframe
print(df)


# %%
def NormalData(DataFrame):  #data normalization 
    NormalMatrix=[]
    for column in DataFrame.iloc[:, 2:]:
        factor=mean(DataFrame[column][0:10])
        NormalMatrix.append(factor)

        DataFrame[column]=DataFrame[column]/mean(DataFrame[column][0:10])
    print(DataFrame)
    
    return(DataFrame)

df=NormalData(df)
# Average and SEM calculation
col = df.iloc[: , 2:10]
av_row = col.mean(axis=1)
df['av'] = av_row

sem_row = col.sem(axis=1)
df['SEM'] = sem_row


print(av_row)
print(sem_row)


# %%
fig = plt.figure(figsize=(9, 5), dpi=100)   # graph with average calcium trace +/- SEM.

ax = fig.add_axes( [.15, .1, .8, .8] )

X = df['Time [s]']
Y = df['av']
yerr = df['SEM']


ax.fill_between(
    
    X, Y - yerr, Y + yerr,
    
    linewidth = 1.5,
    facecolor = 'salmon',
    edgecolor = 'red',      
    
    alpha = 0.25    
)
ax.plot(
    X, Y,
    linestyle       = '-',      
    color           = 'darkred',
    linewidth       = 1.0,
)
ax.set_title('Calcium traces')
ax.set_xlabel('Time [s]')
ax.set_ylabel('Fluo-4, F/F\u2080')

fig.savefig('c:\\Users\\kinga\\Downloads\\output/calcium_trace.png', dpi=300, transparent=False)


# %%
# function calculating the area from each column except from 0-2(timestep, time and background after ascending sorting)  
print("What time range do you want to analyze? Put start and stop point in seconds to continue")
startpoint = int(input("Enter your startpoint [s]:"))
endpoint = int(input("Enter your endpoint [s]:"))
time=endpoint-startpoint
print("\nArea from %s seconds will be calculated\n" % (time))


def FindArea(DataFrame):
    AreaMatrix=[]
    for column in DataFrame.iloc[:, 3:]:
        area = np.trapz(list(DataFrame[column][startpoint:endpoint]), dx=2)
        AreaMatrix.append(round(area-time,3))
    #print(AreaMatrix)
    AreaAverage = mean(AreaMatrix)
    AreaSEM = (statistics.stdev(AreaMatrix))/len(AreaMatrix)
    
    print("Average response in your experiment in give timeframe is: %s \u00B1 %s. Cell number = %s" %(AreaAverage, round(AreaSEM,3),len(AreaMatrix)))
    #print(AreaAverage)
    #print(len(AreaMatrix))
    #print(AreaSEM)
    
        
            
FindArea(df)


# %%
col = df.iloc[: , 2:10]
fig = plt.figure(figsize=(9, 5), dpi=100)   # graph with separate calcium traces.

ax = fig.add_axes( [.15, .1, .8, .8] )

X = df['Time [s]']
Y = col

ax.plot(
    X, Y,
    linestyle       = '-',      
    color           = None,
    linewidth       = 1.0,
)
ax.set_title('Calcium traces')
ax.set_xlabel('Time [s]')
ax.set_ylabel('Fluo-4, F/F\u2080')

fig.savefig('c:\\Users\\kinga\\Downloads\\output/calcium_trace_sep.png', dpi=300, transparent=False)


# %%



