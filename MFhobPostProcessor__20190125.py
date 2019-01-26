"""        QuickGrapher V1.1
        Started on 3/3/2017
        Last Updated 1/26/2019

@author(s): Hugo Perea and Justin Clark

This Python script compare observed and Simulated Target Head
for each stress period. Also, it computes some R^2, Mean Residual, 
and Mea Relative Error.
Instruction:
1. Populate the excel file with your HOB package file 
   and head results from a model run.
2. Change the fin and fpath in this script.

This script was tailored for Pinal. Stress period numbers are in an array.

Approximate Run Time = 10 seconds 
"""
import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib as cplt
from scipy import stats
import seaborn as sns


def import_Excel_wrk(xlsx_in,worksheet):
    #Open Excel file
    xlsx = pd.ExcelFile(xlsx_in)    
    df = xlsx.parse(worksheet)    
    x = np.array(np.rec.fromrecords(df.values))
    
    x=np.reshape(x,(df.SP,df.hobs,df.hsim))

def Histogram(obs,sim,nBins,txt):
    hRes=(obs-sim)
    mu=np.mean(hRes)
    sigma=np.std(hRes)

    y_txt=txt+"\nMean = "+str(round(mu,1))+"\n"+"STdev = "+str(round(sigma,1))+"\n"+str(time.strftime("%m/%d/%Y"))
    # Add the 'Best fit' line
    plt.figure(figsize=(8,8))
    count, bins, ignored = plt.hist(hRes,nBins,normed=1,
                                    facecolor='blue',alpha=0.5,histtype='bar',
                                    rwidth=0.9)
    h=mlab.normpdf(bins,mu,sigma)
    
    plt.plot(bins,h,'r--')
    plt.xlabel('RESIDUALS')
    plt.ylabel('PROBABILITY')
    plt.grid(True,linestyle="--")
    plt.axis((-250,250,0.0,count.max()*1.1))
    plt.title(y_txt)
    
    plt.subplots_adjust(left=0.15)
    plt.show()    
    
        
if __name__ == '__main__':
    fin='SRV_1900-15_HOB.xlsx'
    
    fpath=os.path.join('J:\HYDRO\pythonShare\Programs\HugoPerea\HobPost')
    filename=os.path.join(fpath,fin)
   
    xlsx = pd.ExcelFile(filename)    
    # Create a dataframe
    df = xlsx.parse('HOB_DB')  
    df=df.dropna(axis=1,how='all')
    df=df.loc[(df.hsim>500) & (df.hobs>0)]


    SPdf=xlsx.parse('SP_defn')
    
    nSPdf=SPdf.PHX_HASS_SP.unique()
    
    Period=[[i,min(SPdf[SPdf.PHX_HASS_SP==i].Year),max(SPdf[SPdf.PHX_HASS_SP==i].Year)] for i in nSPdf ]
    
    Cnames=['SP','Year1','Year2']
    SP1=pd.DataFrame.from_records(Period,columns=Cnames,index='SP')   
    
    #join two dataframes 
    dfR=df.join(SP1,on='SP')

    colors=['red','cyan','yellow']
    label=['1','2','3']

    for i in nSPdf:
        x=dfR[dfR.SP==i].hobs
        y=dfR[dfR.SP==i].hsim
        cl=dfR[dfR.SP==i].Layer
        df1 = pd.DataFrame([dfR[dfR.SP==i].hobs, dfR[dfR.SP==i].hsim])
        df2 = np.transpose(df1)
        print(i)
        if x.count()>10:
            sns.lmplot(x='hobs' , y='hsim', data=df2)
    Histogram(dfR.hobs,dfR.hsim,100,'PHX-HASS Head Residuals')