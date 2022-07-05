import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

import random


def add_trends(df, monthly_coff=[], weekly_coff=[]):
  ranges = pd.date_range(start=df.index[0] ,end=df.index[-1], freq='W-MON')

  for i in range(0, len(ranges)-1):

    # df['profit'].loc[ranges[i]:ranges[i+1]] *= monthly_coff[i % len(monthly_coff)]
    df['profit'].loc[ranges[i]:ranges[i+1]] = np.add(df['profit'].loc[ranges[i]:ranges[i+1]].to_numpy(), weekly_coff)
  
def add_anomalys(df, n = 100):
  df.loc[random.sample(list(df.index), n)]['profit'] *= np.random.random(size=n)