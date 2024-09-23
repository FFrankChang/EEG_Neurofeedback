# -*- coding: utf-8 -*-
"""


"""
import os
import sys
import datetime
import pickle
import math
import numpy as np
import scipy as sp
import scipy.stats as stats
import matplotlib
# matplotlib.use('Qt4Agg')
from matplotlib.ticker import FormatStrFormatter
import matplotlib.pyplot as plt
import seaborn as sns #; sns.set()
import pandas as pd
import numpy.linalg as LA
# import bottleneck as bn
import glob
import shutil
from joblib import Parallel, delayed
from statsmodels.stats.anova import AnovaRM
import itertools as it
from itertools import chain
# from IPython import embed as shell
from IPython import embed as shell
from traitlets.config import get_config
# c = get_config()
# c.InteractiveShellEmbed.colors = "Linux"
# shell(config=c)

import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.patches as mpatches
import scipy as sp
from importlib import reload

import statsmodels.api as sm

import functions
import functions_copy
import metad

# import mne
# from mne import io
# from mne.stats import permutation_cluster_test
# from mne.datasets import sample

# import hedfpy
import fir

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
sns.set(style='ticks', font_scale=1, rc={
    'axes.linewidth': 0.25, 
    'axes.labelsize': 7, 
    'axes.titlesize': 7, 
    'xtick.labelsize': 6, 
    'ytick.labelsize': 6, 
    'legend.fontsize': 6, 
    'xtick.major.width': 0.25, 
    'ytick.major.width': 0.25,
    'text.color': 'Black',
    'axes.labelcolor':'Black',
    'xtick.color':'Black',
    'ytick.color':'Black',} )
sns.plotting_context()

project_directory = '/home/lbeeren1/topstore/Researcher beerendonk'

this_dir = os.path.join(project_directory, 'neuromodulation', 'output/figures/corrected/')

try:
    os.makedirs(os.path.join(this_dir))
except OSError:
    pass

df = []

for exp in ['Stijn/discrim','Stijn/detectFA','Stijn/detectMISS','Stijn/attend']:
    df_temp = pd.read_csv(os.path.join(project_directory, exp, 'output', 'meta_noOutliers.csv'))
    df_temp['exp'] = exp
    df.append(df_temp)

df_complete = pd.concat(df, sort=True)
df_complete['modality'] = 'vis'


# remove trials that contain invalid baseline values + trials with fast/no responses
df_complete = df_complete[(~df_complete['raw_baseline'].isnull())].copy()
df_complete = df_complete[(~df_complete['abs_baseline'].isnull())].copy()
df_complete = df_complete[df_complete['RT']>0]

df_complete.reset_index(inplace=True)

# copy this dataframe for later use
df_complete_copy = df_complete.copy() 


shell(colors="neutral")


####### Binning 

# Bin the data for all tasks separately using 5 bins. Outputs one dataframe that contains RT values (meta_all), and another df that contains SDT values (sdt_all)
# Note that meta_all and sdt_all are split according to modality and decision type
meta_all, sdt_all = functions.makebins(df_complete, 5)

# Bin the data for all tasks separately using 20 bins. The way the bins are calculated is identical to functions.makebins,
# but the data is not split into modality and decision types, but averaged across tasks instead 
meta_all20, sdt_all20 = functions.makebins_across_tasks(df_complete,20)


shell(colors="neutral")


### Some stats

# effects of task/drug on prestimulus pupil size:

dfx = df_complete.groupby(['sub_ID','task','drug','miniblock'])['raw_baseline'].mean().groupby(['sub_ID','task','drug']).mean().reset_index()

functions.rm_anova(dfx, 'raw_baseline', ['task','drug'])
# OUT: #                 Anova
# =======================================
#           F Value Num DF  Den DF Pr > F
# ---------------------------------------
# task       4.6876 1.0000 27.0000 0.0394
# drug      25.4634 2.0000 54.0000 0.0000
# task:drug  2.9471 2.0000 54.0000 0.0610
# =======================================

