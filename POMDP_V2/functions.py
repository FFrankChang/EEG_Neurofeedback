#!/usr/bin/env python
# encoding: utf-8

"""
Created by Lola Beerendonk 2022.
"""

from __future__ import division

import os, sys, datetime, pickle
import subprocess, logging, time

import numpy as np
import numpy
import numpy.random as random
import pandas as pd
import scipy as sp
import scipy.stats as stats
# import bottleneck as bn
# import sympy
import math
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from matplotlib.ticker import MultipleLocator
import matplotlib.patches as patches
import seaborn as sns
from sklearn import preprocessing
from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.patches as mpatches
import statsmodels.api as sm
import statsmodels.formula.api as SM
from statsmodels.stats.anova import AnovaRM
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
#import mne
# import hddm
# import kabuki
# import pypsignifit as psi
from itertools import combinations as comb

from collections import OrderedDict
from time import time
from scipy.optimize import fmin_powell
from scipy import integrate
#import pymc3 as pm
#import theano as thno 
#import theano.tensor as T

from IPython import embed as shell

def rm_anova(df, dv, within):
    aovrm = AnovaRM(df, dv, 'sub_ID', within=within, aggregate_func='mean')
    res = aovrm.fit()
    print(res)
    return np.array(res.anova_table)

def makebins(df_complete, number_of_bins):

    meta_all = []
    sdt_all = []

    for exp in np.unique(df_complete['exp']):

        meta = df_complete[(df_complete.exp==exp)].copy()
        meta['baseline_split'] = np.nan
        meta['base_trial_reg'] = np.nan

        # make bins per run (here called miniblock)
        for subj in np.unique(meta.sub_ID):
            for s in np.unique(meta.session[meta.sub_ID == subj]):
                    for m in np.unique(meta.miniblock[(meta.sub_ID ==subj)&(meta.session==s)]):

                        ind = (meta.sub_ID == subj) & (meta.session == s) & (meta.miniblock == m) 

                        trial_nr = np.array(meta['trial_nr'][ind])  

                        if len(meta[ind]) < 50: # Only miniblocks > 49 trials
                            continue

                        #binning: equally populated bins
                        meta.loc[ind,'baseline_split'] = np.array(pd.qcut(meta[ind]['raw_baseline'],number_of_bins,labels = np.arange(0,number_of_bins,1)))

                        metam = meta[ind].copy()
                        # print(metam)
                        if exp[0] == 'S':
                            metam['modality'] = 'vis'
                        else: 
                            metam['modality'] = 'aud'

                        meta_all.append(metam)

                        # compute hits/fas for all bins
                        sdt = pd.DataFrame(index=range(number_of_bins))

                        if exp == 'dis':
                            sdt['target'] = metam[metam['disc_stim']==1].groupby(['baseline_split'])['correct'].count()
                            sdt['notarget'] = metam[metam['disc_stim']==2].groupby(['baseline_split'])['correct'].count()
                        else:
                            sdt['target'] = metam[metam['signal_present']==1].groupby(['baseline_split'])['correct'].count()
                            sdt['notarget'] = metam[metam['signal_present']==0].groupby(['baseline_split'])['correct'].count()

                        sdt['hit'] = metam[metam['hit']==True].groupby(['baseline_split'])['correct'].count()
                        sdt['fa'] = metam[metam['fa']==True].groupby(['baseline_split'])['correct'].count()

                        sdt.reset_index(inplace=True)

                        sdt['baseline_split'] = np.arange(number_of_bins)
                        sdt['raw_baseline'] = np.array(metam.groupby(['baseline_split'])['raw_baseline'].mean())

                        sdt = sdt.iloc[:number_of_bins]

                        # reinsert important columns into sdt dataframe
                        sdt['exp'] = exp
                        if exp[0] == 'S':
                            sdt['modality'] = 'vis'
                        else: 
                            sdt['modality'] = 'aud'
                        sdt['sub_ID'] = subj
                        sdt['session'] = s
                        sdt['miniblock'] = m
                        sdt['task'] = np.unique(metam['task'])[0]
                        sdt['drug'] = np.unique(metam['drug'])[0]


                        sdt_all.append(sdt)

    meta_all = pd.concat(meta_all)
    sdt_all = pd.concat(sdt_all) 

    raw_baseline = sdt_all.groupby(['sub_ID','task','modality','baseline_split','drug'])['raw_baseline'].mean().reset_index()
    sdt_all = sdt_all.groupby(['sub_ID','task','modality','baseline_split','drug'])[['target','notarget','hit','fa']].sum().reset_index()

    # compute d' and criterion from compiled hits/fas per subject per bin
    sdt_all[['target','notarget']] = sdt_all[['target','notarget']]+1
    sdt_all[['hit','fa']] = sdt_all[['hit','fa']]+.5
    sdt_all.loc[:,['target','notarget']].fillna(1,inplace=True)
    sdt_all.loc[:,['hit','fa']].fillna(.5,inplace=True)
    sdt_all['raw_baseline'] = raw_baseline['raw_baseline'].copy()

    sdt_all['hit_rate'] = sdt_all['hit'] / sdt_all['target']
    sdt_all['fa_rate'] = sdt_all['fa'] / sdt_all['notarget']

    sdt_all['hit_rate_z'] = stats.norm.isf(1-sdt_all['hit_rate'])
    sdt_all['fa_rate_z'] =  stats.norm.isf(1-sdt_all['fa_rate'])

    sdt_all['d'] = sdt_all['hit_rate_z'] - sdt_all['fa_rate_z']
    sdt_all['c'] = -(sdt_all['hit_rate_z'] + sdt_all['fa_rate_z']) / 2.0

    # group this dataframe over bins, so it contains mean RT for 5 bins per subject per task and modality
    meta_all = meta_all.groupby(['sub_ID','exp','task','modality','baseline_split','session','miniblock','drug'])[['raw_baseline','RT']].mean().groupby(['sub_ID','task','modality','baseline_split','session','exp','drug']).mean().groupby(['sub_ID','task','modality','baseline_split','exp','drug']).mean().groupby(['sub_ID','task','modality','baseline_split','drug' ]).mean().reset_index()

    return(meta_all, sdt_all)

def makebins_across_tasks(df_complete, number_of_bins):
    meta_all20 = []
    sdt_all20 = []

    for exp in np.unique(df_complete['exp']):

        meta = df_complete[(df_complete.exp==exp)&(~df_complete['raw_baseline'].isnull())].copy()
        meta['baseline_split'] = np.nan
        meta['base_trial_reg'] = np.nan

        for subj in np.unique(meta.sub_ID):
            for s in np.unique(meta.session[meta.sub_ID == subj]):
                    for m in np.unique(meta.miniblock[(meta.sub_ID ==subj)&(meta.session==s)]):

                        ind = (meta.sub_ID == subj) & (meta.session == s) & (meta.miniblock == m)
                        if len(meta[ind]) < 50: # Only miniblocks > 49 trials
                            continue

                        # meta.loc[ind,'baseline_split'] = np.array(pd.qcut(meta[ind]['ev_prev'],number_of_bins,labels = np.arange(0,number_of_bins,1)))
                        meta.loc[ind,'baseline_split'] = np.array(pd.qcut(meta[ind]['raw_baseline'],number_of_bins,labels = np.arange(0,number_of_bins,1)))


                        metam = meta[ind].copy()

                        if exp[0] == 'S':
                            metam['modality'] = 'vis'
                        else: 
                            metam['modality'] = 'aud'

                        meta_all20.append(metam)

                        sdt = pd.DataFrame(index=range(number_of_bins))

                        if exp == 'dis':
                            sdt['target'] = metam[metam['disc_stim']==1].groupby(['baseline_split'])['correct'].count()
                            sdt['notarget'] = metam[metam['disc_stim']==2].groupby(['baseline_split'])['correct'].count()
                        else:
                            sdt['target'] = metam[metam['signal_present']==1].groupby(['baseline_split'])['correct'].count()
                            sdt['notarget'] = metam[metam['signal_present']==0].groupby(['baseline_split'])['correct'].count()
                        # sdt.fillna(1, inplace=True)

                        sdt['hit'] = metam[metam['hit']==True].groupby(['baseline_split'])['correct'].count()
                        sdt['fa'] = metam[metam['fa']==True].groupby(['baseline_split'])['correct'].count()
                        # sdt.fillna(0.5, inplace=True)

                        sdt.reset_index(inplace=True)

                        sdt['baseline_split'] = np.arange(number_of_bins)
                        sdt['raw_baseline'] = np.array(metam.groupby(['baseline_split'])['raw_baseline'].mean())
                        # sdt['ev_prev'] = np.array(metam.groupby(['baseline_split'])['ev_prev'].mean())


                        sdt = sdt.iloc[:number_of_bins]

                        sdt['exp'] = exp
                        if exp[0] == 'S':
                            sdt['modality'] = 'vis'
                        else: 
                            sdt['modality'] = 'aud'
                        sdt['sub_ID'] = subj
                        sdt['session'] = s
                        sdt['miniblock'] = m
                        sdt['task'] = np.unique(metam['task'])[0]
                        sdt['drug'] = np.unique(metam['drug'])[0]


                        sdt_all20.append(sdt)

    meta_all20 = pd.concat(meta_all20)
    sdt_all20 = pd.concat(sdt_all20) 

    raw_baseline20 = sdt_all20.groupby(['sub_ID','exp','baseline_split','drug'])['raw_baseline'].mean().reset_index()
    sdt_all20 = sdt_all20.groupby(['sub_ID','exp','baseline_split','drug'])[['target','notarget','hit','fa']].sum().reset_index()
    sdt_all20[['target','notarget']] = sdt_all20[['target','notarget']]+1
    sdt_all20[['hit','fa']] = sdt_all20[['hit','fa']]+.5
    sdt_all20.loc[:,['target','notarget']].fillna(1,inplace=True)
    sdt_all20.loc[:,['hit','fa']].fillna(.5,inplace=True)
    sdt_all20['raw_baseline'] = raw_baseline20['raw_baseline'].copy()

    sdt_all20['hit_rate'] = sdt_all20['hit'] / sdt_all20['target']
    sdt_all20['fa_rate'] = sdt_all20['fa'] / sdt_all20['notarget']

    sdt_all20['hit_rate_z'] = stats.norm.isf(1-sdt_all20['hit_rate'])
    sdt_all20['fa_rate_z'] =  stats.norm.isf(1-sdt_all20['fa_rate'])

    sdt_all20['d'] = sdt_all20['hit_rate_z'] - sdt_all20['fa_rate_z']
    sdt_all20['c'] = -(sdt_all20['hit_rate_z'] + sdt_all20['fa_rate_z']) / 2.0

    meta_all20 = meta_all20.groupby(['sub_ID','exp','baseline_split','session','miniblock','drug'])[['raw_baseline','RT']].mean().groupby(['sub_ID','baseline_split','session','exp','drug']).mean().groupby(['sub_ID','baseline_split','exp','drug']).mean().groupby(['sub_ID','baseline_split','drug']).mean().reset_index()


    return(meta_all20, sdt_all20)

