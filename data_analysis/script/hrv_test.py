import pandas as pd
from biosppy.signals import ecg
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv(r'E:\EEG_Neurofeedback\data\20240523_01_game\eegraw_20240523_110443_final.csv') 
ecg_signal = data['BIP 01'].values
sampling_rate = 1000  
out = ecg.ecg(signal=ecg_signal, sampling_rate=sampling_rate, show=True)