x = dfx.groupby(['drug','sub_ID'])['raw_baseline'].mean().reset_index()
sp.stats.ttest_rel(x[x['drug']=='PCB']['raw_baseline'],x[x['drug']=='DNP']['raw_baseline'])
# TtestResult(statistic=0.7224045363784259, pvalue=0.47625681618715043, df=27)
sp.stats.ttest_rel(x[x['drug']=='PCB']['raw_baseline'],x[x['drug']=='ATX']['raw_baseline'])
# TtestResult(statistic=-4.778089216846843, pvalue=5.529884911535482e-05, df=27)
sp.stats.ttest_rel(x[x['drug']=='DNP']['raw_baseline'],x[x['drug']=='ATX']['raw_baseline'])
# TtestResult(statistic=-6.48866645045163, pvalue=5.900590399036763e-07, df=27)

x = dfx[dfx['task']=='dis'].copy()
sp.stats.ttest_rel(x[x['drug']=='PCB']['raw_baseline'],x[x['drug']=='DNP']['raw_baseline'])
# TtestResult(statistic=1.1698940577985406, pvalue=0.2522673353788218, df=27)
sp.stats.ttest_rel(x[x['drug']=='PCB']['raw_baseline'],x[x['drug']=='ATX']['raw_baseline'])
# TtestResult(statistic=-4.553652576132865, pvalue=0.00010104845844697583, df=27)
sp.stats.ttest_rel(x[x['drug']=='DNP']['raw_baseline'],x[x['drug']=='ATX']['raw_baseline'])
# TtestResult(statistic=-6.551470073200591, pvalue=5.016043480391071e-07, df=27)

x = dfx[dfx['task']=='det'].copy()
sp.stats.ttest_rel(x[x['drug']=='PCB']['raw_baseline'],x[x['drug']=='DNP']['raw_baseline'])
# TtestResult(statistic=0.18447742286719607, pvalue=0.8550175703958888, df=27)
sp.stats.ttest_rel(x[x['drug']=='PCB']['raw_baseline'],x[x['drug']=='ATX']['raw_baseline'])
# TtestResult(statistic=-4.877043535456708, pvalue=4.2383256506982623e-05, df=27)
sp.stats.ttest_rel(x[x['drug']=='DNP']['raw_baseline'],x[x['drug']=='ATX']['raw_baseline'])
# TtestResult(statistic=-6.229943876574482, pvalue=1.1568781914772665e-06, df=27)

# effects of task/drug on d':
dfx = sdt_all.groupby(['task','drug','sub_ID'])[['target','notarget','hit','fa']].sum().reset_index()

dfx['hit_rate'] = dfx['hit'] / dfx['target']
dfx['fa_rate'] = dfx['fa'] / dfx['notarget']

dfx['hit_rate_z'] = stats.norm.isf(1-dfx['hit_rate'])
dfx['fa_rate_z'] =  stats.norm.isf(1-dfx['fa_rate'])

dfx['d'] = dfx['hit_rate_z'] - dfx['fa_rate_z']
dfx['c'] = -(dfx['hit_rate_z'] + dfx['fa_rate_z']) / 2.0

functions.rm_anova(dfx, 'd', ['task','drug'])
#                  Anova
# =======================================
#           F Value Num DF  Den DF Pr > F
# ---------------------------------------
# task       0.5239 1.0000 27.0000 0.4754
# drug       1.0494 2.0000 54.0000 0.3572
# task:drug  2.7944 2.0000 54.0000 0.0700
# =======================================