def makebins_regress(df_complete, number_of_bins, to_regress_out):

    meta_all_reg = []
    sdt_all_reg = []

    for exp in np.unique(df_complete['exp']):

        meta = df_complete[(df_complete.exp==exp)&(~df_complete['raw_baseline'].isnull())].copy()
        meta = df_complete[(df_complete.exp==exp)&(~df_complete['abs_baseline'].isnull())].copy()
        meta['baseline_split'] = np.nan
        meta['base_trial_reg'] = np.nan

        for subj in np.unique(meta.sub_ID):
            for s in np.unique(meta.session[meta.sub_ID == subj]):
                    for m in np.unique(meta.miniblock[(meta.sub_ID ==subj)&(meta.session==s)]):

                        ind = (meta.sub_ID == subj) & (meta.session == s) & (meta.miniblock == m) 

                        if to_regress_out == 'trial_nr':
                            reg_var = np.array(meta['trial_nr'][ind])  
                        elif to_regress_out == 'ev_prev':
                            reg_var = np.array(meta['ev_prev'][ind])  

                        thismeta = meta[ind].copy()

                        # regress out 
                        reg_out = []
                        reg_out = functions.lin_regress_resid(np.array(thismeta['raw_baseline']), [reg_var]) + np.array(thismeta['raw_baseline'].mean())

                        thismeta['raw_baseline'] = reg_out

                        thismeta['baseline_split'] = pd.qcut(thismeta['raw_baseline'], number_of_bins, labels = np.arange(0,number_of_bins,1))

                        metam = thismeta.copy()
                        if exp[0] == 'S':
                            metam['modality'] = 'vis'
                        else: 
                            metam['modality'] = 'aud'

                        meta_all_reg.append(metam)

                        sdt = pd.DataFrame(index=range(number_of_bins))

                        if exp == 'dis':
                            sdt['target'] = metam[metam['disc_stim']==1].groupby(['baseline_split'])['correct'].count()
                            sdt['notarget'] = metam[metam['disc_stim']==2].groupby(['baseline_split'])['correct'].count()
                        else:
                            sdt['target'] = metam[metam['signal_present']==1].groupby(['baseline_split'])['correct'].count()
                            sdt['notarget'] = metam[metam['signal_present']==0].groupby(['baseline_split'])['correct'].count()

                        sdt['hit'] = metam[metam['hit']==True].groupby(['baseline_split'])['correct'].count()
                        sdt['fa'] = metam[metam['fa']==True].groupby(['baseline_split'])['correct'].count()

                        sdt.reset_index(inplace=True)

                        sdt['baseline_split'] = np.arange(number_of_bins)
                        sdt['raw_baseline'] = np.array(metam.groupby(['baseline_split'])['raw_baseline'].mean())

                        sdt = sdt.iloc[:number_of_bins]

                        sdt['exp'] = exp
                        if exp[0] == 'S':
                            sdt['modality'] = 'vis'
                        else: 
                            sdt['modality'] = 'aud'
                        sdt['sub_ID'] = subj
                        sdt['session'] = s
                        sdt['miniblock'] = m
                        sdt['task'] = np.unique(metam['task'])[0]

                        sdt_all_reg.append(sdt)

    meta_all_reg = pd.concat(meta_all_reg)
    sdt_all_reg = pd.concat(sdt_all_reg) 

    raw_baseline = sdt_all_reg.groupby(['sub_ID','task','modality','baseline_split','drug'])['raw_baseline'].mean().reset_index()
    sdt_all_reg = sdt_all_reg.groupby(['sub_ID','task','modality','baseline_split','drug'])[['target','notarget','hit','fa']].sum().reset_index()
    sdt_all_reg[['target','notarget']] = sdt_all_reg[['target','notarget']]+1
    sdt_all_reg[['hit','fa']] = sdt_all_reg[['hit','fa']]+.5
    sdt_all_reg.loc[:,['target','notarget']].fillna(1,inplace=True)
    sdt_all_reg.loc[:,['hit','fa']].fillna(.5,inplace=True)
    sdt_all_reg['raw_baseline'] = raw_baseline['raw_baseline'].copy()

    sdt_all_reg['hit_rate'] = sdt_all_reg['hit'] / sdt_all_reg['target']
    sdt_all_reg['fa_rate'] = sdt_all_reg['fa'] / sdt_all_reg['notarget']

    sdt_all_reg['hit_rate_z'] = stats.norm.isf(1-sdt_all_reg['hit_rate'])
    sdt_all_reg['fa_rate_z'] =  stats.norm.isf(1-sdt_all_reg['fa_rate'])

    sdt_all_reg['d'] = sdt_all_reg['hit_rate_z'] - sdt_all_reg['fa_rate_z']
    sdt_all_reg['c'] = -(sdt_all_reg['hit_rate_z'] + sdt_all_reg['fa_rate_z']) / 2.0

    meta_all_reg = meta_all_reg.groupby(['sub_ID','exp','task','modality','baseline_split','session','miniblock','drug'])[['raw_baseline','RT']].mean().groupby(['sub_ID','task','modality','baseline_split','session','exp']).mean().groupby(['sub_ID','task','modality','baseline_split','exp']).mean().groupby(['sub_ID','task','modality','baseline_split']).mean().reset_index()

    return(meta_all_reg, sdt_all_reg)


def makebins_across_tasks_ev_prev(df_complete, number_of_bins):
    meta_all20 = []
    sdt_all20 = []

    for exp in np.unique(df_complete['exp']):

        meta = df_complete[(df_complete.exp==exp)&(~df_complete['raw_baseline'].isnull())].copy()
        meta['baseline_split'] = np.nan
        meta['base_trial_reg'] = np.nan

        for subj in np.unique(meta.sub_ID):
            for s in np.unique(meta.session[meta.sub_ID == subj]):
                    for m in np.unique(meta.miniblock[(meta.sub_ID ==subj)&(meta.session==s)]):

                        ind = (meta.sub_ID == subj) & (meta.session == s) & (meta.miniblock == m)
                        if len(meta[ind]) < 50: # Only miniblocks > 49 trials
                            continue

                        # meta.loc[ind,'baseline_split'] = np.array(pd.qcut(meta[ind]['ev_prev'],number_of_bins,labels = np.arange(0,number_of_bins,1)))
                        meta.loc[ind,'baseline_split'] = np.array(pd.qcut(meta[ind]['ev_prev'],number_of_bins,labels = np.arange(0,number_of_bins,1)))


                        metam = meta[ind].copy()

                        if exp[0] == 'S':
                            metam['modality'] = 'vis'
                        else: 
                            metam['modality'] = 'aud'

                        meta_all20.append(metam)

                        sdt = pd.DataFrame(index=range(number_of_bins))

                        if exp == 'dis':
                            sdt['target'] = metam[metam['disc_stim']==1].groupby(['baseline_split'])['correct'].count()
                            sdt['notarget'] = metam[metam['disc_stim']==2].groupby(['baseline_split'])['correct'].count()
                        else:
                            sdt['target'] = metam[metam['signal_present']==1].groupby(['baseline_split'])['correct'].count()
                            sdt['notarget'] = metam[metam['signal_present']==0].groupby(['baseline_split'])['correct'].count()

                        sdt['hit'] = metam[metam['hit']==True].groupby(['baseline_split'])['correct'].count()
                        sdt['fa'] = metam[metam['fa']==True].groupby(['baseline_split'])['correct'].count()
                        sdt.reset_index(inplace=True)

                        sdt['baseline_split'] = np.arange(number_of_bins)
                        sdt['ev_prev'] = np.array(metam.groupby(['baseline_split'])['ev_prev'].mean())

                        sdt = sdt.iloc[:number_of_bins]

                        sdt['exp'] = exp
                        if exp[0] == 'S':
                            sdt['modality'] = 'vis'
                        else: 
                            sdt['modality'] = 'aud'
                        sdt['sub_ID'] = subj
                        sdt['session'] = s
                        sdt['miniblock'] = m
                        sdt['task'] = np.unique(metam['task'])[0]

                        sdt_all20.append(sdt)

    meta_all20 = pd.concat(meta_all20)
    sdt_all20 = pd.concat(sdt_all20) 

    raw_baseline20 = sdt_all20.groupby(['sub_ID','exp','baseline_split'])['ev_prev'].mean().reset_index()
    sdt_all20 = sdt_all20.groupby(['sub_ID','exp','baseline_split'])[['target','notarget','hit','fa']].sum().reset_index()
    sdt_all20[['target','notarget']] = sdt_all20[['target','notarget']]+1
    sdt_all20[['hit','fa']] = sdt_all20[['hit','fa']]+.5
    sdt_all20.loc[:,['target','notarget']].fillna(1,inplace=True)
    sdt_all20.loc[:,['hit','fa']].fillna(.5,inplace=True)
    sdt_all20['ev_prev'] = raw_baseline20['ev_prev'].copy()

    sdt_all20['hit_rate'] = sdt_all20['hit'] / sdt_all20['target']
    sdt_all20['fa_rate'] = sdt_all20['fa'] / sdt_all20['notarget']

    sdt_all20['hit_rate_z'] = stats.norm.isf(1-sdt_all20['hit_rate'])
    sdt_all20['fa_rate_z'] =  stats.norm.isf(1-sdt_all20['fa_rate'])

    sdt_all20['d'] = sdt_all20['hit_rate_z'] - sdt_all20['fa_rate_z']
    sdt_all20['c'] = -(sdt_all20['hit_rate_z'] + sdt_all20['fa_rate_z']) / 2.0

    meta_all20 = meta_all20.groupby(['sub_ID','exp','baseline_split','session','miniblock'])[['ev_prev','RT']].mean().groupby(['sub_ID','baseline_split','session','exp']).mean().groupby(['sub_ID','baseline_split','exp']).mean().groupby(['sub_ID','baseline_split']).mean().reset_index()

    return(meta_all20, sdt_all20)


