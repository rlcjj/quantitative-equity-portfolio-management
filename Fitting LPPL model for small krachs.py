
#Coding LPPL model and fitting CAC40 campanies stocks data

# In[373]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.optimize
from datetime import datetime



# Goals:
# 
# 1) Fit the data to the stock price of a CAC40 company
# 2) Check for coherence with the results of the paper

# In[374]:

Path_to_file = "/Users/monmac/Desktop/Crash/scripts/data/AC.PA.csv"
data1 = pd.read_csv(Path_to_file)
data = data1.reindex(index=data1.index[::-1])


# In[375]:
#we look for the best intervals to fit

print(data.head(1))

print(data1.head(1))

#Checking the global tendency of the stock
plt.plot(range(len(data)),data["Open"])
plt.show()

#%%

#creating the volatility list (high-low)/(open+close)
class Open_csv:
    def __init__(self):
        pass
        
    def open(self,path_to_file):
        data = np.asarray(pd.read_csv(path_to_file, delimiter=",").values)
        return data

open_csv = Open_csv()
# open high low close

def f(vector):
    return (vector[2]-vector[3])/(vector[1]+vector[4])
    
def compute_function_returns(function, data):
    returns = []
    for i in range(len(data)):
        returns.append(function(data[i]))
    return np.asarray(returns)

#%%
#check the maximum vol
vol = compute_function_returns(f,data)

plt.plot(range(len(vol)),vol)
plt.show()

#%%
#Check on the highs
high = []
for i in range(len(data)):
    high.append(data[i,2])
    
plt.plot(range(150), high[750:900])
plt.show
    
#%%
#Check the potential intervals
intervale_valide = []
for i in range(len(vol)):
    vol_lim = max(vol)*0.75
    if vol[i] > vol_lim :
        intervalle_valide.append(i)
    else :
        intervalle_valide.append(0)

plt.plot(range(len(vol)),intervalle_valide)
plt.show()


# In[388]:


#
t_start = "2014-09-01"
t_end = "2015-06-01"

data["Date"] = pd.to_datetime(data["Date"])
mask = (data['Date'] > t_start) & (data['Date'] <= t_end)
data_new = data.loc[mask]
print(len(data_new))
#data_new.head(5)

data_array = data_new["Open"].values
date_array = data_new["Date"].values

plt.figure(figsize=(10,8))
plt.plot(date_array,data_array)
plt.gca().xaxis_date()
plt.show()


# In[389]:


#rescaling of data
t = np.linspace(0,1,len(date_array))
new_data = (data_array-np.min(data_array))/(np.max(data_array)-np.min(data_array))


# In[390]:


#Optimization with scipy curve_fit
#nonlinear function to be optimised
def func_fit(t,A,B,C,w,tc,z,phi):
    return A+B*(tc-t)**z+C*np.cos(w*np.log(tc-t)+phi)

popt,pcov = scipy.optimize.curve_fit(func_fit, t, new_data,[1,-1,0.1,12,1.1,0.5,np.pi],bounds=([0,-100,-100,0,1.001,0,0], 
                                                                    [100,0,100,50,2, 1, 2*np.pi]))

plt.figure(figsize=(10,8))
plt.plot(t,new_data)
plt.plot(t,func_fit(t, *popt),'r-',
  label='fit: a=%5.3f, b=%5.3f, c=%5.3f, w=%5.3f, tc=%5.3f, z=%5.3f, phi=%5.3f' % tuple(popt))
plt.show()


residuals = new_data- func_fit(t, *popt)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((new_data-np.mean(new_data))**2)
r_squared = 1 - (ss_res / ss_tot)
print(r_squared)
print("popt=",popt)
print("tc=",popt[4])