x = dfx[dfx['task']=='det'].copy()
sp.stats.ttest_rel(x[x['drug']=='PCB']['d'],x[x['drug']=='DNP']['d'])
# TtestResult(statistic=-0.3320409921995735, pvalue=0.7424222333513474, df=27)
sp.stats.ttest_rel(x[x['drug']=='PCB']['d'],x[x['drug']=='ATX']['d'])
# TtestResult(statistic=-0.06310483081679652, pvalue=0.9501478930528082, df=27)
sp.stats.ttest_rel(x[x['drug']=='DNP']['d'],x[x['drug']=='ATX']['d'])
# TtestResult(statistic=0.2497513775368566, pvalue=0.8046700442993419, df=27)

x = dfx[dfx['task']=='dis'].copy()
sp.stats.ttest_rel(x[x['drug']=='PCB']['d'],x[x['drug']=='DNP']['d'])
# TtestResult(statistic=-1.3439566676568933, pvalue=0.19014770751385643, df=27)
sp.stats.ttest_rel(x[x['drug']=='PCB']['d'],x[x['drug']=='ATX']['d'])
# TtestResult(statistic=-2.4229671830051878, pvalue=0.022375699076637442, df=27)
sp.stats.ttest_rel(x[x['drug']=='DNP']['d'],x[x['drug']=='ATX']['d'])
# TtestResult(statistic=-1.3005043974884842, pvalue=0.20441965815170038, df=27)

# effects of task/drug on RT:

dfx = df_complete.groupby(['sub_ID','task','drug','miniblock'])['RT'].mean().groupby(['sub_ID','task','drug']).mean().reset_index()

functions.rm_anova(dfx, 'RT', ['task','drug'])
# OUT: #                 Anova
# =======================================
#           F Value Num DF  Den DF Pr > F
# ---------------------------------------
# task      17.5128 1.0000 27.0000 0.0003
# drug       0.9392 2.0000 54.0000 0.3972
# task:drug  0.7221 2.0000 54.0000 0.4904
# =======================================

x = dfx[dfx['task']=='det'].copy()
sp.stats.ttest_rel(x[x['drug']=='PCB']['RT'],x[x['drug']=='DNP']['RT'])
# TtestResult(statistic=-1.418731052919817, pvalue=0.1674184456410582, df=27)
sp.stats.ttest_rel(x[x['drug']=='PCB']['RT'],x[x['drug']=='ATX']['RT'])
# TtestResult(statistic=-1.1287527025730797, pvalue=0.26893193600439946, df=27)
sp.stats.ttest_rel(x[x['drug']=='DNP']['RT'],x[x['drug']=='ATX']['RT'])
# TtestResult(statistic=0.4370613736928636, pvalue=0.665542646707157, df=27)

x = dfx[dfx['task']=='dis'].copy()
sp.stats.ttest_rel(x[x['drug']=='PCB']['RT'],x[x['drug']=='DNP']['RT'])
#  TtestResult(statistic=-0.4867423211916372, pvalue=0.6303689257402372, df=27)
sp.stats.ttest_rel(x[x['drug']=='PCB']['RT'],x[x['drug']=='ATX']['RT'])
# TtestResult(statistic=-0.8284252852396699, pvalue=0.4146930411525489, df=27)
sp.stats.ttest_rel(x[x['drug']=='DNP']['RT'],x[x['drug']=='ATX']['RT'])
# TtestResult(statistic=-0.247011540813678, pvalue=0.8067678604503672, df=27)



## Fig. 2
this_dir = os.path.join(project_directory, 'neuromodulation', 'output/figures/figure2/')

try:
    os.makedirs(os.path.join(this_dir))
except OSError:
    pass

# plots split for task + drugs or exp + drugs
reload(functions)
functions.binned_plot_pupil_drugs([sdt_all, meta_all], [sdt_all20, meta_all20], 5, ['d','RT'], ['Sensitivity (d\')','Reaction time (s)'], this_dir)


reload(functions)
maxdf = functions.max_points([sdt_all, meta_all], [sdt_all20, meta_all20],['d','RT'])

this_dir = os.path.join(project_directory, 'neuromodulation', 'output/figures/figure2/')

try:
    os.makedirs(os.path.join(this_dir))
except OSError:
    pass