def binned_plot_means(datain, datain20, number_of_bins, var, ylab, this_dir):
    from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)

    color = 'darkgreen'
    cm = 1/2.54  # centimeters in inches

    gs_kw = dict(wspace=.65, left=.08, right=.99, hspace=.25, top=.92, bottom=.15) 
    fig, axs = plt.subplots(nrows=2, ncols=5, sharex=True, figsize=(19*cm,8*cm))

    for thisdata, thisdata20, thisvar, thisylab in zip(datain, datain20, var, ylab):
        print(thisvar)

        if thisvar == 'd':
            row = 0
        elif thisvar == 'RT':
            row = 1

        column = 0

        num_bin = number_of_bins[1]

        data = pd.DataFrame(thisdata20.groupby(['sub_ID','baseline_split'])[[thisvar,'raw_baseline']].mean()).reset_index()

        # shell(color="neutral")
        data['errbar'] = np.nan
        for s in np.unique(data.sub_ID):
            submean = data.loc[(data.sub_ID==s),thisvar].mean()
            data.loc[(data.sub_ID==s),'errbar'] = data.loc[(data.sub_ID==s),thisvar] - submean

        betadf = pd.DataFrame(columns=['sub_ID','intfirst','first','intsecond','second1','second2'])
        betadferr = pd.DataFrame(columns=['sub_ID','intfirst','first','intsecond','second1','second2'])

        meanval = data.groupby('baseline_split')['raw_baseline'].mean()[2]
        # print(len(np.unique(data.sub_ID)))
        for s in np.unique(data.sub_ID):
            subdata = data[(data.sub_ID==s)].copy()

            difference = subdata['raw_baseline'].iloc[2] - meanval
            subdata['raw_baseline_c'] = subdata['raw_baseline'] - difference

            x = np.array(subdata['raw_baseline_c'][(subdata.sub_ID==s)]).reshape(-1,1)
            y = np.array(subdata[thisvar][(subdata.sub_ID==s)]).reshape(-1,1)

            poly_feat = PolynomialFeatures(degree=1)
            xp = poly_feat.fit_transform(x)
            xpred = np.linspace(x[0]-100,x[num_bin-1]+100,(num_bin+1)*100)
            model = sm.OLS(y, xp).fit()
            b = np.ones((num_bin+1)*100)
            ypred = np.column_stack((b,xpred))
            intfirst = model.params[0]
            first = model.params[1]
            
            poly_feat = PolynomialFeatures(degree=2)
            xp = poly_feat.fit_transform(x)
            model = sm.OLS(y, xp).fit()
            b = np.ones((num_bin+1)*100)
            c = xpred*xpred
            ypred = np.column_stack((b,xpred,c))
            intsecond = model.params[0]
            second1 = model.params[1]
            second2 = model.params[2]

            betadf = pd.concat([betadf, pd.DataFrame.from_records([{'sub_ID':s, 'intfirst': intfirst, 'first':first,  'intsecond':intsecond, 'second1':second1, 'second2':second2}])],ignore_index=True)

            # for errorbars
            y = np.array(subdata['errbar'][(subdata.sub_ID==s)]).reshape(-1,1)

            poly_feat = PolynomialFeatures(degree=1)
            xp = poly_feat.fit_transform(x)
            xpred = np.linspace(x[0]-100,x[num_bin-1]+100,(num_bin+1)*100)
            model = sm.OLS(y, xp).fit()
            b = np.ones((num_bin+1)*100)
            ypred = np.column_stack((b,xpred))
            intfirst = model.params[0]
            first = model.params[1]
            
            poly_feat = PolynomialFeatures(degree=2)
            xp = poly_feat.fit_transform(x)
            model = sm.OLS(y, xp).fit()
            b = np.ones((num_bin+1)*100)
            c = xpred*xpred
            ypred = np.column_stack((b,xpred,c))
            intsecond = model.params[0]
            second1 = model.params[1]
            second2 = model.params[2]

            betadferr = pd.concat([betadferr, pd.DataFrame.from_records([{'sub_ID':s, 'intfirst': intfirst, 'first':first,  'intsecond':intsecond, 'second1':second1, 'second2':second2}])],ignore_index=True)

        xpred = data.groupby(['baseline_split'])['raw_baseline'].mean()
        # xpred = data.groupby(['exp','session','miniblock','sub_ID','baseline_split'])['raw_baseline'].mean().groupby(['exp','sub_ID','baseline_split','session']).mean().groupby(['exp','baseline_split']).mean().groupby('baseline_split').mean().reset_index()
        xplot = np.linspace(xpred[0]-50,xpred[num_bin-1]+50,100000)

        stat, pfir = sp.stats.ttest_1samp(betadf['first'].values,0.0)
        print('First order poly 20: stat:{} p:{}'.format(str(stat),str(pfir)))
        # if pfir < .05:
        #     lines = []            
        #     lineserr = []
        #     for x in np.arange(len(betadf)):
        #         lines.append(betadf.loc[x,'intfirst'] + xplot*betadf.loc[x,'first'])
        #         lineserr.append(betadferr.loc[x,'intfirst'] + xplot*betadferr.loc[x,'first'])
        #     mean = sum(lines)/len(lines)
        #     # lines = lines - mean
        #     sem = stats.sem(lineserr)
        #     axs[row,column].plot(xplot, mean, color='k',linewidth=.5)
        #     axs[row,column].fill_between(xplot, mean-sem, mean+sem, color=color, alpha=.4, lw=0.0, edgecolor='None')

        stat, psec = sp.stats.ttest_1samp(betadf['second2'].values,0.0)
        print('Second order poly 20: stat:{} p:{}'.format(str(stat),str(psec)))
        if psec < .050:
            lines = []
            lineserr = []
            for x in np.arange(len(betadf)):
                lines.append(betadf.loc[x,'intsecond'] + xplot*betadf.loc[x,'second1'] + xplot*xplot*betadf.loc[x,'second2'])
                lineserr.append(betadferr.loc[x,'intsecond'] + xplot*betadferr.loc[x,'second1'] + xplot*xplot*betadferr.loc[x,'second2'])
            mean = sum(lines)/len(lines)
            sem = stats.sem(lineserr)
            axs[row,column].plot(xplot, mean, color='k',linewidth=.5)
            axs[row,column].fill_between(xplot, mean-sem, mean+sem, color=color, alpha=.4, lw=0.0, edgecolor='None')
        

        axs[row,column].errorbar(xpred, data.groupby(['baseline_split'])[thisvar].mean(), yerr=data.groupby(['baseline_split'])['errbar'].sem(),ls='None', ecolor='k', elinewidth=.5)
        axs[row,column].plot(xpred,data.groupby(['baseline_split'])[thisvar].mean(), marker='o', mec='k', mew=.5, mfc=color, ms=5, ls='None', lw=.5)

        axs[row,column].set_aspect("auto")

        if row == 0: 
            axs[row,column].set_ylim(numpy.round(axs[row,column].get_ylim()+np.array([-.025,+.025]),decimals=1)+np.array([0,.0001]))
        elif row == 1:
            axs[row,column].set_ylim(numpy.round(axs[row,column].get_ylim()+np.array([-.0025,+.0025]),decimals=2)+np.array([0,.0001]))
        axs[0,column].set_title('All')
        axs[row,column].ticklabel_format(style='sci',axis='x',scilimits=(0,0))
        axs[row, column].xaxis.set_tick_params(labelbottom=True)
        if (row == 1): 
            axs[row,column].yaxis.set_major_locator(MultipleLocator(.01))
        if (row == 0):
            axs[row,column].yaxis.set_major_locator(MultipleLocator(.1))
        sns.despine(offset=3, trim=True, ax=axs[row,column])


        for par, col in zip(['modality','task'], [np.array([1,2]),np.array([3,4])]):
            # shell()
            splitdata = pd.DataFrame(thisdata.groupby([par,'sub_ID','baseline_split'])[[thisvar,'raw_baseline']].mean()).groupby([par,'sub_ID','baseline_split']).mean().reset_index()

            num_bin = number_of_bins[0]

            for split, column in zip(np.unique(splitdata[par]),col):
                print(par, split)
                data = splitdata[splitdata[par]==split].copy()

                data['errbar'] = np.nan
                print(len(np.unique(data.sub_ID)))
                for s in np.unique(data.sub_ID):
                    submean = data.loc[(data.sub_ID==s),thisvar].mean()
                    data.loc[(data.sub_ID==s),'errbar'] = data.loc[(data.sub_ID==s),thisvar] - submean

                betadf = pd.DataFrame(columns=['sub_ID','intfirst','first','intsecond','second1','second2'])
                betadferr = pd.DataFrame(columns=['sub_ID','intfirst','first','intsecond','second1','second2'])

                meanval = data.groupby('baseline_split')['raw_baseline'].mean()[2]

                for s in np.unique(data.sub_ID):
                    subdata = data[(data.sub_ID==s)].copy()

                    difference = subdata['raw_baseline'].iloc[2] - meanval
                    subdata['raw_baseline_c'] = subdata['raw_baseline'] - difference

                    x = np.array(subdata['raw_baseline_c'][(subdata.sub_ID==s)]).reshape(-1,1)
                    y = np.array(subdata[thisvar][(subdata.sub_ID==s)]).reshape(-1,1)

                    poly_feat = PolynomialFeatures(degree=1)
                    xp = poly_feat.fit_transform(x)
                    xpred = np.linspace(x[0]-100,x[num_bin-1]+100,(num_bin+1)*100)
                    model = sm.OLS(y, xp).fit()
                    b = np.ones((num_bin+1)*100)
                    ypred = np.column_stack((b,xpred))
                    intfirst = model.params[0]
                    first = model.params[1]
                    
                    poly_feat = PolynomialFeatures(degree=2)
                    xp = poly_feat.fit_transform(x)
                    model = sm.OLS(y, xp).fit()
                    b = np.ones((num_bin+1)*100)
                    c = xpred*xpred
                    ypred = np.column_stack((b,xpred,c))
                    intsecond = model.params[0]
                    second1 = model.params[1]
                    second2 = model.params[2]

                    betadf = pd.concat([betadf, pd.DataFrame.from_records([{'sub_ID':s, 'intfirst': intfirst, 'first':first,  'intsecond':intsecond, 'second1':second1, 'second2':second2}])],ignore_index=True)

                    # for errorbars
                    y = np.array(subdata['errbar'][(subdata.sub_ID==s)]).reshape(-1,1)

                    poly_feat = PolynomialFeatures(degree=1)
                    xp = poly_feat.fit_transform(x)
                    xpred = np.linspace(x[0]-100,x[num_bin-1]+100,(num_bin+1)*100)
                    model = sm.OLS(y, xp).fit()
                    b = np.ones((5+1)*100)
                    ypred = np.column_stack((b,xpred))
                    intfirst = model.params[0]
                    first = model.params[1]
                    
                    poly_feat = PolynomialFeatures(degree=2)
                    xp = poly_feat.fit_transform(x)
                    model = sm.OLS(y, xp).fit()
                    b = np.ones((num_bin+1)*100)
                    c = xpred*xpred
                    ypred = np.column_stack((b,xpred,c))
                    intsecond = model.params[0]
                    second1 = model.params[1]
                    second2 = model.params[2]

                    betadferr = pd.concat([betadferr, pd.DataFrame.from_records([{'sub_ID':s, 'intfirst': intfirst, 'first':first,  'intsecond':intsecond, 'second1':second1, 'second2':second2}])],ignore_index=True)

                xpred = data.groupby(['baseline_split'])['raw_baseline'].mean()
                xplot = np.linspace(xpred[0]-50,xpred[num_bin-1]+50,100000)

                stat, pfir = sp.stats.ttest_1samp(betadf['first'].values,0.0)
                co_d = betadf['first'].values.mean()/betadf['first'].values.std()
                print('First order poly: beta:{}, stat:{} p:{}'.format(str(betadf['first'].values.mean()),str(np.round(stat,3)),str(np.round(pfir,3))))
                print('Cohen\'s d: {}'.format(np.round(co_d,2)))
                if pfir < .05:
                    lines = []            
                    lineserr = []
                    for x in np.arange(len(betadf)):
                        lines.append(betadf.loc[x,'intfirst'] + xplot*betadf.loc[x,'first'])
                        lineserr.append(betadferr.loc[x,'intfirst'] + xplot*betadferr.loc[x,'first'])
                    mean = sum(lines)/len(lines)
                    sem = stats.sem(lineserr)
                    axs[row,column].plot(xplot, mean, color='k',linewidth=.5)
                    axs[row,column].fill_between(xplot, mean-sem, mean+sem, color=color, alpha=.4, lw=0.0, edgecolor='None')

                stat, psec = sp.stats.ttest_1samp(betadf['second2'].values,0.0)
                co_d = betadf['second2'].values.mean()/betadf['second2'].values.std()
                print('Second order poly: beta:{}, stat:{} one-sided p:{}'.format(str(betadf['second2'].values.mean()),str(np.round(stat,3)),str(np.round(psec/2,4))))
                print('Cohen\'s d: {}'.format(np.round(co_d,2)))
                if psec/2 < .05:
                    lines = []
                    lineserr = []
                    for x in np.arange(len(betadf)):
                        lines.append(betadf.loc[x,'intsecond'] + xplot*betadf.loc[x,'second1'] + xplot*xplot*betadf.loc[x,'second2'])
                        lineserr.append(betadferr.loc[x,'intsecond'] + xplot*betadferr.loc[x,'second1'] + xplot*xplot*betadferr.loc[x,'second2'])
                    mean = sum(lines)/len(lines)
                    sem = stats.sem(lineserr)
                    axs[row,column].plot(xplot, mean, color='k',linewidth=.5)
                    axs[row,column].fill_between(xplot, mean-sem, mean+sem, color=color, alpha=.4, lw=0.0, edgecolor='None')
                
                axs[row,column].errorbar(xpred, data.groupby(['baseline_split'])[thisvar].mean(), yerr=data.groupby(['baseline_split'])['errbar'].sem(),ls='None', ecolor='k', elinewidth=.5)
                axs[row,column].plot(xpred,data.groupby(['baseline_split'])[thisvar].mean(), marker='o', mec='k', mew=.5, mfc=color, ms=5, ls='None', lw=.5)
                
                if split == 'aud':
                    axs[0,column].set_title('Auditory')
                elif split == 'vis':
                    axs[0,column].set_title('Visual')
                elif split == 'dis':
                    axs[0,column].set_title('Discrimination')
                elif split == 'det':
                    axs[0,column].set_title('Detection')
                # plt.xlim(3000,4200)

                if row == 0: 
                    axs[row,column].set_ylim(numpy.round(axs[row,column].get_ylim()+np.array([-.025,+.025]),decimals=1)+np.array([0,.0001]))
                elif row == 1:
                    axs[row,column].set_ylim(numpy.round(axs[row,column].get_ylim()+np.array([-.0025,+.0025]),decimals=2)+np.array([0,.0001]))


                axs[row, column].xaxis.set_tick_params(labelbottom=True)
                axs[1,4].ticklabel_format(style='sci',axis='x',scilimits=(0,0))

                # if row == 1 and column != 3:
                #     axs[row, column].xaxis.set_ticklabels([])

                if (row == 1): #& (1 <= column <= 4):
                    axs[row,column].yaxis.set_major_locator(MultipleLocator(.01))
                if (row == 0):
                    axs[row,column].yaxis.set_major_locator(MultipleLocator(.1))
                axs[row,0].set_ylabel(thisylab)

                sns.despine(offset=3, trim=True, ax=axs[row,column])

    fig.savefig(os.path.join(this_dir, 'baseline_means.pdf'.format(var)),transparent=True)
    fig.savefig(os.path.join(this_dir, 'baseline_means.png'.format(var)),dpi=1200,transparent=False)
    plt.close()


