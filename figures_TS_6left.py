"""
Created by Marion Bocquet
Date : 15/04/2024
Credits : LEGOS/CNES/CLS
The script aims to plot the time series and create pdfs
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import seaborn as sns

import matplotlib.ticker as tck
from matplotlib import gridspec


start_date = '199401'
end_date = '202306'
PATH = './DATA/'

def fill_df_nan(df, start_date, end_date):
    """
    Complete dataframe with nans for each month there are no values
    :param df: dataframe to fill
    :param start_date: first date to start filling
    :param end_date: last date to fill
    :return: pandas dataframe filled
    """
    # Complete df with nan
    nb_month = diff_month(datetime(int(end_date[0:4]), 12, 31), datetime(int(start_date[0:4]), 1, 1)) + 1
    df_time_complete = pd.date_range(np.datetime64('%s-%s-01' % (start_date[0:4], start_date[4::])), freq='MS',
                                     periods=nb_month + 1) + pd.DateOffset(days=14)
    data_df_time = np.zeros((df_time_complete.shape[0], df.shape[1])) + np.nan
    df_time = pd.DataFrame(columns=df.columns, data=data_df_time, index=df_time_complete)
    df_time = df_time.rename_axis('time', axis=0)
    df = df.set_index(pd.to_datetime((df.set_index('time').index).values))
    df_red = pd.concat([df, df_time])
    df_red = df_red[~df_red.index.duplicated(keep='first')].sort_index()
    return df_red

def diff_month(d1, d2):
    """
    Compute the number of month between two dates (minus one month)
    :param d1: date1
    :param d2: date3
    :return:
    """
    return (d1.year - d2.year) * 12 + d1.month - d2.month
def concat_df_dealing_overlaps(dates_drop_overlap_ers1, dates_drop_overlap_ers2, dates_drop_overlap_env3, dates_drop_overlap_cs2, list_df):
    """
    :param dates_drop_overlap_ers1: list of dates to remove in ERS1
    :param dates_drop_overlap_ers2: list of dates to remove in ERS2
    :param dates_drop_overlap_env3: list of dates to remove in Envisat
    :param dates_drop_overlap_cs2: list of dates to remove in CS2
    :param list_df: list of dataframe to drop dates and to concat (ers1, ers2, envisat and cs2)
    :return: dataframe concatenate and fill by nan where needed
    """
    # Drop dates overlapping
    df_ers1_dropped = list_df[0].drop(dates_drop_overlap_ers1, axis=0)
    df_ers2_dropped = list_df[1].drop(dates_drop_overlap_ers2, axis=0)
    df_env3_dropped = list_df[2].drop(dates_drop_overlap_env3, axis=0)
    df_cs2_dropped = list_df[3].drop(dates_drop_overlap_cs2, axis=0)

    # concat
    df_dropped = pd.concat([df_ers1_dropped, df_ers2_dropped, df_env3_dropped, df_cs2_dropped])
    # fill
    df_dropped_fill = fill_df_nan(df_dropped, '%s%s' %(list_df[3].index.min().year, str(list_df[3].index.min().month).zfill(2)), '%s%s' %(str(list_df[3].index.max().year), str(list_df[3].index.max().month).zfill(2)))

    return df_dropped_fill


##### LOAD DATA #####

NH_vol_ers1r = pd.read_csv(PATH + 'W99m_ers1r_corr.csv')
NH_vol_ers1r = fill_df_nan(NH_vol_ers1r, start_date, end_date)
NH_mc_vol_ers1r = pd.read_csv(PATH + 'W99_STAT_ers1r.csv')
NH_mc_vol_ers1r = NH_mc_vol_ers1r.set_index('Unnamed: 0')
NH_vol_ers1r_q025 = NH_mc_vol_ers1r.loc['5%']
NH_vol_ers1r_q025 = fill_df_nan(NH_vol_ers1r_q025, start_date, end_date)
NH_vol_ers1r_q975 = NH_mc_vol_ers1r.loc['95%']
NH_vol_ers1r_q975 = fill_df_nan(NH_vol_ers1r_q975, start_date, end_date)

NH_vol_ers2r = pd.read_csv(PATH + 'W99m_ers2r_corr.csv')
NH_vol_ers2r = fill_df_nan(NH_vol_ers2r, start_date, end_date)
NH_mc_vol_ers2r = pd.read_csv(PATH + 'W99_STAT_ers2r.csv')
NH_mc_vol_ers2r = NH_mc_vol_ers2r.set_index('Unnamed: 0')
NH_vol_ers2r_q025 = NH_mc_vol_ers2r.loc['5%']
NH_vol_ers2r_q025 = fill_df_nan(NH_vol_ers2r_q025, start_date, end_date)
NH_vol_ers2r_q975 = NH_mc_vol_ers2r.loc['95%']
NH_vol_ers2r_q975 = fill_df_nan(NH_vol_ers2r_q975, start_date, end_date)

NH_vol_env3 = pd.read_csv(PATH + 'W99m_env3_corr.csv')
NH_vol_env3 = fill_df_nan(NH_vol_env3, start_date, end_date)
NH_mc_vol_env3 = pd.read_csv(PATH + 'W99_STAT_env3.csv')
NH_mc_vol_env3 = NH_mc_vol_env3.set_index('Unnamed: 0')
NH_vol_env3_q025 = NH_mc_vol_env3.loc['5%']
NH_vol_env3_q025 = fill_df_nan(NH_vol_env3_q025, start_date, end_date)
NH_vol_env3_q975 = NH_mc_vol_env3.loc['95%']
NH_vol_env3_q975 = fill_df_nan(NH_vol_env3_q975, start_date, end_date)

NH_vol_c2 = pd.read_csv(PATH + 'W99m_c2esaD1.csv')
NH_vol_c2 = fill_df_nan(NH_vol_c2, start_date, end_date)
NH_mc_vol_c2 = pd.read_csv(PATH + 'W99_STAT_c2esaD1.csv')
NH_mc_vol_c2 = NH_mc_vol_c2.set_index('Unnamed: 0')
NH_vol_c2_q025 = NH_mc_vol_c2.loc['5%']
NH_vol_c2_q025 = fill_df_nan(NH_vol_c2_q025, start_date, end_date)
NH_vol_c2_q975 = NH_mc_vol_c2.loc['95%']
NH_vol_c2_q975 = fill_df_nan(NH_vol_c2_q975, start_date, end_date)

SH_vol_ers1r = pd.read_csv(PATH + 'ers1rSH_corr.csv')
SH_vol_ers1r = fill_df_nan(SH_vol_ers1r, start_date, end_date)
SH_mc_vol_ers1r = pd.read_csv(PATH + 'STAT_ers1rSH_corr.csv')
SH_mc_vol_ers1r = SH_mc_vol_ers1r.set_index('Unnamed: 0')
SH_vol_ers1r_q025 = SH_mc_vol_ers1r.loc['5%']
SH_vol_ers1r_q025 = fill_df_nan(SH_vol_ers1r_q025, start_date, end_date)
SH_vol_ers1r_q975 = SH_mc_vol_ers1r.loc['95%']
SH_vol_ers1r_q975 = fill_df_nan(SH_vol_ers1r_q975, start_date, end_date)

SH_vol_ers2r = pd.read_csv(PATH + 'ers2rSH_corr.csv')
SH_vol_ers2r = fill_df_nan(SH_vol_ers2r, start_date, end_date)
SH_mc_vol_ers2r = pd.read_csv(PATH + 'STAT_ers2rSH_corr.csv')
SH_mc_vol_ers2r = SH_mc_vol_ers2r.set_index('Unnamed: 0')
SH_vol_ers2r_q025 = SH_mc_vol_ers2r.loc['5%']
SH_vol_ers2r_q025 = fill_df_nan(SH_vol_ers2r_q025, start_date, end_date)
SH_vol_ers2r_q975 = SH_mc_vol_ers2r.loc['95%']
SH_vol_ers2r_q975 = fill_df_nan(SH_vol_ers2r_q975, start_date, end_date)

SH_vol_env3 = pd.read_csv(PATH + 'env3SH_corr.csv')
SH_vol_env3 = fill_df_nan(SH_vol_env3, start_date, end_date)
SH_mc_vol_env3 = pd.read_csv(PATH + 'STAT_env3SH_corr.csv')
SH_mc_vol_env3 = SH_mc_vol_env3.set_index('Unnamed: 0')
SH_vol_env3_q025 = SH_mc_vol_env3.loc['5%']
SH_vol_env3_q025 = fill_df_nan(SH_vol_env3_q025, start_date, end_date)
SH_vol_env3_q975 = SH_mc_vol_env3.loc['95%']
SH_vol_env3_q975 = fill_df_nan(SH_vol_env3_q975, start_date, end_date)

SH_vol_c2 = pd.read_csv(PATH + 'c2esaDSH1_SARpIN.csv')
SH_vol_c2 = fill_df_nan(SH_vol_c2, start_date, end_date)
SH_mc_vol_c2 = pd.read_csv(PATH + 'STAT_c2esaDSH1_SARpIN.csv')
SH_mc_vol_c2 = SH_mc_vol_c2.set_index('Unnamed: 0')
SH_vol_c2_q025 = SH_mc_vol_c2.loc['5%']
SH_vol_c2_q025 = fill_df_nan(SH_vol_c2_q025, start_date, end_date)
SH_vol_c2_q975 = SH_mc_vol_c2.loc['95%']
SH_vol_c2_q975 = fill_df_nan(SH_vol_c2_q975, start_date, end_date)

print('All .csv are loaded')
#####--- END LOAD DATA #####


####### Deals with overlaps #####

dates_overlap_NH = [np.datetime64('1995-10-15'), np.datetime64('1995-11-15'),
                    np.datetime64('1995-12-15'), np.datetime64('1996-01-15'),
                    np.datetime64('1996-02-15'), np.datetime64('1996-03-15'),
                    np.datetime64('1996-04-15'), np.datetime64('2002-10-15'),
                    np.datetime64('2002-11-15'), np.datetime64('2002-12-15'),
                    np.datetime64('2003-01-15'), np.datetime64('2003-02-15'),
                    np.datetime64('2003-03-15'), np.datetime64('2003-04-15'),
                    np.datetime64('2010-11-15'), np.datetime64('2010-12-15'),
                    np.datetime64('2011-01-15'), np.datetime64('2011-02-15'),
                    np.datetime64('2011-03-15'), np.datetime64('2011-04-15'),
                    np.datetime64('2011-10-15'), np.datetime64('2011-11-15'),
                    np.datetime64('2011-12-15'), np.datetime64('2012-01-15'),
                    np.datetime64('2012-02-15'), np.datetime64('2012-03-15')]
dates_drop_overlap_ers1_NH = [np.datetime64('1995-10-15'), np.datetime64('1995-11-15'),
                              np.datetime64('1995-12-15'), np.datetime64('1996-01-15'),
                              np.datetime64('1996-02-15'), np.datetime64('1996-03-15'),
                              np.datetime64('1996-04-15')]
dates_drop_overlap_ers2_NH = [np.datetime64('2002-10-15'), np.datetime64('2002-11-15'),
                              np.datetime64('2002-12-15'), np.datetime64('2003-01-15'),
                              np.datetime64('2003-02-15'), np.datetime64('2003-03-15'),
                              np.datetime64('2003-04-15')]
dates_drop_overlap_env3_NH = [np.datetime64('2011-10-15'), np.datetime64('2011-11-15'),
                              np.datetime64('2011-12-15'), np.datetime64('2012-01-15'),
                              np.datetime64('2012-02-15'), np.datetime64('2012-03-15')]
dates_drop_overlap_cs2_NH = [np.datetime64('2010-11-15'), np.datetime64('2010-12-15'),
                             np.datetime64('2011-01-15'), np.datetime64('2011-02-15'),
                             np.datetime64('2011-03-15'), np.datetime64('2011-04-15')]

dates_overlap_SH = [np.datetime64('1995-05-15'), np.datetime64('1995-06-15'),
                    np.datetime64('1995-07-15'), np.datetime64('1995-08-15'),
                    np.datetime64('1995-09-15'), np.datetime64('1995-10-15'),
                    np.datetime64('1995-11-15'), np.datetime64('1995-12-15'),
                    np.datetime64('1996-01-15'), np.datetime64('1996-02-15'),
                    np.datetime64('1996-03-15'), np.datetime64('1996-04-15'),
                    np.datetime64('1996-05-15'), np.datetime64('2002-06-15'),
                    np.datetime64('2002-07-15'), np.datetime64('2002-08-15'),
                    np.datetime64('2002-09-15'), np.datetime64('2002-10-15'),
                    np.datetime64('2002-11-15'), np.datetime64('2002-12-15'),
                    np.datetime64('2003-01-15'), np.datetime64('2003-02-15'),
                    np.datetime64('2003-03-15'), np.datetime64('2003-04-15'),
                    np.datetime64('2003-05-15'), np.datetime64('2010-12-15'),
                    np.datetime64('2011-01-15'), np.datetime64('2011-02-15'),
                    np.datetime64('2011-03-15'), np.datetime64('2011-04-15'),
                    np.datetime64('2011-05-15'), np.datetime64('2011-06-15'),
                    np.datetime64('2011-07-15'), np.datetime64('2011-08-15'),
                    np.datetime64('2011-09-15'), np.datetime64('2011-10-15'),
                    np.datetime64('2011-11-15'), np.datetime64('2011-12-15'),
                    np.datetime64('2012-01-15'), np.datetime64('2012-02-15'),
                    np.datetime64('2012-03-15')]
dates_drop_overlap_ers1_SH = [np.datetime64('1995-05-15'), np.datetime64('1995-06-15'),
                              np.datetime64('1995-07-15'), np.datetime64('1995-08-15'),
                              np.datetime64('1995-09-15'), np.datetime64('1995-10-15'),
                              np.datetime64('1995-11-15'), np.datetime64('1995-12-15'),
                              np.datetime64('1996-01-15'), np.datetime64('1996-02-15'),
                              np.datetime64('1996-03-15'), np.datetime64('1996-04-15'),
                              np.datetime64('1996-05-15')]
dates_drop_overlap_ers2_SH = [np.datetime64('2002-06-15'), np.datetime64('2002-07-15'),
                              np.datetime64('2002-08-15'), np.datetime64('2002-09-15'),
                              np.datetime64('2002-10-15'), np.datetime64('2002-11-15'),
                              np.datetime64('2002-12-15'), np.datetime64('2003-01-15'),
                              np.datetime64('2003-02-15'), np.datetime64('2003-03-15'),
                              np.datetime64('2003-04-15'), np.datetime64('2003-05-15')]
dates_drop_overlap_env3_SH = [np.datetime64('2011-01-15'), np.datetime64('2011-02-15'),
                              np.datetime64('2011-03-15'), np.datetime64('2011-04-15'),
                              np.datetime64('2011-05-15'), np.datetime64('2011-06-15'),
                              np.datetime64('2011-07-15'), np.datetime64('2011-08-15'),
                              np.datetime64('2011-09-15'), np.datetime64('2011-10-15'),
                              np.datetime64('2011-11-15'), np.datetime64('2011-12-15'),
                              np.datetime64('2012-01-15'), np.datetime64('2012-02-15'),
                              np.datetime64('2012-03-15')]
dates_drop_overlap_cs2_SH = [np.datetime64('2010-12-15')]


df_volumes_NH = concat_df_dealing_overlaps(dates_drop_overlap_ers1_NH,
                                               dates_drop_overlap_ers2_NH,
                                               dates_drop_overlap_env3_NH,
                                               dates_drop_overlap_cs2_NH,
                                               [NH_vol_ers1r, NH_vol_ers2r, NH_vol_env3, NH_vol_c2])
df_volumes_SH = concat_df_dealing_overlaps(dates_drop_overlap_ers1_SH,
                                               dates_drop_overlap_ers2_SH,
                                               dates_drop_overlap_env3_SH,
                                               dates_drop_overlap_cs2_SH,
                                               [SH_vol_ers1r, SH_vol_ers2r, SH_vol_env3, SH_vol_c2])

df_volumes_NH = fill_df_nan(df_volumes_NH, '199401', '202304')

df_volumes_SH = fill_df_nan(df_volumes_SH, '199401', '202306')

df_volumes_NH = df_volumes_NH[df_volumes_NH.time.notna()]


df_volumes_SH = df_volumes_SH[df_volumes_SH.time.notna()]
df_volumes_SH['evolume_region_1'] = df_volumes_SH['evolume'] - df_volumes_SH['evolume_region_2'] - df_volumes_SH[
    'evolume_region_3'] - df_volumes_SH['evolume_region_4'] - df_volumes_SH['evolume_region_5'] - df_volumes_SH[
                                        'evolume_region_6'] - df_volumes_SH['evolume_region_7']
df_volumes_SH['evolume_region_56'] = df_volumes_SH['evolume_region_5'] + df_volumes_SH['evolume_region_6']

df_volumes_NH_q025 = concat_df_dealing_overlaps(dates_drop_overlap_ers1_NH,
                                                    dates_drop_overlap_ers2_NH,
                                                    dates_drop_overlap_env3_NH,
                                                    dates_drop_overlap_cs2_NH,
                                                    [NH_vol_ers1r_q025, NH_vol_ers2r_q025,
                                                     NH_vol_env3_q025, NH_vol_c2_q025])
df_volumes_NH_q975 = concat_df_dealing_overlaps(dates_drop_overlap_ers1_NH,
                                                    dates_drop_overlap_ers2_NH,
                                                    dates_drop_overlap_env3_NH,
                                                    dates_drop_overlap_cs2_NH,
                                                    [NH_vol_ers1r_q975, NH_vol_ers2r_q975,
                                                     NH_vol_env3_q975, NH_vol_c2_q975])

df_volumes_SH_q025 = concat_df_dealing_overlaps(dates_drop_overlap_ers1_SH,
                                                    dates_drop_overlap_ers2_SH,
                                                    dates_drop_overlap_env3_SH,
                                                    dates_drop_overlap_cs2_SH,
                                                    [SH_vol_ers1r_q025, SH_vol_ers2r_q025,
                                                     SH_vol_env3_q025, SH_vol_c2_q025])

df_volumes_NH_q975 = concat_df_dealing_overlaps(dates_drop_overlap_ers1_NH,
                                                    dates_drop_overlap_ers2_NH,
                                                    dates_drop_overlap_env3_NH,
                                                    dates_drop_overlap_cs2_NH,
                                                    [NH_vol_ers1r_q975, NH_vol_ers2r_q975,
                                                     NH_vol_env3_q975, NH_vol_c2_q975])

df_volumes_SH_q025 = concat_df_dealing_overlaps(dates_drop_overlap_ers1_SH,
                                                    dates_drop_overlap_ers2_SH,
                                                    dates_drop_overlap_env3_SH,
                                                    dates_drop_overlap_cs2_SH,
                                                    [SH_vol_ers1r_q025, SH_vol_ers2r_q025,
                                                     SH_vol_env3_q025, SH_vol_c2_q025])

df_volumes_SH_q975 = concat_df_dealing_overlaps(dates_drop_overlap_ers1_SH,
                                                    dates_drop_overlap_ers2_SH,
                                                    dates_drop_overlap_env3_SH,
                                                    dates_drop_overlap_cs2_SH,
                                                    [SH_vol_ers1r_q975, SH_vol_ers2r_q975,
                                                     SH_vol_env3_q975, SH_vol_c2_q975])


####### End Deals with overlaps #####


df_volumes_NH['time'] = pd.to_datetime(df_volumes_NH.time)
df_volumes_NH = df_volumes_NH.set_index('time', drop=False)




##### seasonal cycle

df_volumes_NH['month'] = df_volumes_NH.index.month
df_volumes_SH['month'] = df_volumes_SH.index.month
df_volumes_NH['year'] = df_volumes_NH.index.year
df_volumes_SH['year'] = df_volumes_SH.index.year


def plot_TS_unc(NH_vol_ers1r, NH_vol_ers1r_q025, NH_vol_ers1r_q975, NH_vol_ers2r, NH_vol_ers2r_q025, NH_vol_ers2r_q975,
                NH_vol_env3, NH_vol_env3_q025, NH_vol_env3_q975, NH_vol_c2, NH_vol_c2_q025, NH_vol_c2_q975,
                SH_vol_ers1r, SH_vol_ers1r_q025, SH_vol_ers1r_q975, SH_vol_ers2r, SH_vol_ers2r_q025,
                SH_vol_ers2r_q975, SH_vol_env3, SH_vol_env3_q025, SH_vol_env3_q975, SH_vol_c2, SH_vol_c2_q025, SH_vol_c2_q975,
                df_volumes_NH, df_volumes_SH):
    figure = plt.figure('Time series', figsize=(12, 6))
    sns.set_style("ticks")
    sns.despine()
    spec = gridspec.GridSpec(ncols=1, nrows=2)
    ax0 = figure.add_subplot(spec[0])
    ax1 = figure.add_subplot(spec[1])

    ax0.fill_between(NH_vol_ers1r.index, NH_vol_ers1r_q025.evolume, NH_vol_ers1r_q975.evolume, alpha=0.5, color='gray',
                     linewidth=0, label='90% confidence')
    ax0.fill_between(NH_vol_ers2r.index, NH_vol_ers2r_q025.evolume, NH_vol_ers2r_q975.evolume, alpha=0.5, color='gray',
                     linewidth=0)
    ax0.fill_between(NH_vol_env3.index, NH_vol_env3_q025.evolume, NH_vol_env3_q975.evolume, alpha=0.5, color='gray',
                     linewidth=0)
    ax0.fill_between(NH_vol_c2.index, NH_vol_c2_q025.evolume, NH_vol_c2_q975.evolume, alpha=0.5, color='gray',
                     linewidth=0)
    ax0.plot(NH_vol_c2.index, NH_vol_c2.evolume, '.-', color='#011f4b', markersize=6.5, lw=1, label='CryoSat-2')
    ax0.plot(NH_vol_env3.index, NH_vol_env3.evolume, '.-', color='#005b96', markersize=6.5, lw=1, label='Envisat')
    ax0.plot(NH_vol_ers2r.index, NH_vol_ers2r.evolume, '.-', color='#6497b1', markersize=6.5, lw=1, label='ERS-2')
    ax0.plot(NH_vol_ers1r.index, NH_vol_ers1r.evolume, '.-', color='#9AC0CD', markersize=6.5, lw=1, label='ERS-1')

    ax0.set_ylim(ymin=0)


    ax0.legend(ncol=5, frameon=False, loc='upper left', reverse=True)
    ax0.set_ylabel('Volume $km^3$')
    ax0.set_xlabel('Year')

    ax1.fill_between(SH_vol_ers1r.index, SH_vol_ers1r_q025.evolume, SH_vol_ers1r_q975.evolume, alpha=0.5, color='gray',
                     linewidth=0)
    ax1.plot(SH_vol_ers1r.index, SH_vol_ers1r.evolume, '.-', color='#9AC0CD', markersize=6.5, lw=1, label='ERS-1')
    ax1.fill_between(SH_vol_ers2r.index, SH_vol_ers2r_q025.evolume, SH_vol_ers2r_q975.evolume, alpha=0.5, color='gray',
                     linewidth=0)
    ax1.plot(SH_vol_ers2r.index, SH_vol_ers2r.evolume, '.-', color='#6497b1', markersize=6.5, lw=1, label='ERS-2')
    ax1.fill_between(SH_vol_env3.index, SH_vol_env3_q025.evolume, SH_vol_env3_q975.evolume, alpha=0.5, color='gray',
                     linewidth=0)
    ax1.plot(SH_vol_env3.index, SH_vol_env3.evolume, '.-', color='#005b96', markersize=6.5, lw=1, label='Envisat')
    ax1.fill_between(SH_vol_c2.index, SH_vol_c2_q025.evolume, SH_vol_c2_q975.evolume, alpha=0.5, color='gray',
                     linewidth=0)
    ax1.plot(SH_vol_c2.index, SH_vol_c2.evolume, '.-', color='#011f4b', markersize=6.5, lw=1, label='CryoSat-2')
    ax1.set_ylim(ymin=0)

    ax1.set_ylabel('Volume $km^3$')
    ax1.set_xlabel('Year')


    ax0.yaxis.set_minor_locator(tck.AutoMinorLocator())
    ax0.xaxis.set_minor_locator(tck.AutoMinorLocator())
    ax1.xaxis.set_minor_locator(tck.AutoMinorLocator())
    ax1.yaxis.set_minor_locator(tck.AutoMinorLocator())
    plt.tight_layout()
    plt.subplots_adjust(top=0.96, bottom=0.085, wspace=0.2)

    ax0.set_title('(a)', loc='left')
    ax1.set_title('(b)', loc='left')

    plt.savefig('vol_TS_noclim.pdf')


plot_TS_unc(NH_vol_ers1r, NH_vol_ers1r_q025, NH_vol_ers1r_q975, NH_vol_ers2r, NH_vol_ers2r_q025, NH_vol_ers2r_q975,
            NH_vol_env3, NH_vol_env3_q025, NH_vol_env3_q975, NH_vol_c2, NH_vol_c2_q025, NH_vol_c2_q975,
            SH_vol_ers1r, SH_vol_ers1r_q025, SH_vol_ers1r_q975, SH_vol_ers2r, SH_vol_ers2r_q025,
            SH_vol_ers2r_q975, SH_vol_env3, SH_vol_env3_q025, SH_vol_env3_q975, SH_vol_c2, SH_vol_c2_q025, SH_vol_c2_q975,
            df_volumes_NH, df_volumes_SH)