# plots split for task + drugs or exp + drugs
reload(functions)
functions.binned_plot_pupil_drugs_hitfa([sdt_all, sdt_all], [sdt_all20, sdt_all20], number_of_bins, ['hit_rate','c'], ['hit rate','criterion'], this_dir)


### Stats

for var in ['d','hit_rate','fa_rate','raw_baseline']:
    print(var)
    anova_table = AnovaRM(sdt_all, var, 'sub_ID', within=['baseline_split','drug','task'])
    res = anova_table.fit()
    print(res)

for var in ['RT']:
    print(var)
    anova_table = AnovaRM(meta_all, var, 'sub_ID', within=['baseline_split','drug','task'])
    res = anova_table.fit()
    print(res)

detdf = sdt_all[sdt_all['task']=='det'].copy()

for var in ['d','hit_rate','fa_rate','c']:
    print(var)
    anova_table = AnovaRM(detdf, var, 'sub_ID', within=['baseline_split','drug'])
    res = anova_table.fit()
    print(res)

disdf = sdt_all[sdt_all['task']=='dis'].copy()

for var in ['d','hit_rate','fa_rate']:
    print(var)
    anova_table = AnovaRM(disdf, var, 'sub_ID', within=['baseline_split','drug'])
    res = anova_table.fit()
    print(res)


# MLM
import pandas as pd
import statsmodels.formula.api as smf

df1 = sdt_all20.groupby(['sub_ID','baseline_split','drug'])[['raw_baseline','d']].mean().reset_index()

for drug in np.unique(df1['drug']):
    df = df1[df1['drug']==drug]
    print(drug)

    # df = pd.read_csv('/Users/jwdegee/Downloads/baseline_df.csv')
    # df['bin'] = df['bin']-2 # not neccesary
    # for groupby in ['task', 'modality']:
    # for g, d in df.groupby([groupby]):
    d2 = df.groupby(['sub_ID', 'baseline_split']).mean().reset_index()
    md1 = smf.mixedlm("d ~ baseline_split", d2, groups=d2["sub_ID"])
    md2 = smf.mixedlm("d ~ baseline_split + I(baseline_split**2)", d2, groups=d2["sub_ID"])
    mdf1 = md1.fit(reml=False)
    mdf2 = md2.fit(reml=False)
    print()
    # print(groupby)
    # print(g)
    print(mdf2.aic-mdf1.aic)
    # print()
    print(mdf2.bic-mdf1.bic)
    # print(mdf2.summary())



### Fig. 1 

this_dir = os.path.join(project_directory, 'neuromodulation', 'output/figures/figure1/')

try:
    os.makedirs(os.path.join(this_dir))
except OSError:
    pass

## histograms

palette = {
    'PCB': 'darkgreen',
    'ATX': 'steelblue',
    'DNP': 'brown',
}

df_complete['raw_baseline'] = df_complete['raw_baseline']/1000 #for plotting purposes

cm = 1/2.54  # centimeters in inches
fig, axs = plt.subplots(nrows=1, ncols=2, sharex=True, figsize=(9*cm,4*cm))

for task, column , title in zip(['dis','det'],[0,1],['Discrimination','Detection']):

    sns.kdeplot(data=df_complete[df_complete['task']==task],x='raw_baseline',hue='drug', bw_adjust=5, legend=False, palette=palette, lw=1, ax=axs[column])
    axs[column].set_title(title)
    axs[column].ticklabel_format(style='sci',axis='x',scilimits=(0,0))
    axs[0].set_ylabel('Count')
    axs[1].set_ylabel('')
    axs[column].yaxis.set_ticklabels([])
    axs[1].set_xlabel('Baseline pupil (a.u.)')
    axs[0].set_xlabel('')

sns.despine(offset=3, trim=True)

fig.savefig(os.path.join(this_dir, 'pupil_drugs_hist.png'),dpi=1200)
fig.savefig(os.path.join(this_dir, 'pupil_drugs_hist.pdf'))
plt.close()