def binned_plot_hitfa(datain, datain20, number_of_bins, var, ylab, this_dir):
    from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)

    color = 'darkgreen'
    cm = 1/2.54  # centimeters in inches

    gs_kw = dict(wspace=.65, left=.08, right=.99, hspace=.25, top=.92, bottom=.15) 
    fig, axs = plt.subplots(nrows=2, ncols=5, sharex=True, figsize=(19*cm,8*cm))

    for thisdata, thisdata20, thisvar, thisylab in zip(datain, datain20, var, ylab):
        print(thisvar)

        if thisvar == 'hit_rate':
            row = 0
        elif thisvar == 'fa_rate':
            row = 1

        column = 0

        data = pd.DataFrame(thisdata20.groupby(['sub_ID','baseline_split'])[[thisvar,'raw_baseline']].mean()).reset_index()

        data['errbar'] = np.nan
        for s in np.unique(data.sub_ID):
            submean = data.loc[(data.sub_ID==s),thisvar].mean()
            data.loc[(data.sub_ID==s),'errbar'] = data.loc[(data.sub_ID==s),thisvar] - submean

        betadf = pd.DataFrame(columns=['sub_ID','intfirst','first','intsecond','second1','second2'])
        betadferr = pd.DataFrame(columns=['sub_ID','intfirst','first','intsecond','second1','second2'])

        meanval = data.groupby('baseline_split')['raw_baseline'].mean()[2]
        print(len(np.unique(data.sub_ID)))
        for s in np.unique(data.sub_ID):
            subdata = data[(data.sub_ID==s)].copy()

            difference = subdata['raw_baseline'].iloc[2] - meanval
            subdata['raw_baseline_c'] = subdata['raw_baseline'] - difference

            x = np.array(subdata['raw_baseline_c'][(subdata.sub_ID==s)]).reshape(-1,1)
            y = np.array(subdata[thisvar][(subdata.sub_ID==s)]).reshape(-1,1)

            poly_feat = PolynomialFeatures(degree=1)
            xp = poly_feat.fit_transform(x)
            xpred = np.linspace(x[0]-100,x[number_of_bins-1]+100,(number_of_bins+1)*100)
            model = sm.OLS(y, xp).fit()
            b = np.ones((number_of_bins+1)*100)
            ypred = np.column_stack((b,xpred))
            intfirst = model.params[0]
            first = model.params[1]
            
            poly_feat = PolynomialFeatures(degree=2)
            xp = poly_feat.fit_transform(x)
            model = sm.OLS(y, xp).fit()
            b = np.ones((number_of_bins+1)*100)
            c = xpred*xpred
            ypred = np.column_stack((b,xpred,c))
            intsecond = model.params[0]
            second1 = model.params[1]
            second2 = model.params[2]

            betadf = pd.concat([betadf, pd.DataFrame.from_records([{'sub_ID':s, 'intfirst': intfirst, 'first':first,  'intsecond':intsecond, 'second1':second1, 'second2':second2}])],ignore_index=True)

            # for errorbars
            y = np.array(subdata['errbar'][(subdata.sub_ID==s)]).reshape(-1,1)

            poly_feat = PolynomialFeatures(degree=1)
            xp = poly_feat.fit_transform(x)
            xpred = np.linspace(x[0]-100,x[number_of_bins-1]+100,(number_of_bins+1)*100)
            model = sm.OLS(y, xp).fit()
            b = np.ones((number_of_bins+1)*100)
            ypred = np.column_stack((b,xpred))
            intfirst = model.params[0]
            first = model.params[1]
            
            poly_feat = PolynomialFeatures(degree=2)
            xp = poly_feat.fit_transform(x)
            model = sm.OLS(y, xp).fit()
            b = np.ones((number_of_bins+1)*100)
            c = xpred*xpred
            ypred = np.column_stack((b,xpred,c))
            intsecond = model.params[0]
            second1 = model.params[1]
            second2 = model.params[2]

            betadferr = pd.concat([betadferr, pd.DataFrame.from_records([{'sub_ID':s, 'intfirst': intfirst, 'first':first,  'intsecond':intsecond, 'second1':second1, 'second2':second2}])],ignore_index=True)

        xpred = data.groupby(['baseline_split'])['raw_baseline'].mean()
        # xpred = data.groupby(['exp','session','miniblock','sub_ID','baseline_split'])['raw_baseline'].mean().groupby(['exp','sub_ID','baseline_split','session']).mean().groupby(['exp','baseline_split']).mean().groupby('baseline_split').mean().reset_index()
        xplot = np.linspace(xpred[0]-50,xpred[number_of_bins-1]+50,100000)

        stat, psec = sp.stats.ttest_1samp(betadf['second2'].values,0.0)
        print('Second order poly 20: beta:{}, stat:{} p:{}'.format(str(betadf['second2'].values.mean()),str(np.round(stat,3)),str(np.round(psec,5))))
        if psec < .05:
            lines = []
            lineserr = []
            for x in np.arange(len(betadf)):
                lines.append(betadf.loc[x,'intsecond'] + xplot*betadf.loc[x,'second1'] + xplot*xplot*betadf.loc[x,'second2'])
                lineserr.append(betadferr.loc[x,'intsecond'] + xplot*betadferr.loc[x,'second1'] + xplot*xplot*betadferr.loc[x,'second2'])
            mean = sum(lines)/len(lines)
            sem = stats.sem(lineserr)
            axs[row,column].plot(xplot, mean, color='k',linewidth=.5)
            axs[row,column].fill_between(xplot, mean-sem, mean+sem, color=color, alpha=.4, lw=0.0, edgecolor='None')
        #else:
        stat, pfir = sp.stats.ttest_1samp(betadf['first'].values,0.0)
        print('First order poly 20: beta:{}, stat:{} p:{}'.format(str(betadf['first'].values.mean()),str(np.round(stat,3)),str(np.round(pfir,3))))
        if pfir < .05:
            lines = []            
            lineserr = []
            for x in np.arange(len(betadf)):
                lines.append(betadf.loc[x,'intfirst'] + xplot*betadf.loc[x,'first'])
                lineserr.append(betadferr.loc[x,'intfirst'] + xplot*betadferr.loc[x,'first'])
            mean = sum(lines)/len(lines)
            # lines = lines - mean
            sem = stats.sem(lineserr)
            axs[row,column].plot(xplot, mean, color='k',linewidth=.5)
            axs[row,column].fill_between(xplot, mean-sem, mean+sem, color=color, alpha=.4, lw=0.0, edgecolor='None')
                
        axs[row,column].errorbar(xpred, data.groupby(['baseline_split'])[thisvar].mean(), yerr=data.groupby(['baseline_split'])['errbar'].sem(),ls='None', ecolor='k', elinewidth=.5)
        axs[row,column].plot(xpred,data.groupby(['baseline_split'])[thisvar].mean(), marker='o', mec='k', mew=.5, mfc=color, ms=5, ls='None', lw=.5)

        axs[row,column].set_aspect("auto")

        axs[row,column].set_ylim(numpy.round(axs[row,column].get_ylim()+np.array([-.0025,+.0025]),decimals=2)+np.array([0,.0001]))
        axs[0,column].set_title('All')
        axs[row,column].ticklabel_format(style='sci',axis='x',scilimits=(0,0))
        if (row == 1): 
            axs[row,column].yaxis.set_major_locator(MultipleLocator(.01))
        if (row == 0):
            axs[row,column].yaxis.set_major_locator(MultipleLocator(.01))
        sns.despine(offset=3, trim=True, ax=axs[row,column])


        for par, col in zip(['modality','task'], [np.array([1,2]),np.array([3,4])]):
            # shell()
            splitdata = pd.DataFrame(thisdata.groupby([par,'sub_ID','baseline_split'])[[thisvar,'raw_baseline']].mean()).groupby([par,'sub_ID','baseline_split']).mean().reset_index()

            for split, column in zip(np.unique(splitdata[par]),col):
                print(par, split)
                data = splitdata[splitdata[par]==split].copy()

                data['errbar'] = np.nan
                print(len(np.unique(data.sub_ID)))
                for s in np.unique(data.sub_ID):
                    submean = data.loc[(data.sub_ID==s),thisvar].mean()
                    data.loc[(data.sub_ID==s),'errbar'] = data.loc[(data.sub_ID==s),thisvar] - submean

                betadf = pd.DataFrame(columns=['sub_ID','intfirst','first','intsecond','second1','second2'])
                betadferr = pd.DataFrame(columns=['sub_ID','intfirst','first','intsecond','second1','second2'])

                meanval = data.groupby('baseline_split')['raw_baseline'].mean()[2]

                for s in np.unique(data.sub_ID):
                    subdata = data[(data.sub_ID==s)].copy()

                    difference = subdata['raw_baseline'].iloc[2] - meanval
                    subdata['raw_baseline_c'] = subdata['raw_baseline'] - difference

                    x = np.array(subdata['raw_baseline_c'][(subdata.sub_ID==s)]).reshape(-1,1)
                    y = np.array(subdata[thisvar][(subdata.sub_ID==s)]).reshape(-1,1)

                    poly_feat = PolynomialFeatures(degree=1)
                    xp = poly_feat.fit_transform(x)
                    xpred = np.linspace(x[0]-100,x[4]+100,(number_of_bins+1)*100)
                    model = sm.OLS(y, xp).fit()
                    b = np.ones((number_of_bins+1)*100)
                    ypred = np.column_stack((b,xpred))
                    intfirst = model.params[0]
                    first = model.params[1]
                    
                    poly_feat = PolynomialFeatures(degree=2)
                    xp = poly_feat.fit_transform(x)
                    model = sm.OLS(y, xp).fit()
                    b = np.ones((number_of_bins+1)*100)
                    c = xpred*xpred
                    ypred = np.column_stack((b,xpred,c))
                    intsecond = model.params[0]
                    second1 = model.params[1]
                    second2 = model.params[2]

                    betadf = pd.concat([betadf, pd.DataFrame.from_records([{'sub_ID':s, 'intfirst': intfirst, 'first':first,  'intsecond':intsecond, 'second1':second1, 'second2':second2}])],ignore_index=True)

                    # for errorbars
                    y = np.array(subdata['errbar'][(subdata.sub_ID==s)]).reshape(-1,1)

                    poly_feat = PolynomialFeatures(degree=1)
                    xp = poly_feat.fit_transform(x)
                    xpred = np.linspace(x[0]-100,x[4]+100,(number_of_bins+1)*100)
                    model = sm.OLS(y, xp).fit()
                    b = np.ones((number_of_bins+1)*100)
                    ypred = np.column_stack((b,xpred))
                    intfirst = model.params[0]
                    first = model.params[1]
                    
                    poly_feat = PolynomialFeatures(degree=2)
                    xp = poly_feat.fit_transform(x)
                    model = sm.OLS(y, xp).fit()
                    b = np.ones((number_of_bins+1)*100)
                    c = xpred*xpred
                    ypred = np.column_stack((b,xpred,c))
                    intsecond = model.params[0]
                    second1 = model.params[1]
                    second2 = model.params[2]

                    betadferr = pd.concat([betadferr, pd.DataFrame.from_records([{'sub_ID':s, 'intfirst': intfirst, 'first':first,  'intsecond':intsecond, 'second1':second1, 'second2':second2}])],ignore_index=True)

                xpred = data.groupby(['baseline_split'])['raw_baseline'].mean()
                xplot = np.linspace(xpred[0]-50,xpred[4]+50,100000)

                stat, psec = sp.stats.ttest_1samp(betadf['second2'].values,0.0)
                print('Second order poly: beta:{}, stat:{}, p:{}'.format(str(betadf['second2'].values.mean()),str(np.round(stat,3)),str(np.round(psec,4))))
                if psec < .05:
                    lines = []
                    lineserr = []
                    for x in np.arange(len(betadf)):
                        lines.append(betadf.loc[x,'intsecond'] + xplot*betadf.loc[x,'second1'] + xplot*xplot*betadf.loc[x,'second2'])
                        lineserr.append(betadferr.loc[x,'intsecond'] + xplot*betadferr.loc[x,'second1'] + xplot*xplot*betadferr.loc[x,'second2'])
                    mean = sum(lines)/len(lines)
                    sem = stats.sem(lineserr)
                    axs[row,column].plot(xplot, mean, color='k',linewidth=.5)
                    axs[row,column].fill_between(xplot, mean-sem, mean+sem, color=color, alpha=.4, lw=0.0, edgecolor='None')
                # else:
                stat, pfir = sp.stats.ttest_1samp(betadf['first'].values,0.0)
                print('First order poly: beta:{}, stat:{} p:{}'.format(str(betadf['first'].values.mean()),str(np.round(stat,3)),str(np.round(pfir,3))))
                if pfir < .05:
                    lines = []            
                    lineserr = []
                    for x in np.arange(len(betadf)):
                        lines.append(betadf.loc[x,'intfirst'] + xplot*betadf.loc[x,'first'])
                        lineserr.append(betadferr.loc[x,'intfirst'] + xplot*betadferr.loc[x,'first'])
                    mean = sum(lines)/len(lines)
                    sem = stats.sem(lineserr)
                    axs[row,column].plot(xplot, mean, color='k',linewidth=.5)
                    axs[row,column].fill_between(xplot, mean-sem, mean+sem, color=color, alpha=.4, lw=0.0, edgecolor='None')
                    

                
                axs[row,column].errorbar(xpred, data.groupby(['baseline_split'])[thisvar].mean(), yerr=data.groupby(['baseline_split'])['errbar'].sem(),ls='None', ecolor='k', elinewidth=.5)
                axs[row,column].plot(xpred,data.groupby(['baseline_split'])[thisvar].mean(), marker='o', mec='k', mew=.5, mfc=color, ms=5, ls='None', lw=.5)
                
                if split == 'aud':
                    axs[0,column].set_title('Auditory')
                elif split == 'vis':
                    axs[0,column].set_title('Visual')
                elif split == 'dis':
                    axs[0,column].set_title('Discrimination')
                elif split == 'det':
                    axs[0,column].set_title('Detection')
                # plt.xlim(3000,4200)

                if row == 0: 
                    axs[row,column].set_ylim(numpy.round(axs[row,column].get_ylim()+np.array([-.0025,+.0025]),decimals=2)+np.array([0,.0001]))
                elif row == 1:
                    axs[row,column].set_ylim(numpy.round(axs[row,column].get_ylim()+np.array([-.0025,+.0025]),decimals=2)+np.array([0,.0001]))


                axs[1,4].ticklabel_format(style='sci',axis='x',scilimits=(0,0))

                # if row == 1 and column != 3:
                #     axs[row, column].xaxis.set_ticklabels([])

                if (row == 1): #& (1 <= column <= 4):
                    axs[row,column].yaxis.set_major_locator(MultipleLocator(.01))
                if (row == 0):
                    axs[row,column].yaxis.set_major_locator(MultipleLocator(.01))
                axs[row,0].set_ylabel(thisylab)

                sns.despine(offset=3, trim=True, ax=axs[row,column])

    fig.savefig(os.path.join(this_dir, 'baseline_means_hitfa.pdf'.format(var)),transparent=True)
    fig.savefig(os.path.join(this_dir, 'baseline_means_hitfa.png'.format(var)),dpi=1200,transparent=False)
    plt.close()