#######

this_dir = os.path.join(project_directory, 'neuromodulation', 'output/figures/figure1/')

try:
    os.makedirs(os.path.join(this_dir))
except OSError:
    pass

## histograms

palette = {
    'PCB': 'darkgreen',
    'ATX': 'steelblue',
    'DNP': 'brown',
}

df_complete['raw_baseline'] = df_complete['raw_baseline']/1000 #for plotting purposes

cm = 1/2.54  # centimeters in inches
fig, ax = plt.subplots(figsize=(5*cm,4*cm))

sns.kdeplot(data=df_complete,x='raw_baseline',hue='drug', bw_adjust=5, legend=False, palette=palette, lw=1)
# axs[column].set_title(title)
ax.ticklabel_format(style='sci',axis='x',scilimits=(0,0))
ax.set_ylabel('Trial count')
# ax.set_ylabel('')
ax.yaxis.set_ticklabels([])
ax.set_xlabel('Baseline pupil (a.u.)')
ax.set_xlabel('')

sns.despine(offset=3, trim=True)

fig.savefig(os.path.join(this_dir, 'pupil_drugs_hist_all.png'),dpi=1200)
fig.savefig(os.path.join(this_dir, 'pupil_drugs_hist_all.pdf'))
plt.close()


#### pupil trace

this_dir = os.path.join(project_directory, 'neuromodulation', 'output/figures/figure1/')
import hedfpy

try:
    os.makedirs(os.path.join(this_dir))
except OSError:
    pass

subject = 15
preprocess_dir = os.path.join(project_directory, 'Stijn/discrim/pipeline/1_preprocessed', '{}'.format(subject))

hdf5_filename = os.path.join(preprocess_dir, '{}.h5'.format(subject))  
ho = hedfpy.HDFEyeOperator(hdf5_filename)   

alias = 'sub-15_drug-PCB_ses-2_run-1'

trial_times = ho.read_session_data(alias, 'trials')
session_start = trial_times['trial_start_EL_timestamp'][0]
pupil_data = ho.data_from_time_period((np.array(trial_times['trial_start_EL_timestamp'])[0], np.array(trial_times['trial_end_EL_timestamp'])[-1]), alias)
time = np.array(pupil_data['time'])
pupil_raw = np.array(pupil_data[('L_pupil_lp_clean')])

df_raw = pd.DataFrame(np.stack([time, pupil_raw]).T, columns=['time', 'pupil'])

for trials in [3,22,30,45,58,88,98,105,120]:
    start = trials
    end = trials+6

    starttime = trial_times[trial_times['trial_start_index']==start]['trial_start_EL_timestamp'].values[0]
    endtime = trial_times[trial_times['trial_start_index']==end]['trial_end_EL_timestamp'].values[0]

    try: 
        starti = df_raw[df_raw['time']==starttime].index[0]
    except:
        starti = df_raw[df_raw['time']==starttime-1].index[0]
    
    try: 
        endi = df_raw[df_raw['time']==endtime].index[0]
    except:
        endi = df_raw[df_raw['time']==endtime+1].index[0]

    pupil_part = df_raw.iloc[starti:endi]

    fig,ax = plt.subplots()
    plt.plot(np.array(pupil_part['time']),np.array(pupil_part['pupil']), color='k', lw=.5)
    # plt.axvline(0, lw=0.5, color='k')
    fig.savefig(os.path.join(this_dir,'pupil_trace_{}.png'.format(start)),dpi=1200, transparent=True)
    plt.close()


df_complete['raw_baseline'] = df_complete['raw_baseline']/1000 #for plotting purposes



# distributions

### Mean

meanpup = df_complete.groupby(['sub_ID','task','drug'])['raw_baseline'].mean().reset_index()
meanpup_PCB = meanpup[meanpup['drug']=='PCB'].copy()
meanpup_ATX = meanpup[meanpup['drug']=='ATX'].copy()
meanpup_DNP = meanpup[meanpup['drug']=='DNP'].copy()

meanpup = meanpup.merge(meanpup_PCB, on=['sub_ID', 'task'])
meanpup['raw_baseline'] = meanpup['raw_baseline_x']-meanpup['raw_baseline_y']
meanpup = meanpup[meanpup['drug_x']!='PCB']

cm = 1/2.54  # centimeters in inches
fig,ax = plt.subplots(figsize=(3.5*cm,4*cm))

drugs = ['PCB','ACh+','CA+']
bar_colors = ['darkgreen','brown','steelblue']

sns.stripplot(data=meanpup, x='drug_x', y='raw_baseline', hue='drug_x', legend=False, alpha=.35, order=['DNP','ATX'], palette=palette, size=2)
sns.stripplot(data=meanpup.groupby(['drug_x']).mean(), x='drug_x', y='raw_baseline', hue='drug_x', legend=False, order=['DNP','ATX'], palette=palette, marker='d')
ax.axhline(linewidth=.5, ls='dashed', color='k')
ax.set_ylim((-1.5,2))
ax.set_ylabel('Mean pupil (a.u.)')
ax.set_xlabel('')

# ax.set_ylim(3000,3800)
sns.despine(offset=3, trim=True)

fig.savefig(os.path.join(this_dir, 'pupil_mean.pdf'))
fig.savefig(os.path.join(this_dir, 'pupil_mean.png'), dpi=1200)
plt.close()


### SEM

this_dir = os.path.join(project_directory, 'neuromodulation', 'output/figures/figure2/')

try:
    os.makedirs(os.path.join(this_dir))
except OSError:
    pass

variance = df_complete.groupby(['sub_ID','task','drug'])['raw_baseline'].sem().reset_index()
var_PCB = variance[variance['drug']=='PCB'].copy()
var_ATX = variance[variance['drug']=='ATX'].copy()
var_DNP = variance[variance['drug']=='DNP'].copy()

variance = variance.merge(var_PCB, on=['sub_ID', 'task'])
variance['raw_baseline'] = variance['raw_baseline_x']-variance['raw_baseline_y']
variance = variance[variance['drug_x']!='PCB']

cm = 1/2.54  # centimeters in inches
fig,ax = plt.subplots(figsize=(3.5*cm,4*cm))

drugs = ['PCB','ACh+','CA+']
bar_colors = ['darkgreen','brown','steelblue']

sns.stripplot(data=variance, x='drug_x', y='raw_baseline', hue='drug_x', legend=False, alpha=.35, order=['DNP','ATX'], palette=palette, size=2)
sns.stripplot(data=variance.groupby(['drug_x']).mean(), x='drug_x', y='raw_baseline', hue='drug_x', legend=False, order=['DNP','ATX'], palette=palette, marker='d')
ax.axhline(linewidth=.5, ls='dashed', color='k')
ax.set_ylabel('Pupil variance (SEM)')
ax.set_xlabel('')
ax.set_ylim((-4,10))
# ax.ticklabel_format(style='sci',axis='x',scilimits=(0,0))

# ax.set_ylim(3000,3800)
sns.despine(offset=3, trim=True)

fig.savefig(os.path.join(this_dir, 'pupil_sem.pdf'))
fig.savefig(os.path.join(this_dir, 'pupil_sem.png'), dpi=1200)


# Physiological

this_dir = os.path.join(project_directory, 'neuromodulation', 'output/figures/figure2/')

try:
    os.makedirs(os.path.join(this_dir))
except OSError:
    pass

phys = pd.read_csv(os.path.join(project_directory, 'neuromodulation', 'phys_measures.csv'))
phys = phys[phys['measurement']==1]

phys_PCB = phys[phys['drug']=='PLC'].copy()
phys_ATX = phys[phys['drug']=='ATX'].copy()
phys_DNP = phys[phys['drug']=='DNP'].copy()