def max_points(datain, datain20, var):
  
    # gs_kw = dict(wspace=.65, left=.08, right=.99, hspace=.25, top=.92, bottom=.15) #,wspace=.7,hspace=.3
    cm = 1/2.54  # centimeters in inches
    fig, axs = plt.subplots(nrows=2, ncols=3, sharex=True, figsize=(13*cm,8*cm)) #, gridspec_kw=gs_kw

    maxdf = pd.DataFrame(columns=['task','drug','measure','sub_ID','max','beta'])

    shell(colors="neutral")

    for thisdata, thisdata20, thisvar in zip(datain, datain20, var):
        print(thisvar)

        if thisvar == 'd':
            row = 0
        elif thisvar == 'RT':
            row = 1

        # shell(colors="neutral")

        for drug,col in zip(['PCB','ATX','DNP'],['darkgreen','steelblue','brown']):

            data = pd.DataFrame(thisdata20[thisdata20.drug==drug].groupby(['sub_ID','baseline_split']).mean()).reset_index()

            number_of_bins = 20

            betadf = pd.DataFrame(columns=['sub_ID','intfirst','first','intsecond','second1','second2'])
            betadferr = pd.DataFrame(columns=['sub_ID','intfirst','first','intsecond','second1','second2'])

            # print(len(np.unique(data.sub_ID)))
            for s in np.unique(data.sub_ID):
                subdata = data[(data.sub_ID==s)].copy()

                x = np.array(subdata['raw_baseline'][(subdata.sub_ID==s)]).reshape(-1,1)
                y = np.array(subdata[thisvar][(subdata.sub_ID==s)]).reshape(-1,1)

                poly_feat = PolynomialFeatures(degree=1)
                xp = poly_feat.fit_transform(x)
                xpred = np.linspace(x[0]-100,x[19]+100,(number_of_bins+1)*100)
                model = sm.OLS(y, xp).fit()
                b = np.ones((number_of_bins+1)*100)
                ypred = np.column_stack((b,xpred))
                intfirst = model.params[0]
                first = model.params[1]
                
                poly_feat = PolynomialFeatures(degree=2)
                xp = poly_feat.fit_transform(x)
                model = sm.OLS(y, xp).fit()
                b = np.ones((number_of_bins+1)*100)
                c = xpred*xpred
                ypred = np.column_stack((b,xpred,c))
                intsecond = model.params[0]
                second1 = model.params[1]
                second2 = model.params[2]

                betadf = pd.DataFrame.from_records([{'sub_ID':s, 'intfirst': intfirst, 'first':first,  'intsecond':intsecond, 'second1':second1, 'second2':second2}])

                xplot = np.linspace(xpred[0],xpred[-1],100000)
                
                if thisvar == 'd':
                    line = betadf['intsecond'][0] + xplot*betadf['second1'][0] + xplot*xplot*betadf['second2'][0]
                    maxpoint = np.where(line==line.max())[0][0]
                    maxpoint = xplot[maxpoint][0]
                elif thisvar == 'RT':
                    line = betadf['intsecond'][0] + xplot*betadf['second1'][0] + xplot*xplot*betadf['second2'][0]
                    maxpoint = np.where(line==line.min())[0][0]
                    maxpoint = xplot[maxpoint][0]

                maxdf = pd.concat([maxdf,pd.DataFrame.from_records([{'task':'all','drug':drug,'measure':thisvar,'sub_ID':s,'max':maxpoint,'beta':betadf['second2'][0]}])])

                ### now for detect, discrim etc.

        for drug,col in zip(['PCB','ATX','DNP'],['darkgreen','steelblue','brown']):

            splitdata = pd.DataFrame(thisdata[thisdata.drug==drug].groupby(['task','sub_ID','baseline_split'])[[thisvar,'raw_baseline']].mean()).reset_index()
            
            for task, column in zip(['det','dis'],[2,1]):

                data = splitdata[splitdata['task']==task].copy()

                number_of_bins = 5

                betadf = pd.DataFrame(columns=['sub_ID','intfirst','first','intsecond','second1','second2'])
                betadferr = pd.DataFrame(columns=['sub_ID','intfirst','first','intsecond','second1','second2'])

                for s in np.unique(data.sub_ID):
                    subdata = data[(data.sub_ID==s)].copy()

                    x = np.array(subdata['raw_baseline'][(subdata.sub_ID==s)]).reshape(-1,1)
                    y = np.array(subdata[thisvar][(subdata.sub_ID==s)]).reshape(-1,1)

                    poly_feat = PolynomialFeatures(degree=1)
                    xp = poly_feat.fit_transform(x)
                    xpred = np.linspace(x[0]-100,x[number_of_bins-1]+100,(number_of_bins+1)*100)
                    model = sm.OLS(y, xp).fit()
                    b = np.ones((number_of_bins+1)*100)
                    ypred = np.column_stack((b,xpred))
                    intfirst = model.params[0]
                    first = model.params[1]
                    
                    poly_feat = PolynomialFeatures(degree=2)
                    xp = poly_feat.fit_transform(x)
                    model = sm.OLS(y, xp).fit()
                    b = np.ones((number_of_bins+1)*100)
                    c = xpred*xpred
                    ypred = np.column_stack((b,xpred,c))
                    intsecond = model.params[0]
                    second1 = model.params[1]
                    second2 = model.params[2]

                    betadf = pd.DataFrame.from_records([{'sub_ID':s, 'intfirst': intfirst, 'first':first,  'intsecond':intsecond, 'second1':second1, 'second2':second2}])

                    xplot = np.linspace(xpred[0],xpred[-1],100000)
                    
                    if thisvar == 'd':
                        line = betadf['intsecond'][0] + xplot*betadf['second1'][0] + xplot*xplot*betadf['second2'][0]
                        maxpoint = np.where(line==line.max())[0][0]
                        maxpoint = xplot[maxpoint][0]
                    elif thisvar == 'RT':
                        line = betadf['intsecond'][0] + xplot*betadf['second1'][0] + xplot*xplot*betadf['second2'][0]
                        maxpoint = np.where(line==line.min())[0][0]
                        maxpoint = xplot[maxpoint][0]

                    maxdf = pd.concat([maxdf,pd.DataFrame.from_records([{'task':task,'drug':drug,'measure':thisvar,'sub_ID':s,'max':maxpoint,'beta':betadf['second2'][0]}])])

            # sns.despine(offset=3, trim=True)
    return maxdf
    
        # fig.savefig(os.path.join(this_dir, 'baseline_pupil_drugs_try.png'),dpi=1200, transparent = True)
        # fig.savefig(os.path.join(this_dir, 'baseline_pupil_drugs_try.pdf'), transparent = True)
        # plt.close()


            # xpred = data.groupby(['baseline_split'])['raw_baseline'].mean()
            # xpred = data.groupby(['exp','session','miniblock','sub_ID','baseline_split'])['raw_baseline'].mean().groupby(['exp','sub_ID','baseline_split','session']).mean().groupby(['exp','baseline_split']).mean().groupby('baseline_split').mean().reset_index()
            

            # stat, psec = sp.stats.ttest_1samp(betadf['second2'].values,0.0)
            # print('Second order poly 20 {}: beta:{}, stat:{} p:{}'.format(drug, str(betadf['second2'].values.mean()),str(np.round(stat,3)),str(np.round(psec,5))))
            # if psec < .050:
            #     lines = []
            #     lineserr = []
            #     for x in np.arange(len(betadf)):
            #         lines.append(betadf.loc[x,'intsecond'] + xplot*betadf.loc[x,'second1'] + xplot*xplot*betadf.loc[x,'second2'])
            #         # maxpoint = max(betadf.loc[x,'intsecond'] + xplot*betadf.loc[x,'second1'] + xplot*xplot*betadf.loc[x,'second2'])
            #         # maxdf.append({"task":"all","drug":drug,"measure":thisvar,"max":maxpoint})
            #         lineserr.append(betadferr.loc[x,'intsecond'] + xplot*betadferr.loc[x,'second1'] + xplot*xplot*betadferr.loc[x,'second2'])
            #     mean = sum(lines)/len(lines)
            #     sem = stats.sem(lineserr)
            #     axs[row,0].plot(xplot, mean, color='k',linewidth=.5)
            #     axs[row,0].fill_between(xplot, mean-sem, mean+sem, color=col, alpha=.4, lw=0.0, edgecolor='None')
            # #else:


def binned_plot_pupil_drugs(datain, datain20, number_of_bins, var, ylab, this_dir):
    print(var)
    color = 'indianred'
    
    # datain = datain[~datain['drug'].isnull()]

    # gs_kw = dict(wspace=.65, left=.08, right=.99, hspace=.25, top=.92, bottom=.15) #,wspace=.7,hspace=.3
    cm = 1/2.54  # centimeters in inches
    fig, axs = plt.subplots(nrows=2, ncols=3, sharex=True, figsize=(13*cm,8*cm)) #, gridspec_kw=gs_kw

    for thisdata, thisdata20, thisvar, thisylab in zip(datain, datain20, var, ylab):
        print(thisvar)

        if thisvar == 'd':
            row = 0
        elif thisvar == 'RT':
            row = 1

        # for drug,col in zip(['PCB','DNP'],['darkgreen','steelblue']):
        for drug,col in zip(['PCB','DNP','ATX'],['darksalmon','lightsteelblue','indianred']):

            data = pd.DataFrame(thisdata20[thisdata20.drug==drug].groupby(['sub_ID','baseline_split']).mean()).reset_index()

            data['errbar'] = np.nan
            for s in np.unique(data.sub_ID):
                submean = data.loc[(data.sub_ID==s),thisvar].mean()
                data.loc[(data.sub_ID==s),'errbar'] = data.loc[(data.sub_ID==s),thisvar] - submean

            betadf = pd.DataFrame(columns=['sub_ID','intfirst','first','intsecond','second1','second2'])
            betadferr = pd.DataFrame(columns=['sub_ID','intfirst','first','intsecond','second1','second2'])

            meanval = data.groupby('baseline_split')['raw_baseline'].mean()[9]
            # print(len(np.unique(data.sub_ID)))
            for s in np.unique(data.sub_ID):
                subdata = data[(data.sub_ID==s)].copy()

                difference = subdata['raw_baseline'].iloc[9] - meanval
                subdata['raw_baseline_c'] = subdata['raw_baseline'] - difference

                x = np.array(subdata['raw_baseline_c'][(subdata.sub_ID==s)]).reshape(-1,1)
                y = np.array(subdata[thisvar][(subdata.sub_ID==s)]).reshape(-1,1)

                poly_feat = PolynomialFeatures(degree=1)
                xp = poly_feat.fit_transform(x)
                xpred = np.linspace(x[0]-100,x[19]+100,(number_of_bins+1)*100)
                model = sm.OLS(y, xp).fit()
                b = np.ones((number_of_bins+1)*100)
                ypred = np.column_stack((b,xpred))
                intfirst = model.params[0]
                first = model.params[1]
                
                poly_feat = PolynomialFeatures(degree=2)
                xp = poly_feat.fit_transform(x)
                model = sm.OLS(y, xp).fit()
                b = np.ones((number_of_bins+1)*100)
                c = xpred*xpred
                ypred = np.column_stack((b,xpred,c))
                intsecond = model.params[0]
                second1 = model.params[1]
                second2 = model.params[2]

                betadf = pd.concat([betadf, pd.DataFrame.from_records([{'sub_ID':s, 'intfirst': intfirst, 'first':first,  'intsecond':intsecond, 'second1':second1, 'second2':second2}])],ignore_index=True)

                # for errorbars
                y = np.array(subdata['errbar'][(subdata.sub_ID==s)]).reshape(-1,1)

                poly_feat = PolynomialFeatures(degree=1)
                xp = poly_feat.fit_transform(x)
                xpred = np.linspace(x[0]-100,x[19]+100,(number_of_bins+1)*100)
                model = sm.OLS(y, xp).fit()
                b = np.ones((number_of_bins+1)*100)
                ypred = np.column_stack((b,xpred))
                intfirst = model.params[0]
                first = model.params[1]
                
                poly_feat = PolynomialFeatures(degree=2)
                xp = poly_feat.fit_transform(x)
                model = sm.OLS(y, xp).fit()
                b = np.ones((number_of_bins+1)*100)
                c = xpred*xpred
                ypred = np.column_stack((b,xpred,c))
                intsecond = model.params[0]
                second1 = model.params[1]
                second2 = model.params[2]

                betadferr = pd.concat([betadferr, pd.DataFrame.from_records([{'sub_ID':s, 'intfirst': intfirst, 'first':first,  'intsecond':intsecond, 'second1':second1, 'second2':second2}])],ignore_index=True)


            xpred = data.groupby(['baseline_split'])['raw_baseline'].mean()
            # xpred = data.groupby(['exp','session','miniblock','sub_ID','baseline_split'])['raw_baseline'].mean().groupby(['exp','sub_ID','baseline_split','session']).mean().groupby(['exp','baseline_split']).mean().groupby('baseline_split').mean().reset_index()
            xplot = np.linspace(xpred[0]-50,xpred[19]+50,100000)

            stat, psec = sp.stats.ttest_1samp(betadf['second2'].values,0.0)
            print('Second order poly 20 {}: beta:{}, stat:{} p:{}'.format(drug, str(betadf['second2'].values.mean()),str(np.round(stat,3)),str(np.round(psec,5))))
            if psec < .05:
                lines = []
                lineserr = []
                for x in np.arange(len(betadf)):
                    lines.append(betadf.loc[x,'intsecond'] + xplot*betadf.loc[x,'second1'] + xplot*xplot*betadf.loc[x,'second2'])
                    lineserr.append(betadferr.loc[x,'intsecond'] + xplot*betadferr.loc[x,'second1'] + xplot*xplot*betadferr.loc[x,'second2'])
                mean = sum(lines)/len(lines)
                sem = stats.sem(lineserr)
                axs[row,0].plot(xplot, mean, color='k',linewidth=.5)
                axs[row,0].fill_between(xplot, mean-sem, mean+sem, color=col, alpha=.4, lw=0.0, edgecolor='None')
            #else:    

            xpred = data.groupby(['baseline_split'])['raw_baseline'].mean()

            axs[row,0].errorbar(xpred, data.groupby(['baseline_split'])[thisvar].mean(), yerr=data.groupby(['baseline_split'])['errbar'].sem(),ls='None', ecolor='k', elinewidth=.5, label='')
            axs[row,0].plot(xpred,data.groupby(['baseline_split'])[thisvar].mean(), marker='o', mec='k', mew=.5, mfc=col, ms=5, ls='None', lw=.5, label=drug)
            axs[row,0].set_ylabel(thisylab)
            axs[row,0].ticklabel_format(style='sci',axis='x',scilimits=(0,0))
            axs[0,0].set_title('All')
            axs[0,0].set_ylim((1.0,1.91))

            if row == 0: 
                axs[row,0].set_ylim(numpy.round(axs[row,0].get_ylim()+np.array([-.025,+.05]),decimals=1)+np.array([0,.0001]))
            elif row == 1:
                axs[row,0].set_ylim(numpy.round(axs[row,0].get_ylim()+np.array([-.0025,+.0025]),decimals=2)+np.array([0,.0001]))
            # axs[0,column].set_title('All')
            axs[row,0].ticklabel_format(style='sci',axis='x',scilimits=(0,0))
            if (row == 1): 
                axs[row,0].yaxis.set_major_locator(MultipleLocator(.01))
            if (row == 0):
                axs[row,0].yaxis.set_major_locator(MultipleLocator(.1))
            sns.despine(offset=3, trim=True, ax=axs[row,0])

        # thisdata = thisdata[thisdata['modality']=='vis']

        for drug,col in zip(['PCB','DNP','ATX'],['coral','steelblue','brown']):
        # for drug,col in zip(['PCB','DNP'],['darkgreen','steelblue']):

            splitdata = pd.DataFrame(thisdata[thisdata.drug==drug].groupby(['task','sub_ID','baseline_split'])[[thisvar,'raw_baseline']].mean()).reset_index()
            
            for task, column in zip(['det','dis'],[2,1]):

                data = splitdata[splitdata['task']==task].copy()

                data['errbar'] = np.nan
                for s in np.unique(data.sub_ID):
                    submean = data.loc[(data.sub_ID==s),thisvar].mean()
                    data.loc[(data.sub_ID==s),'errbar'] = data.loc[(data.sub_ID==s),thisvar] - submean

                betadf = pd.DataFrame(columns=['sub_ID','intfirst','first','intsecond','second1','second2'])
                betadferr = pd.DataFrame(columns=['sub_ID','intfirst','first','intsecond','second1','second2'])

                meanval = data.groupby('baseline_split')['raw_baseline'].mean()[2]

                for s in np.unique(data.sub_ID):
                    subdata = data[(data.sub_ID==s)].copy()

                    difference = subdata['raw_baseline'].iloc[2] - meanval
                    subdata['raw_baseline_c'] = subdata['raw_baseline'] - difference

                    x = np.array(subdata['raw_baseline_c'][(subdata.sub_ID==s)]).reshape(-1,1)
                    y = np.array(subdata[thisvar][(subdata.sub_ID==s)]).reshape(-1,1)

                    poly_feat = PolynomialFeatures(degree=1)
                    xp = poly_feat.fit_transform(x)
                    xpred = np.linspace(x[0]-100,x[4]+100,(number_of_bins+1)*100)
                    model = sm.OLS(y, xp).fit()
                    b = np.ones((number_of_bins+1)*100)
                    ypred = np.column_stack((b,xpred))
                    intfirst = model.params[0]
                    first = model.params[1]
                    
                    poly_feat = PolynomialFeatures(degree=2)
                    xp = poly_feat.fit_transform(x)
                    model = sm.OLS(y, xp).fit()
                    b = np.ones((number_of_bins+1)*100)
                    c = xpred*xpred
                    ypred = np.column_stack((b,xpred,c))
                    intsecond = model.params[0]
                    second1 = model.params[1]
                    second2 = model.params[2]

                    betadf = pd.concat([betadf, pd.DataFrame.from_records([{'sub_ID':s, 'intfirst': intfirst, 'first':first,  'intsecond':intsecond, 'second1':second1, 'second2':second2}])],ignore_index=True)

                    # for errorbars
                    y = np.array(subdata['errbar'][(subdata.sub_ID==s)]).reshape(-1,1)

                    poly_feat = PolynomialFeatures(degree=1)
                    xp = poly_feat.fit_transform(x)
                    xpred = np.linspace(x[0]-100,x[4]+100,(number_of_bins+1)*100)
                    model = sm.OLS(y, xp).fit()
                    b = np.ones((number_of_bins+1)*100)
                    ypred = np.column_stack((b,xpred))
                    intfirst = model.params[0]
                    first = model.params[1]
                    
                    poly_feat = PolynomialFeatures(degree=2)
                    xp = poly_feat.fit_transform(x)
                    model = sm.OLS(y, xp).fit()
                    b = np.ones((number_of_bins+1)*100)
                    c = xpred*xpred
                    ypred = np.column_stack((b,xpred,c))
                    intsecond = model.params[0]
                    second1 = model.params[1]
                    second2 = model.params[2]

                    betadferr = pd.concat([betadferr, pd.DataFrame.from_records([{'sub_ID':s, 'intfirst': intfirst, 'first':first,  'intsecond':intsecond, 'second1':second1, 'second2':second2}])],ignore_index=True)

                xpred = data.groupby(['baseline_split'])['raw_baseline'].mean()
                xplot = np.linspace(xpred[0]-50,xpred[4]+50,100000)

                stat, pfir = sp.stats.ttest_1samp(betadf['first'].values,0.0)
                print('First order poly {} - {}: stat:{} p:{}'.format(drug, task, str(np.round(stat,3)),str(np.round(pfir,5))))
                if pfir < .05:
                    lines = []            
                    lineserr = []
                    for x in np.arange(len(betadf)):
                        lines.append(betadf.loc[x,'intfirst'] + xplot*betadf.loc[x,'first'])
                        lineserr.append(betadferr.loc[x,'intfirst'] + xplot*betadferr.loc[x,'first'])
                    mean = sum(lines)/len(lines)
                    # lines = lines - mean
                    sem = stats.sem(lineserr)
                    axs[row,column].plot(xplot, mean, color='k',linewidth=.5)
                    axs[row,column].fill_between(xplot, mean-sem, mean+sem, color=col, alpha=.4, lw=0.0, edgecolor='None')

                stat, psec = sp.stats.ttest_1samp(betadf['second2'].values,0.0)
                psec = psec/2
                print('Second order poly {} - {}: stat:{} p:{}'.format(drug, task, str(np.round(stat,3)),str(np.round(psec,5))))
                if psec < .05:
                    lines = []
                    lineserr = []
                    for x in np.arange(len(betadf)):
                        lines.append(betadf.loc[x,'intsecond'] + xplot*betadf.loc[x,'second1'] + xplot*xplot*betadf.loc[x,'second2'])
                        lineserr.append(betadferr.loc[x,'intsecond'] + xplot*betadferr.loc[x,'second1'] + xplot*xplot*betadferr.loc[x,'second2'])
                    mean = sum(lines)/len(lines)
                    sem = stats.sem(lineserr)
                    axs[row,column].plot(xplot, mean, color='k',linewidth=.5)
                    axs[row,column].fill_between(xplot, mean-sem, mean+sem, color=col, alpha=.4, lw=0.0, edgecolor='None')

                                       
            for drug,col in zip(['PCB','DNP','ATX'],['coral','steelblue','brown']):
            # for drug,col in zip(['PCB','DNP'],['darkgreen','steelblue']):

                splitdata = pd.DataFrame(thisdata[thisdata.drug==drug].groupby(['sub_ID','baseline_split','task'])[[thisvar,'raw_baseline']].mean()).reset_index()
                
                for task, column, thistitle in zip(['det','dis'],[2,1],['Detection','Discrimination']):

                    data = splitdata[splitdata['task']==task].copy()

                    data['errbar'] = np.nan
                    for s in np.unique(data.sub_ID):
                        submean = data.loc[(data.sub_ID==s),thisvar].mean()
                        data.loc[(data.sub_ID==s),'errbar'] = data.loc[(data.sub_ID==s),thisvar] - submean

                    xpred = data.groupby(['baseline_split'])['raw_baseline'].mean()

                    axs[row,column].errorbar(xpred, data.groupby(['baseline_split'])[thisvar].mean(), yerr=data.groupby(['baseline_split'])['errbar'].sem(),ls='None', ecolor='k', elinewidth=.5, label='')
                    axs[row,column].plot(xpred,data.groupby(['baseline_split'])[thisvar].mean(), marker='o', mec='k', mew=.5, mfc=col, ms=5, ls='None', lw=.5, label=drug)
                    axs[row,0].set_ylabel(thisylab)
                    axs[row,column].ticklabel_format(style='sci',axis='x',scilimits=(0,0))
                    axs[0,column].set_title(thistitle)

            for column in [1,2]:            
                axs[row,column].set_aspect("auto")
                # axs[row,column].set_xlim((2750,4750))
                # axs[row,column].xaxis.set_major_locator(MultipleLocator(500))
                if row == 0: 
                    # axs[row,column].set_ylim(numpy.round(axs[row,column].get_ylim()+np.array([-.025,+.025]),decimals=1)+np.array([0,.0001]))
                    axs[0,column].set_ylim((1.2,1.91))
                    axs[row,column].yaxis.set_major_locator(MultipleLocator(.1))
                elif row == 1:
                    # axs[1,column].set_ylim((0.80,0.891))
                    if column == 1:
                        axs[row,column].set_ylim((0.63,.691))
                    elif column == 2:
                        axs[row,column].set_ylim((0.59,.631))
                    axs[row,column].yaxis.set_major_locator(MultipleLocator(.01))

            

    sns.despine(offset=3, trim=True)
    fig.savefig(os.path.join(this_dir, 'baseline_pupil_drugs_Aug.png'),dpi=1200, transparent = True)
    fig.savefig(os.path.join(this_dir, 'baseline_pupil_drugs_Aug.pdf'), transparent = True)
    plt.close()

def lin_regress_resid(Y,X,project_out=False, eq='ols'):
    
    Y = np.array(Y)
    # prepare data:
    d = {'Y' : pd.Series(Y),}
    for i in range(len(X)):
        d['X{}'.format(i)] = pd.Series(X[i])
    data = pd.DataFrame(d)
    
    # formula:
    formula = 'Y ~ X0'
    if len(X) > 1:
        for i in range(1,len(X)):
            formula = formula + ' + X{}'.format(i)
    
    # fit:
    if eq == 'ols':
        model = SM.ols(formula=formula, data=data)
    fitted = model.fit()
    
    if project_out:
        residuals = fitted.resid + fitted.params['Intercept']
    else:
        residuals = fitted.resid
    
    return np.array(residuals)
    