phys_ATX['HR_cor'] = np.array(phys_ATX['HR_perc'])-np.array(phys_PCB['HR_perc'])
phys_DNP['HR_cor'] = np.array(phys_DNP['HR_perc'])-np.array(phys_PCB['HR_perc'])

phys_ATX['MAP_cor'] = np.array(phys_ATX['MAP_perc'])-np.array(phys_PCB['MAP_perc'])
phys_DNP['MAP_cor'] = np.array(phys_DNP['MAP_perc'])-np.array(phys_PCB['MAP_perc'])

phys_cor = phys_ATX.append(phys_DNP)


cm = 1/2.54  # centimeters in inches
fig,ax = plt.subplots(figsize=(3.5*cm,4*cm))

drugs = ['PCB','ACh+','CA+']
bar_colors = ['darkgreen','brown','steelblue']

sns.stripplot(data=phys_cor, x='drug', y='HR_cor', hue='drug', legend=False, alpha=.35, order=['DNP','ATX'], palette=palette, size=2)
sns.stripplot(data=phys_cor.groupby(['drug']).mean(), x='drug', y='HR_cor', hue='drug', legend=False, order=['DNP','ATX'], palette=palette, marker='d')
ax.axhline(linewidth=.5, ls='dashed', color='k')
ax.set_ylabel('HR modulation (%)')
ax.set_xlabel('')
ax.set_ylim((-40,40))

# ax.set_ylim(3000,3800)
sns.despine(offset=3, trim=True)

fig.savefig(os.path.join(this_dir, 'HR_mean.pdf'))
fig.savefig(os.path.join(this_dir, 'HR_mean.png'), dpi=1200)
plt.close()


cm = 1/2.54  # centimeters in inches
fig,ax = plt.subplots(figsize=(3.5*cm,4*cm))

drugs = ['PCB','ACh+','CA+']
bar_colors = ['darkgreen','brown','steelblue']

sns.stripplot(data=phys_cor, x='drug', y='MAP_cor', hue='drug', legend=False, alpha=.35, order=['DNP','ATX'], palette=palette, size=2)
sns.stripplot(data=phys_cor.groupby(['drug']).mean(), x='drug', y='MAP_cor', hue='drug', legend=False, order=['DNP','ATX'], palette=palette, marker='d')
ax.axhline(linewidth=.5, ls='dashed', color='k')
ax.set_ylabel('BP modulation (%)')
ax.set_xlabel('')

ax.set_ylim((-20,40))
sns.despine(offset=3, trim=True)

fig.savefig(os.path.join(this_dir, 'MAP_mean.pdf'))
fig.savefig(os.path.join(this_dir, 'MAP_mean.png'), dpi=1200)
plt.close()



# MLM
df = sdt_all20.groupby(['sub_ID','baseline_split','drug'])[['raw_baseline','d']].mean().reset_index()
df = df[df['drug']=='DNP']

import pandas as pd
import statsmodels.formula.api as smf
# df = pd.read_csv('/Users/jwdegee/Downloads/baseline_df.csv')
# df['bin'] = df['bin']-2 # not neccesary
# for groupby in ['task', 'modality']:
# for g, d in df.groupby([groupby]):
d2 = df.groupby(['sub_ID', 'baseline_split']).mean().reset_index()
md1 = smf.mixedlm("d ~ baseline_split", d2, groups=d2["sub_ID"])
md2 = smf.mixedlm("d ~ baseline_split + I(baseline_split**2)", d2, groups=d2["sub_ID"])
mdf1 = md1.fit(reml=False)
mdf2 = md2.fit(reml=False)
print()
# print(groupby)
# print(g)
print(mdf2.aic-mdf1.aic)
# print()
print(mdf2.bic-mdf1.bic)
    # print(mdf2.summary())

df = meta_all20.groupby(['sub_ID','baseline_split','drug'])[['raw_baseline','RT']].mean().reset_index()
df = df[df['drug']=='DNP']

import pandas as pd
import statsmodels.formula.api as smf
# df = pd.read_csv('/Users/jwdegee/Downloads/baseline_df.csv')
# df['bin'] = df['bin']-2 # not neccesary
# for groupby in ['task', 'modality']:
# for g, d in df.groupby([groupby]):
d2 = df.groupby(['sub_ID', 'baseline_split']).mean().reset_index()
md1 = smf.mixedlm("RT ~ baseline_split", d2, groups=d2["sub_ID"])
md2 = smf.mixedlm("RT ~ baseline_split + I(baseline_split**2)", d2, groups=d2["sub_ID"])
mdf1 = md1.fit(reml=False)
mdf2 = md2.fit(reml=False)
print()
# print(groupby)
# print(g)
print(mdf2.aic-mdf1.aic)
# print()
print(mdf2.bic-mdf1.bic)
    # print(mdf2.summary())


######### drugs effects det vs. dis

atx_dis = sdt_all[(sdt_all['drug']=='ATX')&(sdt_all['task']=='dis')].groupby('sub_ID')['d'].mean()
plc_dis = sdt_all[(sdt_all['drug']=='PCB')&(sdt_all['task']=='dis')].groupby('sub_ID')['d'].mean()
dnp_dis = sdt_all[(sdt_all['drug']=='DNP')&(sdt_all['task']=='dis')].groupby('sub_ID')['d'].mean()

atx_det = sdt_all[(sdt_all['drug']=='ATX')&(sdt_all['task']=='det')].groupby('sub_ID')['d'].mean()
plc_det = sdt_all[(sdt_all['drug']=='PCB')&(sdt_all['task']=='det')].groupby('sub_ID')['d'].mean()
dnp_det = sdt_all[(sdt_all['drug']=='DNP')&(sdt_all['task']=='det')].groupby('sub_ID')['d'].mean()

stat, p = sp.stats.ttest_rel(np.array(atx_dis),np.array(plc_dis))
print('dis ATX vs PCB', stat,p)

stat, p = sp.stats.ttest_rel(np.array(dnp_dis),np.array(plc_dis))
print('dis DNP vs PCB', stat,p)

stat, p = sp.stats.ttest_rel(np.array(atx_det),np.array(plc_det))
print('det ATX vs PCB', stat,p)


atx_dis_RT = meta_all[(meta_all['drug']=='ATX')&(meta_all['task']=='dis')].groupby('sub_ID')['RT'].mean()
plc_dis_RT = meta_all[(meta_all['drug']=='PCB')&(meta_all['task']=='dis')].groupby('sub_ID')['RT'].mean()
dnp_dis_RT = meta_all[(meta_all['drug']=='DNP')&(meta_all['task']=='dis')].groupby('sub_ID')['RT'].mean()

atx_det_RT = meta_all[(meta_all['drug']=='ATX')&(meta_all['task']=='det')].groupby('sub_ID')['RT'].mean()
plc_det_RT = meta_all[(meta_all['drug']=='PCB')&(meta_all['task']=='det')].groupby('sub_ID')['RT'].mean()
dnp_det_RT = meta_all[(meta_all['drug']=='DNP')&(meta_all['task']=='det')].groupby('sub_ID')['RT'].mean()

stat, p = sp.stats.ttest_rel(np.array(atx_dis_RT),np.array(plc_dis_RT))
print('dis ATX vs PCB RT', stat,p)

stat, p = sp.stats.ttest_rel(np.array(dnp_dis_RT),np.array(plc_dis_RT))
print('dis DNP vs PCB RT', stat,p)

stat, p = sp.stats.ttest_rel(np.array(atx_det_RT),np.array(plc_det_RT))
print('det ATX vs PCB RT', stat,p)

stat, p = sp.stats.ttest_rel(np.array(dnp_det_RT),np.array(plc_det_RT))
print('det DNP vs PCB RT', stat,p)

